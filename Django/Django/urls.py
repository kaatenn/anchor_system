"""Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

import src.views

urlpatterns = [
    path('token', src.views.get_csrf_token),
    path('login', src.views.login),
    path('register', src.views.register),
    path('setBaseInfo', src.views.set_base_info),
    path('getUserInfo', src.views.get_user_info),
    path('updateInfo', src.views.update_user_info),
    path('getEmployedAnchor', src.views.get_employed_anchor)
]
