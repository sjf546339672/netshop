import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views import View

from cart.cartmanager import getCartManger


class ToOrderView(View):

    def get(self, request):
        # 获取请求参数
        cartitems = request.GET.get("cartitems", "")
        # 判断用户是否登录
        if not request.session.get("user"):
            return render(request, "login.html", {"cartitems": cartitems,
                                                  "redirect": "order"})
        return HttpResponseRedirect("/order/order.html/?cartitems={}".format(cartitems))


class OrderListView(View):

    def get(self, request):
        # 获取请求参数
        cartitems = request.GET.get("cartitems", "")

        # 将json格式字符串转换成python对象(字典{goodsid:1,colorid:1,sizeid:1})列表
        # [ {goodsid:1,colorid:1,sizeid:1}, {goodsid:1,colorid:1,sizeid:1}]
        cart_item_list = json.loads("[" + cartitems + "]")
        print("================================")
        print(cart_item_list)
        print("================================")

        # 将python对象列表转换成CartItem对象列表
        cart_item_obj = [getCartManger(request).get_cartitems(**item) for item in cart_item_list if item]

        # 获取用户的默认收货地址
        address = request.session.get("user").address_set.get(isdefault=True)

        # 获取支付总金额
        total_price = 0
        for cm in cart_item_obj:
            total_price += cm.getTotalPrice()
        return render(request, "order.html", {"cartitemObjList": cart_item_obj,
                                              "address": address,
                                              "totalPrice": total_price})

