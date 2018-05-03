from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.db.models import ProtectedError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from work_profiles.forms import UserForm, ProfileForm, NewUserForm, UserCreateFormAdd, UserGroupForm
from work_profiles.models import Profile


@login_required
def ListUsers(request):
    can_save = (request.user.groups.filter(id=1).__len__() > 0)

    return render(request, 'dictionaries/users_list.html', {
        'name_obj': Profile._meta.verbose_name_plural,
        'can_save': can_save
    })


def ListUsersJson(request):
    list_objects = Profile.objects.all().order_by('user__last_name')
    json_res = []
    for obj in list_objects:
        json_res.append(obj.to_dict)
    return JsonResponse({'success': True, 'objects': json_res})


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profileEptm)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))

        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profileEptm)
    print(request.user.profileEptm.deparment)
    return render(request, 'user_Change.html', {
        'user_form': user_form,
        'profile_form': profile_form,

        'dd': 'dfdfdf'
    })


@login_required
@transaction.atomic
def new_profile(request):
    user = User()
    profile = Profile()
    if request.method == 'POST':

        user_form = NewUserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            userData = user_form.cleaned_data()
            user.username = userData['username']
            user.first_name = userData['firstname']
            user.last_name = userData['lastname']
            user.email = userData['useremail']


@login_required
def new_user_Profile(request):
    if request.user.groups.filter(pk=1).__len__() == 0:
        if request.method == 'GET':
            return HttpResponse("У вас нет прав добавлять пользователей")
        else:
            return JsonResponse({'success': False, 'errors': ''})
    user = User()
    if request.method == 'POST':
        form = UserCreateFormAdd(request.POST, instance=user)
        if not (form.is_valid()):
            return JsonResponse({'success': False,
                                 'errors': [(k, v[0]) for k, v in form.errors.items()]}, safe=False)
        else:
            user = form.save()
            print(user.profileEptm.id)

            return JsonResponse({'success': True, 'name': user.username})

    else:
        form = UserCreateFormAdd(instance=user)
        return render(request, 'dictionaries/newUser.html', {'form': form})


@login_required
def update_user_profile_admin(request, pk):
    if request.method == 'POST':
        p = get_object_or_404(Profile, pk=pk)
        profile_form = ProfileForm(request.POST, instance=p)
        user_form = UserForm(request.POST, instance=p.user)
        group_form = UserGroupForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid() and group_form.is_valid():
            user = user_form.save()
            profile_form.save()
            group_id = group_form['group'].value()
            group = Group.objects.get(pk=group_id)
            user.groups.clear()
            print(group)
            user.groups.add(group)
            return JsonResponse({'success': True, 'name': user.username})
        else:
            errors = [(k, v[0]) for k, v in user_form.errors.items()]
            for e in [(k, v[0]) for k, v in profile_form.errors.items()]:
                errors.append(e)
            for e in [(k, v[0]) for k, v in group_form.errors.items()]:
                errors.append(e)
            return JsonResponse({'success': False, 'errors': errors})
    else:
        p = get_object_or_404(Profile, pk=pk)
        user_form = UserForm(instance=p.user)
        profile_form = ProfileForm(instance=p)
        group_id = p.user_group_first_id
        if group_id > 0:
            user_group_form = UserGroupForm(initial={'group': group_id})
        else:
            user_group_form = UserGroupForm(initial={'group': 3})
        print(request.user.profileEptm.deparment)
        return render(request, 'dictionaries/user_update.html', {
            'user_form': user_form,
            'form': profile_form,
            'group_form': user_group_form,
            'name': p.user.username,
            'can_save': (request.user.groups.filter(id=1).__len__() > 0)
        })


def delete_user_profile(request, pk):


    data = dict()
    if request.method == 'POST':
        if request.user.groups.filter(pk=1):
            try:
                d = Profile.objects.get(pk=pk)
                d.user.delete()
                data['success'] = True  # This is just to play along with the existing code
                return JsonResponse(data)
            except ProtectedError:
                data['success'] = False
                data['error_message'] = 'Пользователь в системе'
                return JsonResponse(data)
            except Profile.DoesNotExist:
                data['success'] = False
                data['error_message'] = 'Нет такого пользователя'
                return JsonResponse(data)
            except Exception as e:
                data['success'] = False
                data['error_message'] = 'Ошибка удаления'
                return JsonResponse(data)
        else:
            data['success'] = False
            data['error_message'] = 'У вас нет прав удалять !'
        return JsonResponse(data)
    else:
        d = Profile.objects.get(pk=pk)
        context = {'object': d.name, 'obj_name': d._meta.verbose_name.title}
        return render(request, 'dictionaries/dictionary_delete.html', context)
