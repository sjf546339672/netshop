from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from .cartmanager import *


class AddCartView(View):
    def post(self, request):
        # 在多级字典数据的时候，需要手动设置modified=True，实时地将数据存入到session对象中。
        request.session.modified = True

        # 获取当前操作类型
        flag = request.POST.get("flag", "")

        # 判断当前操作类型
        if flag == "add":
            # 创建cartManager对象
            cart_manager_obj = getCartManger(request)
            # 加入购物车操作
            cart_manager_obj.add(**request.POST.dict())

        elif flag == "plus":
            # 创建cartManager对象
            cart_manager_obj = getCartManger(request)
            # 修改商品数量
            cart_manager_obj.update(step=1, **request.POST.dict())

        elif flag == 'minus':
            # 创建cartManager对象
            cart_manager_obj = getCartManger(request)
            # 修改商品的数量（添加）
            cart_manager_obj.update(step=-1, **request.POST.dict())

        elif flag == 'delete':
            # 创建cartManager对象
            cart_manager_obj = getCartManger(request)
            # 逻辑删除购物车选项
            cart_manager_obj.delete(**request.POST.dict())
        return HttpResponseRedirect("/cart/queryAll/")


class CartListView(View):

    def get(self, request):
        # 创建cartManager对象
        cart_manager_obj = getCartManger(request)
        # 查询所有购物项信息
        cart_list = cart_manager_obj.queryAll()
        return render(request, "cart.html", {"cartList": cart_list})

    def post(self, request):
        pass
