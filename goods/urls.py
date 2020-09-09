# coding: utf-8
from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_views(), name="index")
]
