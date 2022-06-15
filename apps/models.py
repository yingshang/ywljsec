from django.db import models

# Create your models here.



class userinfo(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100,default='')
    address = models.TextField(default='')
    money = models.FloatField(default=50000)
    roles = models.CharField(max_length=100,default='普通用户')


class commodityinfo(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    limit = models.IntegerField()

class orderinfo(models.Model):
    username = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address =models.CharField(max_length=100)
    ordererid = models.CharField(max_length=100)
    purchase_amount = models.FloatField(max_length=100)
    purchase_time = models.DateTimeField(auto_now=True)
