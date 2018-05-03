from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import CreateView, UpdateView

from departures.forms import CustomDepartureFormSet
from departures.models import Departure
from main_requests.model_additional import MainRequestAddition
from work3.settings import DATETIME_INPUT_FORMATS
from work_profiles.models import Profile
from .filter import MainRequestFilter
from .forms import newMainRequestForm, updateMainRequestForm
from .models import MainRequest
from departures import models as model_departure


# Create your views here.
# @login_required
# для тестов
def simple(request):
    return render(request, 'simple.html')


# создание новой заявки
class CreateNewRequest(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = '/base/filter-request/'
    form_class = newMainRequestForm
    template_name = 'baseviews/new_request/new_request.html'
    success_url = '/base/filter-request/'

    def get_form_kwargs(self):
        kwargs = super(CreateNewRequest, self).get_form_kwargs()
        user = self.request.user
        prof = Profile.objects.get(user=user)
        dep = prof.deparment.name
        position = prof.user_position
        kwargs.update({'user': user})
        initial = kwargs.pop('initial')
        initial.update({'request_outer_department': dep})
        initial.update({'request_outer_status': position})
        initial.update({'request_user': prof})

        kwargs.update({'initial': initial})

        # kwargs.update({'request_outer_department': dep})
        # kwargs.update({'request_outer_status': position})
        return kwargs

    def get_context_data(self, **kwargs):
        profiles = Profile.objects.all()
        data = super(CreateNewRequest, self).get_context_data(**kwargs)
        data['profiles'] = profiles

        return data

    def get_success_url(self):
        # print(self.request.META['HTTP_REFERER'])
        return redirect('base_create_view_success', number=1)

    def form_valid(self, form):
        new_request = form.save(commit=False)
        user = self.request.user
        new_request.input_user = Profile.objects.get(user=user)
        old_number = MainRequest.objects.all().aggregate(Max('number'))
        new_request.number = old_number['number__max'] + 1
        if new_request.request_user is not None:
            new_request.request_outer_status = None
            new_request.request_outer_department = None
        new_request.save()
        return JsonResponse({'success': True,
                             'number': new_request.number})
        # return render(self.request,'baseviews/new_request/success_new_request.html', {'number':new_request.number})
        # return super().form_valid(form)

    def form_invalid(self, form):
        return JsonResponse({'success': False,
                             'errors': [(k, v[0]) for k, v in form.errors.items()]})


def new_request_success(request):
    return render(request, 'baseviews/new_request/success_new_request.html')


# изменеие формы заявок
class UpdateRequest(UpdateView):
    form_class = updateMainRequestForm
    model = MainRequest
    template_name = 'baseviews/update_view/update.html'
    success_url = '/simplle/'

    def get_form_kwargs(self):
        kwargs = super(UpdateRequest, self).get_form_kwargs()
        kwargs.update({'place_user': self.request.user})

        return kwargs

    def get_context_data(self, **kwargs):
        data = super(UpdateRequest, self).get_context_data(**kwargs)
        profiles = Profile.objects.all()
        data['profiles'] = profiles
        if self.request.POST:
            data['departures'] = CustomDepartureFormSet(self.request.POST, instance=self.object,
                                                        dep_user=self.request.user)
        else:
            data['departures'] = CustomDepartureFormSet(instance=self.object, dep_user=self.request.user)
        can_save = self.object.can_save(self.request.user)
        data['can_save'] = can_save
        # print('Permitions ---',self.request.user.has_perms('departures.add_departure'))


        data['can_add_departure'] = self.object.can_add_dep(self.request.user)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        departures = context['departures']
        # try to delete object before valid
        dep_ids = []
        if form.is_valid():
            # print("Form valid")
            # for dep in departures.forms:
            #     print('dep obj')
            #     if dep in departures.deleted_forms:
            #         print("Delete")


            counter = 0
            if departures.is_valid():
                # print("deparures valid")
                with transaction.atomic():  # что это за  хрень?
                    self.object = form.save()
                    assert isinstance(departures, CustomDepartureFormSet)
                    departures.instance = self.object
                    for formdep in departures.forms:
                        departure = formdep.save(commit=False)
                        departure.input_user = Profile.objects.get(user=self.request.user)
                        # print('dperture - ',formdep.instance.id,' ',formdep.instance.main_request )
                        counter += 1
                        dep_id = [{'id': formdep.instance.id, 'number': counter}]
                        if formdep in departures.deleted_forms:
                            dep_id.append({'id_deleted': 'true'})
                        dep_ids.append(dep_id)
                departures.save()

                return JsonResponse({'success': True, 'dep_ids': dep_ids})
            else:

                # print(departures.non_form_errors)
                # print(departures.errors)
                deps_errors = []
                counter = 0
                for dep_form in departures.forms:
                    counter += 1
                    if not dep_form.is_valid:
                        dep_errors = {counter: [(k, v[0]) for k, v in form.errors.items()]}

                return JsonResponse({'success': False,
                                     'departures_errors': [{'departures': departures.errors}],
                                     'dep_ids': dep_ids,
                                     'errors': []}, safe=False)

    def form_invalid(self, form):
        return JsonResponse({'success': False,
                             'errors': [(k, v[0]) for k, v in form.errors.items()]}, safe=False)


# для тестов
@login_required
def test_base(request):
    return render(request, 'test2/request-list.html')


# фильтр json 20:00 - rjytw cvtys
# filter
@login_required
def ListFilterJsonView(request):
    get_form = request.GET.get("get_form")
    if get_form is not None and get_form:
        f = MainRequestFilter(request.GET, queryset=MainRequest.objects.all().order_by('-pk')[0:1])
        return render(request, 'includes/arctic-form/filter-form', {'form': f.form})

    dt = timezone.now()
    dt_last_yesterday = (dt + timedelta(days=-1)).replace(hour=20).replace(minute=0).replace(second=0)
    dt_input = request.GET.get('last-dt')
    first_id = request.GET.get('first_id')
    row_count = 20
    f = MainRequestFilter(request.GET, queryset=MainRequest.objects.all().order_by('-pk'))
    not_closed_departure = request.GET.get('not_closed_departure')
    dc = Departure.objects.filter(start_datetime__lt=dt_last_yesterday, end_datetime__isnull=True)
    if dc.__len__()>0:

        not_cl_dep_requests = MainRequest.objects.filter(id__in=dc.values_list('main_request',flat=True))

        print(dt_last_yesterday,not_cl_dep_requests, dt_input)
        if not_cl_dep_requests.__len__() > 0:
            if f.form.is_valid():
                deps_need_closed = []

                for req in not_cl_dep_requests:
                    json = req.to_dict
                    add_main_req = MainRequestAddition(req)
                    json1 = add_main_req.to_dict_add()
                    deps_need_closed.append(json1)
                json_delete_change = []
                if dt_input is not None:
                    if dt_input != '':
                        list_changed_not_in_filter = MainRequest.objects.filter(changed_datetime__gt=dt_input)

                        list_changed_not_in_filter = list_changed_not_in_filter.exclude(
                        id__in=not_cl_dep_requests.values_list('id', flat=True))
                        for req in list_changed_not_in_filter:
                            json = req.to_dict
                            add_main_req = MainRequestAddition(req)
                            json1 = add_main_req.to_dict_add()
                            json_delete_change.append(json1)

                return JsonResponse({'success': True, 'need_closed': True, 'requests': [],
                                 'new_requests': [],
                                 'changed_requests': [],
                                 'deps_need_closed': deps_need_closed,
                                 'json_delete_change': json_delete_change,
                                 'dt': dt, 'max_rows': row_count})

    deps_queryset = []
    # if not_closed_departure>0:
    #     deps_queryset = model_departure.Departure.objects.filter(end_datetime__isnull=True)
    # print(not_closed_departure)
    list_new_requests = []
    list_changed_request = []
    list_changed_not_in_filter = []
    list_changed_not_in_filter = []
    if first_id != None:
        if first_id.isdigit():
            if int(first_id) > 0:
                list_requests = f.qs.filter(id__lt=first_id)[0:row_count]
            else:
                list_requests = f.qs[0:row_count]
            if dt_input is not None:
                list_new_requests = f.qs.filter(input_datetime__gt=dt_input)
                list_changed_request = f.qs.filter(changed_datetime__gt=dt_input)
                list_changed_not_in_filter = MainRequest.objects.filter(changed_datetime__gt=dt_input)
        else:
            list_requests = f.qs[0:row_count]
    else:
        list_requests = f.qs[0:row_count]

    dt = timezone.now()

    # print('dt_input - ',dt_input)
    json_res = []
    for req in list_requests:
        json = req.to_dict
        add_main_req = MainRequestAddition(req)
        # print(add_main_req.main_request)
        json1 = add_main_req.to_dict_add()
        json_res.append(json1)

        # json_res - yjdsq lkz ghjrhenrb
        # json_new - dyjdm ghtitibt
        # json-change - bpvtybdibtcz#
    # print('-------------------new-requests---------------------------')
    json_new = []
    for req in list_new_requests:
        json = req.to_dict
        add_main_req = MainRequestAddition(req)
        # print(add_main_req.main_request)
        json1 = add_main_req.to_dict_add()
        if not req in list_requests:
            json_new.append(json1)
            # print('append')
    # print('-------------------new-changed---------------------------')
    json_change = []
    for req in list_changed_request:
        json = req.to_dict
        add_main_req = MainRequestAddition(req)
        # print(add_main_req.main_request)
        json1 = add_main_req.to_dict_add()
        if not req in list_requests and not req in list_new_requests:
            json_change.append(json1)
            # print('append')
    if list_changed_not_in_filter.__len__()>0:
        list_changed_not_in_filter = list_changed_not_in_filter.exclude(
            id__in=list_requests.values_list('id', flat=True)).exclude(
            id__in=list_new_requests.values_list('id', flat=True)).exclude(
            id__in=list_changed_request.values_list('id', flat=True))
    json_delete_change = []
    for req in list_changed_not_in_filter:
        json = req.to_dict
        add_main_req = MainRequestAddition(req)
        # print(add_main_req.main_request)
        json1 = add_main_req.to_dict_add()
        json_delete_change.append(json1)

    if f.form.is_valid():
        return JsonResponse({'success': True, 'need_closed': False, 'requests': json_res,
                             'new_requests': json_new,
                             'changed_requests': json_change,
                             'deps_need_closed': [],
                             'json_delete_change': json_delete_change,
                             'dt': dt, 'max_rows': row_count})
    else:
        return JsonResponse({'success': False,
                             'errors': [(k, v[0]) for k, v in f.form.errors.items()]}, safe=False)
        # return render(request, 'test2/parts/request-list/content-json.html',
        #              {'form': f.form, 'list_requests': list_requests, 'rows': row_count,'dt':dt})
        # 'filter': f,
