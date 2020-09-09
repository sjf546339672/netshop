from django.db import models


class Category(models.Model):
    """商品类别"""
    cname = models.CharField(max_length=30)

    def __str__(self):
        return u"Category: {}".format(self.cname)


class Goods(models.Model):
    """商品"""
    gname = models.CharField(max_length=100)
    gdesc = models.CharField(max_length=100)
    oldprice = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return u"Goods: {}".format(self.gname)


class GoodsDetailName(models.Model):
    gdname = models.CharField(max_length=30)

    def __str__(self):
        return u"GoodsDetailName: {}".format(self.gdname)


class GoodsDetail(models.Model):
    gdurl = models.ImageField(upload_to="")
    gdname = models.ForeignKey(GoodsDetailName, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)


class Size(models.Model):
    sname = models.CharField(max_length=30)

    def __str__(self):
        return u"Size: {}".format(self.sname)


class Color(models.Model):
    colorname = models.CharField(max_length=30)
    colorurl = models.ImageField(upload_to="color/")

    def __str__(self):
        return u"Color: {}".format(self.colorname)


class Inventory(models.Model):  # 库存
    count = models.PositiveIntegerField()
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)



