from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
import json
from django.db import transaction
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from departures.forms import DeparturesFormSet, CustomDepartureFormSet
from .models import MainRequest
from .forms import newMainRequestForm, filterForm, updateMainRequestForm
from work_profiles.models import Profile
from .filter import MainRequestFilter

import  main_requests.JSONEncoder


# Create your views here.
# @login_required
@login_required
def home(request):
    dt = timezone.now().__add__(timedelta(days=-5))
    form = filterForm(initial={'input_dateTime_start': dt,
                               'input_dateTime_end': '',
                               'input_user': '',
                               'request_user': '',
                               'request_outer_user': '',
                               'request_dateTime_start': '',
                               'request_dateTime_end': '',
                               'receive_user': '',
                               'receive_dateTime_start': '',
                               'receive_dateTime_end': '',
                               'close_user': '',
                               'close_dateTime_start': '',
                               'close_dateTime_end': ''
                               })

    requests = MainRequest.objects.all().filter(input_datetime__gte=dt).order_by('-pk')
    return render(request, 'home.html', {'main_requests': requests, 'form': form})


@login_required
def new_request(request):
    print(request.POST)
    if request.method == 'POST':
        form = newMainRequestForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            user = request.user
            new_request.input_user = Profile.objects.get(user=user)
            old_number = MainRequest.objects.all().aggregate(Max('number'))

            new_request.number = old_number['number__max'] + 1
            if new_request.request_user is not None:
                new_request.request_outer_status = None
                new_request.request_outer_department = None

            new_request.save()
            return HttpResponse("Success")
        else:
            return render(request, 'new_request.html', {'form': form})
    else:
        form = newMainRequestForm()
    profiles = Profile.objects.all()
    return render(request, 'new_request.html', {'form': form, "profiles": profiles})


def getfilterRequests(filterForm):
    requsts = requests = MainRequest.objects.all()
    if filterForm.data.get('input_dateTime_start') != '':
        requests = requests.filter(input_datetime__gte=filterForm.cleaned_data['input_dateTime_start'])
    if filterForm.data.get('input_dateTime_end') != '':
        requests = requests.filter(input_datetime__lte=filterForm.cleaned_data['input_dateTime_end'])
    if filterForm.data.get('input_user') != '':
        requests = requests.filter(input_user=filterForm.cleaned_data['input_user'])

    if filterForm.data.get('request_dateTime_start') != '':
        requests = requests.filter(request_dateTime__gte=filterForm.cleaned_data['request_dateTime_start'])
    if filterForm.data.get('request_dateTime_end') != '':
        requests = requests.filter(request_dateTime__lte=filterForm.cleaned_data['request_dateTime_end'])
    if filterForm.data.get('request_user') != '':
        requests = requests.filter(request_user=filterForm.cleaned_data['request_user'])
    if filterForm.data.get('request_outer_user') != '':
        requests = requests.filter(request_outer_User=filterForm.cleaned_data['request_outer_user'])
    if filterForm.data.get('place') != '':
        requests = requests.filter(place=filterForm.cleaned_data['place'])
    return requests


@login_required
def filter_requests(request):
    if request.method == 'GET':
        form = filterForm(request.GET or None)
        print(form.data.get('request_user'))
        requests = MainRequest.objects.all()

        if form.is_valid():
            requests = getfilterRequests(form)
            requests = requests.order_by('-pk')
            return render(request, 'home-content.html', {'main_requests': requests})
        else:
            print((form.errors))
            return render(request, 'includes/filterform.html', {'form': form})
    else:
        form = filterForm()
        return render(request, 'includes/filterform.html', {'form': form})


@login_required
def correct_request(request, id_request):
    if request.method == 'GET':
        mainRequestObject = MainRequest.objects.get(id=id_request)
        if mainRequestObject.request_outer_status is None:
            mainRequestObject.request_outer_status = Profile.objects.get(
                id=mainRequestObject.request_user.id).user_position
        if mainRequestObject.request_outer_department is None:
            mainRequestObject.request_outer_department = Profile.objects.get(
                id=mainRequestObject.request_user.id).deparment.name
        user = request.user
        form_request = updateMainRequestForm(None, instance=mainRequestObject)
        groups = user.groups.all().values_list('id', flat=True)
        enableReceive = False
        if 2 in groups:  # исполнители
            form_request.fields['receive_user'].widget.attrs['disabled'] = True

            if mainRequestObject.input_user.user != user:
                form_request.fields['request_user'].widget.attrs['disabled'] = True
                form_request.fields['request_outer_User'].widget.attrs['disabled'] = True
                form_request.fields['request_outer_status'].widget.attrs['disabled'] = True
                form_request.fields['request_outer_department'].widget.attrs['disabled'] = True
                form_request.fields['request_dateTime'].widget.attrs['disabled'] = True
                form_request.fields['place'].widget.attrs['disabled'] = True
                form_request.fields['about'].widget.attrs['disabled'] = True
                form_request.fields['place'].widget.attrs['disabled'] = True
            if mainRequestObject.receive_user is None:
                enableReceive = True
        else:
            if not (1 in groups):

                if mainRequestObject.input_user.user != user:
                    for field in form_request.fields:
                        print(field)
                        form_request.fields[field].widget.attrs['disabled'] = True


                else:
                    form_request.fields['receive_user'].widget.attrs['disabled'] = True
                    form_request.fields['receive_dateTime'].widget.attrs['disabled'] = True
                    form_request.fields['close_user'].widget.attrs['disabled'] = True
                    form_request.fields['close_dateTime'].widget.attrs['disabled'] = True
        profiles = Profile.objects.all()
        return render(request, 'correct_request.html',
                      {'form': form_request, 'pk': id_request, 'number': mainRequestObject.number, 'profiles': profiles,
                       'enableReceive': enableReceive})
    if request.method == "POST":
        mainRequestObject = MainRequest.objects.get(id=id_request)
        form_request = updateMainRequestForm(request.POST or None, instance=mainRequestObject)
        if form_request.is_valid():
            form_new_request = form_request.save(commit=False)
            form_new_request.save()
            return HttpResponse("Success")
        else:
            return HttpResponse(form_request.errors.as_json(escape_html=True),
                                content_type="application/json")


# Base view
@login_required
class ListViewRequest(ListView):
    model = MainRequest
    context_object_name = 'main_requests'
    template_name = 'baseviews/requests_list.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Декорируем диспетчер функцией login_required, чтобы запретить просмотр отображения неавторизованными
        пользователями
        """
        return super(ListViewRequest, self).dispatch(request, *args, **kwargs)


# filter
@login_required
def ListFilterView(request):
    dt = timezone.now().__add__(timedelta(days=-5))


    f = MainRequestFilter(request.GET, queryset=MainRequest.objects.all().order_by('-pk'))

    row_count = request.GET.get('col-row')
    if row_count == None:
        row_count = 10
    print(row_count)
    paginator = Paginator(f.qs, row_count)
    page = request.GET.get('page', 1)
    print(page)



    try:
        list_requests = paginator.page(page)
    except PageNotAnInteger:
        list_requests = paginator.page(1)
    except EmptyPage:
        list_requests = paginator.page(paginator.num_pages)

    return render(request, 'baseviews/requests_list.html',
                  { 'form': f.form, 'list_requests': list_requests, 'rows': row_count})
    #'filter': f,

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

    def get_context_data(self, **kwargs):
        profiles = Profile.objects.all()
        data = super(CreateNewRequest, self).get_context_data(**kwargs)
        data['profiles'] = profiles
        return data

    def get_success_url(self):
        print(self.request.META['HTTP_REFERER'])
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
        return render(self.request,'baseviews/new_request/success_new_request.html', {'number':new_request.number})
        #return super().form_valid(form)

def new_request_success(request):
    return render(request, 'baseviews/new_request/success_new_request.html')


class UpdateRequest(UpdateView):# изменеие формы заявок
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
        
        if self.request.POST:
            data['departures'] = CustomDepartureFormSet(self.request.POST, instance=self.object, dep_user = self.request.user )
        else:
            data['departures'] = CustomDepartureFormSet(instance=self.object, dep_user = self.request.user)
        return data




    def form_valid(self, form):
        context = self.get_context_data()
        departures = context['departures']
        # try to delete object before valid



        if form.is_valid():
            print("Form valid")
            for dep in departures.forms:
                if dep in departures.deleted_forms:
                    print("Delete")
            if departures.is_valid():
                print( "deparures valid")
                with transaction.atomic(): # что это за  хрень?
                    self.object = form.save()
                    departures.instance = self.object
                    for formdep in departures.forms:
                        departure = formdep.save(commit=False)
                        departure.input_user = Profile.objects.get(user=self.request.user)
                departures.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                return self.render_to_response(self.get_context_data(form=form,
                                                                     departures=departures))


    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form = form))

# для тестов
@login_required
def test_base(request):
    return render(request, 'test2/request-list.html')

# фильтр json
# filter
@login_required
def ListFilterJsonView(request):

    get_form = request.GET.get("get_form")
    if get_form is not None:
        if get_form:
            f = MainRequestFilter(request.GET, queryset=MainRequest.objects.all().order_by('-pk')[0:1])
            return render(request,'includes/filter/filter_modal_form.html',{'form':f.form})

    dt = timezone.now()
    first_id=request.GET.get('first_id')
    row_count = 20
    if first_id == None:
        f = MainRequestFilter(request.GET, queryset=MainRequest.objects.all().order_by('-pk'))
    else:
        f = MainRequestFilter(request.GET,
                              queryset=MainRequest.objects.all().order_by('-pk'))

    if first_id == None:
        list_requests = f.qs[0:row_count]
    else:
        list_requests = f.qs.filter('id_lt', first_id)[0:row_count]



    dt = timezone.now()
    list = f.qs
    json_res=[]
    for req in list_requests:

        json = req.to_dict()
        json_res.append(json)


    if f.form.is_valid():
         return JsonResponse({'success': True,'requests':json_res,'dt':dt,'max_rows':row_count})
    else:
        return JsonResponse({'success': False,
                      'errors': [(k, v[0]) for k, v in f.form.errors.items()]}, safe=False)
   # return render(request, 'test2/parts/request-list/content-json.html',
    #              {'form': f.form, 'list_requests': list_requests, 'rows': row_count,'dt':dt})
    # 'filter': f,

