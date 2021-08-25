import django.contrib.auth.views
from django.urls import path
from . import views

urlpatterns = [
    path('workmode', views.workmode, name ='workmode'),
    path('dtest', views.dtest, name ='dtest'),
    path('dtest5', views.down5,name='down5'),
    path('',views.homepage , name='homepage'),
    path('profil', views.statistics, name='profil'),
    path('speedtest', views.sptest, name='sptest'),
    path('manualspeedtest',views.manualtest, name='manual'),
    path('auto',views.autotest, name='auto'),
    path('result/<int:result_id>', views.resulturl, name="resulturl"),
    path('profil/result/<int:result_id>', views.resulturl, name="resulturl1"),
    path('register', views.register, name='register'),
    path('profil/records', views.records, name='records'),
    path('result/<int:result_id>/edit', views.editrecords, name="editrec"),
    path('profil/result/<int:result_id>/edit', views.editrecords, name="editrec"),
]
