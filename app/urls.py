from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('history',TestListView.as_view(),name='test_list'),
    path('download/<int:test_id>',download,name='test_download'),

]