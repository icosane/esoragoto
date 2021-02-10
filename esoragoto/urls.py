from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('another', views.another, TemplateView.as_view(template_name='another.html'), name='another'),
]