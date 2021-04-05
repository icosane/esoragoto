from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ru', views.ru, name='ru'),
    path('offline', views.offline, name='offline'),
    path('graph_n1', views.graph_n1, name='graph_n1'),
    path('graph_n2', views.graph_n2, name='graph_n2'),
    path('graph_n1ru', views.graph_n1ru, name='graph_n1ru'),
    path('graph_n2ru', views.graph_n2ru, name='graph_n2ru'),
    path('', include('pwa.urls')),
]