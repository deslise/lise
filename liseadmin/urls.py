from django.conf.urls import url

from liseadmin import views

urlpatterns = [
    url(r'^request_categories/$', views.requestCategories, name='request-categories'),
    url(r'^manage_categories/$', views.manageCategories, name='manage-categories'),
    url(r'^manage_plan/$', views.managePlan, name='manage-plan'),
    url(r'^manage_data/$', views.manageData, name='manage-data'),
    url(r'^new_items/$', views.newItems, name='new-items'),
    url(r'^update_data/$', views.updateData, name='update-data'),
    url(r'^manage_topics/$', views.manageTopics, name='manage-topics'),
    url(r'^recusar_item/(?P<item_id>[\d]+)/$', views.recusarItem, name='recusar-item'),
    url(r'^state_request/(?P<req_id>[\d]+)/(?P<state>.*)$', views.setStateRequest, name='state-request'),
]