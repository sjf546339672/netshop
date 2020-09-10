# coding: utf-8
from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("category/<str:category_id>/", views.IndexView.as_view()),
    path("category/<str:category_id>/page/<str:num>/", views.IndexView.as_view()),
    path("goodsdetails/<str:goods_id>/", views.DetailView.as_view()),
]
