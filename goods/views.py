import math

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from goods.models import *


class IndexView(View):

    def get(self, request, category_id=1, num=1):
        category_id = int(category_id)
        num = int(num)
        # 查询所有类别数据
        category_list = Category.objects.all().order_by("id")
        # 查询当前类别下的所有商品信息
        good_list = Goods.objects.filter(category_id=category_id).order_by("id")

        # 分页
        # 创建分页器对象
        paginator = Paginator(good_list, 8)
        # 获取当前页的数据
        page_good_list = paginator.page(num)

        # 生成分页页码数列表
        # 每页开始页码
        begin_page = (num-int(math.ceil(10.0/2)))  # 10  6
        if begin_page < 1:
            begin_page = 1

        # 每页结束页码
        end_page = begin_page + 9
        if end_page > paginator.num_pages:
            end_page = paginator.num_pages

        if end_page < 10:
            begin_page = 1
        else:
            begin_page = end_page - 9

        page_list = range(begin_page, end_page + 1)

        return render(request, "index.html", {"category_list": category_list,
                                              "good_list": page_good_list,
                                              "currentCid": category_id,
                                              "page_list": page_list,
                                              "currentNum": num})


def recomend_view(func):
    def wrapper(detailView, request, goods_id, *args, **kwargs):
        # 将存放在cookie中的goodsId获取
        cookie_str = request.COOKIES.get('recommend', '')
        print("===============================", cookie_str)

        # 存放所有goodsid的列表
        goodsIdList = [gid for gid in cookie_str.split() if gid.strip()]

        # 思考1：最终需要获取的推荐商品
        goodsObjList = [Goods.objects.get(id=gsid) for gsid in goodsIdList if gsid!=goods_id and Goods.objects.get(id=gsid).category_id == Goods.objects.get(id=goods_id).category_id][:4]

        # 将goodsObjList传递给get方法
        response = func(detailView, request, goods_id, goodsObjList, *args, **kwargs)

        # 判断goodsid是否存在goodsIdList中
        if goods_id in goodsIdList:
            goodsIdList.remove(goods_id)
            goodsIdList.insert(0, goods_id)
        else:
            goodsIdList.insert(0, goods_id)

        # 将goodsIdList中的数据保存到Cookie中
        response.set_cookie('recommend', ' '.join(goodsIdList), max_age=3*24*60*60)
        return response
    return wrapper


class DetailView(View):

    @recomend_view
    def get(self, request, goods_id, recommend_list=[]):
        goods_id = int(goods_id)
        # 根据goods_id查询商品信息(goods对象)
        detail_good = Goods.objects.get(id=goods_id)
        return render(request, "detail.html", {"detail_good": detail_good, "recommend_list": recommend_list})



