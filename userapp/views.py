from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views import View

from cart.cartmanager import SessionCartManager
from .models import *
from utils.code import gene_code
from django.core.serializers import serialize


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
    """用户中心"""
    def get(self, request):
        return render(request, "center.html")


class LogoutView(View):
    """退出当前用户"""

    def post(self, request):
        # 删除session中登录用户信息
        if "user" in request.session:
            del request.session["user"]
        return JsonResponse({"delflag": True})


class LoginView(View):
    """登录"""
    def get(self, request):
        # 获取请求参数
        redirect = request.GET.get('redirect', '')
        return render(request, 'login.html', {'redirect': redirect})

    def post(self, request):
        uname = request.POST.get("uname", "")
        pwd = request.POST.get("pwd", "")

        user_list = UserInfo.objects.filter(uname=uname, pwd=pwd)
        if user_list:
            request.session["user"] = user_list[0]
            redirect = request.POST.get('redirect', '')
            if redirect == 'cart':
                # 将session中的购物项移动到数据库
                SessionCartManager(request.session).migrateSession2DB()
                return HttpResponseRedirect("/user/center/")
            elif redirect == 'order':
                return HttpResponseRedirect('/order/order.html?cartitems={}'.format(request.POST.get('cartitems', '')))
            return HttpResponseRedirect('/user/center/')
        return HttpResponseRedirect('/user/login/')


class LoadCodeView(View):
    """生成验证码"""
    def get(self, request):
        img, str_code = gene_code()
        # 将生成的验证码存放到session中
        request.session["sessionCode"] = str_code
        return HttpResponse(img, content_type="image/png")


class CheckCodeView(View):
    """校验验证码"""
    def get(self, request):
        # 获取输入框中的验证码
        code = request.GET.get("code", '')
        # 获取生成的验证码
        session_code = request.session.get("sessionCode", None)
        # 比较输入验证码是否与生成的验证相同
        flag = code == session_code
        return JsonResponse({"flag": flag})


class AddressView(View):

    def get(self, request):
        user = request.session.get("user", "")
        # 获取当前登录用户所有的收货地址
        addr_list = user.address_set.all()
        return render(request, "address.html", {"addrList": addr_list})

    def post(self, request):
        aname = request.POST.get("aname", "")
        aphone = request.POST.get("aphone", "")
        addr = request.POST.get("addr", "")
        user = request.session.get("user", "")

        # 将数据存入数据库
        address = Address.objects.create(aname=aname, aphone=aphone, addr=addr, userinfo=user, isdefault=(lambda count: True if count == 0 else False)(user.address_set.all().count()))
        # 获取当前登录用户所有的收货地址
        addr_list = user.address_set.all()
        return render(request, "address.html", {"addrList": addr_list})


class LoadAreaView(View):

    def get(self, request):
        # 获取请求参数
        pid = request.GET.get("pid", -1)
        pid = int(pid)
        # 根据父id查询区划信息
        area_list = Area.objects.filter(parentid=pid)
        # 进行序列化
        json_area_list = serialize("json", area_list)
        return JsonResponse({"jareaList": json_area_list})











