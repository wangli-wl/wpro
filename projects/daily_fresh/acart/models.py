#coding=utf-8

from django.db import models

class CartInfo(models.Model):
    cuser = models.ForeignKey('auser.UserInfo')
    cgoods = models.ForeignKey('agoods.GoodsInfo')
    #买了几个什么
    count = models.IntegerField()
