#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.staticfiles import views as static_views
from django.conf.urls.static import static
from django.conf import settings

import library.views as views

urlpatterns = [
                  url(r'^$', views.index, name='index'),
                  url(r'^login/', views.user_login, name='user_login'),
                  url(r'^logout/', views.user_logout, name='user_logout'),
                  url(r'^register/', views.user_register, name='user_register'),
                  url(r'^set_password/', views.set_password, name='set_password'),
                  url(r'^profile/', views.profile, name='profile'),
                  url(r'^mission/', views.mission, name='mission'),
                  url(r'^detail$', views.mission_detail, name='mission_detail'),
                  url(r'^check/$', views.check, name='check'),
                  url(r'^proof/$', views.proof, name='proof'),
                  url(r'^myissue/', views.myissue, name='myissue'),
                  url(r'^mymission/', views.mymission, name='mymission'),
                  url(r'^myaudit/', views.myaudit, name='myaudit'),
                  url(r'^share/', views.share, name='share'),
                  url(r'^backstage/', views.backstage, name='backstage'),
                  url(r'^backstage_login/', views.backstage_login, name='backstage_login'),
                  url(r'^admin_alter/', views.admin_alter, name='admin_alter'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
