from django.db import models


from django.db import models

class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upasswd = models.CharField(max_length=40)
    uemail = models.CharField(max_length=40,default='')
    ushou = models.CharField(max_length=30,default='')
    uaddress = models.CharField(max_length=200,default='')
    uyoubian = models.CharField(max_length=6,default='')
    uphone = models.CharField(max_length=11,default='')
