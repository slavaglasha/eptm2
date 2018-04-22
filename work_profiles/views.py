from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect

# Create your views here.
from work_profiles.forms import UserForm, ProfileForm,NewUserForm
from work_profiles.models import Profile


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
        profile_form = ProfileForm( instance=request.user.profileEptm)
    print(request.user.profileEptm.deparment)
    return render(request, 'user_Change.html', {
        'user_form':user_form,
        'profile_form':profile_form,

        'dd':'dfdfdf'
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
            user.username =userData['username']
            user.first_name = userData['firstname']
            user.last_name =userData['lastname']
            user.email = userData['useremail']

