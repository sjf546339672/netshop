# coding: utf-8
from django.urls import path
from . import views

urlpatterns = [
    path("", views.ToOrderView.as_view(), name="order"),
    path("order.html/", views.OrderListView.as_view(), name="order"),
]


