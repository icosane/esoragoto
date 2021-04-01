from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('graph', views.home, name='home'),
    path('graph2', views.home2, name='home2'),
    path('another', views.another, name='another'),
    path('another2', views.another, name='another2'),
    path('offline', views.offline, name='offline'),
    path('index_n', views.index_n, name='index_n'),
    path('', include('pwa.urls')),
]