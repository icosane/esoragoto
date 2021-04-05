"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from esoragoto import views
#from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index, name='index'),
    path('ru', views.ru, name='ru'),
    path('offline', views.offline, name='offline'),
    path('graph_n1', views.graph_n1, name='graph_n1'),
    path('graph_n2', views.graph_n2, name='graph_n2'),
    path('', include('pwa.urls')),
    #path('admin/', admin.site.urls),
]
