# coding: utf-8
from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path("", views.AddCartView.as_view(), name="cart"),
    path("queryAll/", views.CartListView.as_view(), name="queryAll"),
]











