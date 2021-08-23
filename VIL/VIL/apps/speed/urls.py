import django.contrib.auth.views
from django.urls import path
from . import views

urlpatterns = [
    path('workmode', views.workmode, name ='workmode'),
    path('dtest', views.dtest, name ='dtest'),
    path('dtest5', views.down5,name='down5'),
    path('',views.homepage , name='homepage'),
    path('customer', views.historyprint, name='history'),
    path('speedtest', views.sptest, name='sptest'),
    path('manualspeedtest',views.manualtest, name='manual'),
    path('auto',views.autotest, name='auto')
]
