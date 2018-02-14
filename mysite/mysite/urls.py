"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^home/', include('home.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^data/', include('data.urls')),
    url(r'^user/login/$', auth_views.login, {'template_name': 'user/login.html'}, name='login'),
    #url(r'^sign_up/$', auth_views.login, {'template_name': 'sign_up/index.html'}, name='sign_up'),
    url(r'^user/logout/$', auth_views.logout, name='logout'),
    #url(r'^', include('home.urls')),

]
