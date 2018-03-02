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
from django.views.generic.base import TemplateView

#set' object is not reversible keyError :'ru' Еужно во всех url gjcnfdbnm КВАДРАТНЫЕСКОБКИ
urlpatterns = [
     url(r'^$', main_views.home, name='home'),
     url(r'^request/(?P<id_request>\w+)/&', main_views.correct_request, name='correct_request'),
     url(r'^signup/', account_views.signup, name='signup'),
     url(r'^login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
     url(r'^logout/', auth_views.LogoutView.as_view(), name='logout'),
     url(r'^new_request/', main_views.new_request, name='new_request'),
     url(r'^filter_request/', main_views.filter_requests, name='filter_request'),
    # url(r'^base/list-request/', main_views.ListViewRequest.as_view(), name='listview'),
     url(r'^base/filter-request/$',main_views.ListFilterView, name='list_view'),
     url(r'^base/new-request/$',main_views.CreateNewRequest.as_view(), name='base_create_view'),
     url(r'^base/new-request/success/',main_views.new_request_success, name='base_create_view_success'),
     url(r'^base/update-request/(?P<pk>\d+)/$', main_views.UpdateRequest.as_view(), name='base_update_veiw'),
     url(r'^simplle/',main_views.simple, name='view'),
     url(r'^test2/base/',main_views.test_base, name='view'),
     url(r'^test2/filter-request-json/$',main_views.ListFilterJsonView, name='list_json'),
    url(r'^admin/', admin.site.urls),

]
