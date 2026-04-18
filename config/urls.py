"""config URL Configuration

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
import links.views as views


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.index, name='index'),
    path('create/', views.create_short_url, name='create_short_url'),
    path('login/', views.user_login, name='user_login'),
    path('register/', views.user_register, name='user_register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('auth/google', views.login_google, name='login_google'),
    path('auth/google/callback', views.google_callback, name='google_callback'),
    path('stats/', views.stats, name='stats'),
    path('test-error/', views.test_error, name='test-error'),
    path('search/', views.search, name='search'),

    path('delete/<int:pk>', views.link_delete, name='link_delete'),
    path('copy/<int:pk>', views.link_copy, name='link_copy'),
    path('<str:code>/', views.redirect_url, name='redirect_url')
]
