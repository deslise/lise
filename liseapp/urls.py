from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf.urls import *
from django.template.response import TemplateResponse

from liseapp import views



urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^perfil$', views.myAccountDetails, name='my-account-details'),
    url(r'^plan/(?P<plan_id>\d+)$', views.dashboardDetails, name='dashboard-details'),
    url(r'^plan/(?P<plan_id>\d+)/toptopics$', views.topTopics, name='top-topics'),
    url(r'^plan/(?P<plan_id>\d+)/polaritytopics$', views.polarityTopics, name='polarity-topics'),
    url(r'^plan/(?P<plan_id>\d+)/operatingdays$', views.operatingDays, name='operating-days'),
    url(r'^plan/(?P<plan_id>\d+)/operatinghours$', views.operatingHours, name='operating-hours'),
    url(r'^plan/(?P<plan_id>\d+)/competitionregions$', views.competitionRegions, name='competition-regions'),
    url(r'^plan/(?P<plan_id>\d+)/rankingbusiness$', views.rankingBusiness, name='ranking-business'),
    url(r'^plan/(?P<plan_id>\d+)/sublocations$', views.sublocations, name='sublocations'),
    url(r'^plan/(?P<plan_id>\d+)/competitoropinions$', views.competitorOpinions, name='competitor-opinions'),
    url(r'^plan/(?P<plan_id>\d+)/meanscontact$', views.meansContact, name='means-contact'),
    url(r'^plan/register$', views.registerPlan, name='register-plan'),
    url(r'^plan/delete/(?P<plan_id>\d+)$', views.deletePlan, name='delete-plan'),
    url(r'^notifications/$', views.pageNotifications, name='notifications'),
    url(r'^notifications/(?P<pk>\d+)$', views.pageNotifications, name='notifications'),
    url(r'^plan/edit/(?P<plan_id>\d+)$', views.editPlan, name='edit-plan'),
    url(r'^login/$', auth_views.login, {'template_name': 'sign-in.html'}, name='signin'),
    url(r'^signup$', views.signUp, name='signup'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'liseapp:signin'}, name='logout'),
    url(r'^changepassword/$', views.changePassword, name='change-password'),
    url(r'^forgotpassword/$', views.forgotPassword, name='forgot-password'),
    url(r'^noaccess/$', views.noAccess, name='no-access'),
]


if settings.DEBUG:
    urlpatterns += [url(r'^', TemplateResponse, {'template':'404.html'})]
