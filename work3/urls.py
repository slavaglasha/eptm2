"""work3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from main_requests import views as main_views
from account import views as account_views
from work_profiles import views as profile_view
from departments import views as departments_view
from places import views as places_view
# from django.views.generic.base import TemplateView

# set' object is not reversible keyError :'ru' Еужно во всех url gjcnfdbnm КВАДРАТНЫЕСКОБКИ
urlpatterns = [

    url(r'^signup/', account_views.signup, name='signup'),
    url(r'^login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/', auth_views.LogoutView.as_view(template_name='simple.html'), name='logout'),

    url(r'^user-change/', profile_view.update_profile, name='update_profile'),

    url(r'^base/new-request/$', main_views.CreateNewRequest.as_view(), name='base_create_view'),
    url(r'^base/new-request/success/', main_views.new_request_success, name='base_create_view_success'),
    url(r'^base/update-request/(?P<pk>\d+)/$', main_views.UpdateRequest.as_view(), name='base_update_veiw'),
    url(r'^simplle/', main_views.simple, name='views'),

    url(r'^test2/filter-request-json/$', main_views.ListFilterJsonView, name='list_json'),
    url(r'^admin/', admin.site.urls),

    url(r'^dictionaries/departments/$', departments_view.ListDepartment, name='dictionary_department'),
    url(r'^dictionaries/departments-list-json/$', departments_view.ListDepartmentJson, name='department_list_json'),
    url(r'^dictionaries/departments-new/$', departments_view.CreateNewDepartment.as_view(),
        name='department_create_view'),
    url(r'^dictionaries/departments-update/(?P<pk>\d+)/$', departments_view.UpdateDepartment.as_view(),
        name='department_update_view'),
    url(r'^dictionaries/department-delete/(?P<pk>\d+)/$', departments_view.Deartmen_delete,
        name='department_delete_view'),

    url(r'^dictionaries/places/$', places_view.ListPlaces, name='dictionary_places'),
    url(r'^dictionaries/places-list-json/$', places_view.ListPlacesJson, name='places_list_json'),
    url(r'^dictionaries/places-new/$', places_view.CreateNewPlaces.as_view(),
        name='places_create_view'),
    url(r'^dictionaries/places-update/(?P<pk>\d+)/$', places_view.UpdatePlaces.as_view(),
        name='places_update_view'),
    url(r'^dictionaries/places-delete/(?P<pk>\d+)/$', places_view.Places_delete,
        name='places_delete_view'),

    url(r'^test2/base/', main_views.test_base, name='view'),
    url(r'^$', main_views.test_base, name='view'),

]
