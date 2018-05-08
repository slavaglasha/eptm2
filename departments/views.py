from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.generic import CreateView, UpdateView
from departments.forms import DepartmentForm
from departments.models import department




class AuthenticatedMixin(object):
        def dispatch(self, request, *args, **kwargs):
            if not request.user.is_authenticated():
                return HttpResponseForbidden()
            return super(AuthenticatedMixin, self).dispatch(request, *args, **kwargs)


# для тестов
@login_required
def ListDepartment(request):
    can_save = (request.user.groups.filter(id=1).__len__() > 0)

    return render(request, 'dictionaries/departments_list.html', {
        'name_obj': department._meta.verbose_name_plural,
        'can_save': can_save
    })


def ListDepartmentJson(request):
    list_objects = department.objects.all().order_by('name')
    json_res = []
    for obj in list_objects:
        json_res.append(obj.to_dict)
    return JsonResponse({'success': True, 'objects': json_res})


# создание нового обьекта
class CreateNewDepartment(AuthenticatedMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = '/base/filter-request/'
    form_class = DepartmentForm
    template_name = 'dictionaries/new_dictionary.html'
    success_url = 'dictionaries/new_dictionary.html'

    # def get_form_kwargs(self):
    #     kwargs = super(CreateNewDepartment, self).get_form_kwargs()
    #     user = self.request.user
    #     prof = Profile.objects.get(user=user)
    #     initial = kwargs.pop('initial')
    #     initial.update({'request_user': prof})
    #     kwargs.update({'initial': initial})
    #     print(kwargs)
    #
    #     # kwargs.update({'request_outer_department': dep})
    #     # kwargs.update({'request_outer_status': position})
    #     return kwargs

    def get_success_url(self):
        print(self.request.META['HTTP_REFERER'])
        return redirect('base_create_view_success', number=1)

    def form_valid(self, form):
        new_department = form.save(commit=False)
        name = new_department.name

        new_department.save()
        return JsonResponse({'success': True,
                             'name': name})
        # return render(self.request,'baseviews/new_request/success_new_request.html', {'number':new_request.number})
        # return super().form_valid(form)

    def form_invalid(self, form):
        return JsonResponse({'success': False,
                             'errors': [(k, v[0]) for k, v in form.errors.items()]})

        # изменеие формы заявок


class UpdateDepartment(UpdateView, ):
    form_class = DepartmentForm
    model = department
    template_name = 'dictionaries/dictionary_update.html'
    success_url = '/simplle/'

    # def get_form_kwargs(self):
    #     kwargs = super(UpdateRequest, self).get_form_kwargs()
    #     kwargs.update({'place_user': self.request.user})
    #
    #     return kwargs

    def get_context_data(self, **kwargs):
        data = super(UpdateDepartment, self).get_context_data(**kwargs)
        # profiles = Profile.objects.all()
        # data['profiles'] = profiles
        # if self.request.POST:
        #     data['departures'] = CustomDepartureFormSet(self.request.POST, instance=self.object,
        #                                                 dep_user=self.request.user)
        # else:
        #     data['departures'] = CustomDepartureFormSet(instance=self.object, dep_user=self.request.user)

        data['can_save'] = (self.request.user.groups.filter(id=1).__len__() > 0)

        return data

    def form_valid(self, form):
        if form.is_valid():
            # for dep in departures.forms:
            #     print('dep obj')
            #     if dep in departures.deleted_forms:
            #         print("Delete")
            self.object = form.save()
            return JsonResponse({'success': True, 'name': form.instance.name})

    def form_invalid(self, form):
        return JsonResponse({'success': False,
                             'errors': [(k, v[0]) for k, v in form.errors.items()]}, safe=False)


def Deartmen_delete(request, pk):
    d = get_object_or_404(department, pk=pk)

    data = dict()
    if request.method == 'POST':
        if request.user.groups.filter(pk=1):
            d.delete()
            data['success'] = True  # This is just to play along with the existing code
            return JsonResponse(data)
        else:
            data['success'] = False
            data['error_message'] = 'У вас нет прав удалять !'
        return JsonResponse(data)
    else:
        context = {'object': d.name, 'obj_name': d._meta.verbose_name.title}
        return render(request, 'dictionaries/dictionary_delete.html', context)

        # class DeleteDepartmetn(DeleteView):
        #    model = department
        #    template_name = 'dictionaries/dictionary_delete.html'
        #    success_url = '/simplle/'#

        # def get_object(self, queryset=None):
        #   obj = super(DeleteDepartmetn, self).get_object()
        #   print("Delete ", obj)
        #   return obj

        #  def delete(self, request, *args, **kwargs):
        #      self.get_object().delete()
        #      return JsonResponse({'success': True})
