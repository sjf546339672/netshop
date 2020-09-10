from django.db import models


class Category(models.Model):
    """商品类别"""
    cname = models.CharField(max_length=30)

    def __str__(self):
        return u"Category: {}".format(self.cname)


class Goods(models.Model):
    """商品"""
    gname = models.CharField(max_length=100)  # 商品名称
    gdesc = models.CharField(max_length=100)  # 商品描述
    oldprice = models.DecimalField(max_digits=5, decimal_places=2)  # 旧的价格
    price = models.DecimalField(max_digits=6, decimal_places=2)  # 现价
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return u"Goods: {}".format(self.gname)

    def getGoodImg(self):
        """通过库存获取到color第一个对象再获取到Img"""
        return self.inventory_set.first().color.colorurl

    def getGoodColorList(self):
        """获取所有的颜色"""
        color_list = []
        for inventory in self.inventory_set.all():
            color = inventory.color
            if color not in color_list:
                color_list.append(color)
        return color_list

    def getGoodSizeList(self):
        size_list = []
        for inventory in self.inventory_set.all():
            size = inventory.size
            if size not in size_list:
                size_list.append(size)
        return size_list

    def getGoodDetailList(self):
        import collections
        datas = collections.OrderedDict()
        for gooddetail in self.goodsdetail_set.all():
            gdname = gooddetail.getGoodname()
            if gdname not in datas:
                datas[gdname] = [gooddetail.gdurl]
            else:
                datas[gdname].append(gooddetail.gdurl)
        return datas


class GoodsDetailName(models.Model):
    gdname = models.CharField(max_length=30)

    def __str__(self):
        return u"GoodsDetailName: {}".format(self.gdname)


class GoodsDetail(models.Model):
    gdurl = models.ImageField(upload_to="")
    gdname = models.ForeignKey(GoodsDetailName, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)

    def getGoodname(self):
        return self.gdname.gdname


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



