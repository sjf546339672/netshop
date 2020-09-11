# coding: utf-8
from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("checkUname/", views.CheckUnameView.as_view(), name="checkUname"),
    path("center/", views.CenterView.as_view(), name="center"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("loadCode.jpg", views.LoadCodeView.as_view(), name="loadCode"),
    path("checkcode/", views.CheckCodeView.as_view(), name="checkcode"),
    path("address/", views.AddressView.as_view(), name="address"),
    path("loadArea/", views.LoadAreaView.as_view(), name="loadArea"),
]


