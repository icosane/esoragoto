from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ru', views.ru, name='ru'),
    path('graph', views.home, name='home'),
    path('graph2', views.home2, name='home2'),
    path('another', views.another, name='another'),
    path('another2', views.another, name='another2'),
    path('offline', views.offline, name='offline'),
    path('graph_n1', views.graph_n1, name='graph_n1'),
    path('graph_n11', views.graph_n11, name='graph_n11'),
    path('graph_n2', views.graph_n2, name='graph_n2'),
    path('', include('pwa.urls')),
]