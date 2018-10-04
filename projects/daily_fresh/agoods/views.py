#coding=utf-8

from django.shortcuts import render
from auser import user_decrator
from auser.models import *

def islogin(request, title):
    if request.session.has_key('user_id'):
        id = request.session['user_id']
        user = UserInfo.objects.filter(id=id)
        uname = user[0].uname
        context = {'title': title,'uname':uname}
    else:
        context = {'title': title,'uname':''}
    return context

def index(request):
    context = islogin(request, '商品首页')
    return render(request, 'agoods/index.html', context)

def list(request):
    context = islogin(request, '商品列表')
    return render(request, 'agoods/list.html', context)

def detail(request):
    context = islogin(request, '商品详情')
    return render(request, 'agoods/detail.html', context)

@user_decrator.login
def cart(request):
    context = islogin(request)
    return render(request, 'agoods/cart.html', context)