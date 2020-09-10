from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views import View
from .models import *
from utils.code import gene_code


class RegisterView(View):

    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        uname = request.POST.get("uname")
        pwd = request.POST.get("pwd")

        # 插入数据到数据库
        user = UserInfo.objects.create(uname=uname, pwd=pwd)
        # 判断是都注册成功
        if user:
            # 将用户信息存储到session中
            request.session["user"] = user
            return HttpResponseRedirect("/user/center/")
        return HttpResponseRedirect("/user/register/")


class CheckUnameView(View):
    """用户名唯一校验"""
    def get(self, request):
        uname = request.GET.get("uname", "")
        user_list = UserInfo.objects.filter(uname=uname)
        flag = False
        if user_list:
            flag = True
        return JsonResponse({"flag": flag})


class CenterView(View):

    def get(self, request):
        return render(request, "center.html")


class LogoutView(View):

    def post(self, request):
        # 删除session中登录用户信息
        if "user" in request.session:
            del request.session["user"]
        return JsonResponse({"delflag": True})


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")


class loadCodeView(View):
    def get(self, request):
        img, str_code = gene_code()
        # 将生成的验证码存放到session中
        request.session["sessionCode"] = str_code

        return HttpResponse(img, content_type="image/png")


class CheckCodeView(View):
    def get(self, request):
        # 获取输入框中的验证码
        code = request.GET.get("code", '')
        # 获取生成的验证码
        session_code = request.session.get("sessionCode", None)
        # 比较输入验证码是否与生成的验证相同
        print("=========", code, session_code, type(code), type(session_code))
        flag = code == session_code
        return JsonResponse({"flag": flag})

