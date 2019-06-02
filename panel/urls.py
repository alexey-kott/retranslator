from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^sign-up/$', views.sign_up, name='sign_up'),
    re_path(r'^sign-in/$', views.sign_in, name='sign_in'),
    re_path(r'^sign-out/$', views.sign_out, name='sign_out'),
    ]
