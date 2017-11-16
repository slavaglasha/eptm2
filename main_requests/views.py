from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Max
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import MainRequest
from .forms import newMainRequestForm, filterForm
from work_profiles.models import Profile


# Create your views here.
# @login_required
@login_required
def home(request):
    requests = MainRequest.objects.all()
    requests=requests.order_by('-pk')
    form = filterForm()
    return render(request, 'home.html', {'main_requests': requests, 'form': form})


def new_request(request):
    print(request.POST)
    if request.method == 'POST':
        form = newMainRequestForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            user = User.objects.first()
            new_request.input_user = Profile.objects.get(user=user)
            old_number = MainRequest.objects.all().aggregate(Max('number'))

            new_request.number = old_number['number__max'] + 1
            new_request.save()
            return render(request, 'new_request.html', {'form': form})
    else:
        form = newMainRequestForm()
    return render(request, 'new_request.html', {'form': form})


def filter_requests(request):

    if request.method == 'POST':
        form = filterForm(request.POST or None)
        requests = MainRequest.objects.all()


        if form.is_valid():

            if request.POST.get('input_dateTime_start') != '':
                requests = requests.filter(input_datetime__gte=form.cleaned_data['input_dateTime_start'])
            if request.POST.get('input_dateTime_end') != '':
                requests = requests.filter(input_datetime__lte=form.cleaned_data['input_dateTime_end'])
            if request.POST.get('input_user') != '':
                requests = requests.filter(receive_user=form.cleaned_data['input_user'])

            if request.POST.get('request_dateTime_start') != '':
                requests = requests.filter(request_dateTime__gte=form.cleaned_data['request_dateTime_start'])
            if request.POST.get('input_dateTime_end') != '':
                requests = requests.filter(request_dateTime__lte=form.cleaned_data['request_dateTime_end'])
            if request.POST.get('receive_user') != '':
                requests = requests.filter(request_user=form.cleaned_data['request_user'])

            if request.POST.get('receive_dateTime_start') != '':
                requests = requests.filter(receive_dateTime__gte=form.cleaned_data['receive_dateTime_start'])
            if request.POST.get('receive_dateTime_end') != '':
                requests = requests.filter(receive_dateTime__lte=form.cleaned_data['receive_dateTime_end'])
            if request.POST.get('receive_user') != '':
                requests = requests.filter(receive_user=form.cleaned_data['receive_user'])

            if request.POST.get('close_dateTime_start') != '':
                requests = requests.filter(close_dateTime__gte=form.cleaned_data['close_dateTime_start'])
            if request.POST.get('close_dateTime_end') != '':
                requests = requests.filter(close_dateTime__lte=form.cleaned_data['close_dateTime_end'])
            if request.POST.get('close_user') != '':
                requests = requests.filter(close_user=form.cleaned_data['close_user'])

            return render(request, 'home-content.html', {'main_requests': requests})
        else:
            print((form.errors))
            return render(request, 'includes/filterform.html', {'form': form})
    else:
        form = filterForm()
        return render(request, 'includes/filterform.html', {'form': form})
