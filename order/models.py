from django.db import models

from userapp.models import Address, UserInfo


class Order(models.Model):
    out_trade_num = models.UUIDField()  # 交易编码
    order_num = models.CharField(max_length=100)  # 订单编号
    trade_no = models.CharField(max_length=120)  # 支付成功后生成的编号
    status = models.CharField(max_length=20, default="待支付")  # 支付状态
    payway = models.CharField(max_length=20, default="alipay")  # 支付方式
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)


class OrderItem(models.Model):
    goodsid = models.PositiveIntegerField()
    colorid = models.PositiveIntegerField()
    sizeid = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)


