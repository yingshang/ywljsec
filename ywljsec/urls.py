"""ywljsec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from apps.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index,name="index"),
    path('init_data/', init_data,name='init_data'),
    path('shopping/', shopping,name='shopping'),
    path('msg_code/', msg_code,name='msg_code'),
    path('register/', register,name='register'),
    path('unauthorized_access/', unauthorized_access,name='unauthorized_access'),

]
