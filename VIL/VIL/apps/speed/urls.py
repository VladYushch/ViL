from django.urls import path

from . import views

urlpatterns = [
    path('', views.sptest, name ='sptest'),
    path('dtest', views.dtest, name ='dtest')
]
