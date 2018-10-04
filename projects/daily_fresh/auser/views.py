#coding=utf-8

from django.shortcuts import render, redirect
from auser.models import *
from django.http import JsonResponse, HttpResponseRedirect
from hashlib import sha1
import user_decrator

def register(request):
    return render(request, 'auser/register.html')

def register_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upasswd = post.get('pwd')
    upasswd_c = post.get('cpwd')
    uemail = post.get('email')
    if upasswd!=upasswd_c:
        context = {'title':'注册'}
        return render(request, 'auser/register.html', context)
    userinfo = UserInfo()
    userinfo.uname = uname
    s1 = sha1()
    s1.update(upasswd)
    upasswd = s1.hexdigest()
    userinfo.upasswd = upasswd
    userinfo.uemail = uemail
    userinfo.save()
    return redirect('/user/login/')

def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count' : count})

def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title':'登录', 'error_name':0, 'error_pwd':0, 'uname':uname}
    return render(request, 'auser/login.html', context)

def login_handle(request):
    post = request.POST
    uname = post.get('username')
    upasswd = post.get('pwd')
    jizhu = post.get('jizhu',0)

    users = UserInfo.objects.filter(uname=uname)

    if len(users)==1:
        s1 = sha1()
        s1.update(upasswd)

        if s1.hexdigest()==users[0].upasswd:
            url = request.COOKIES.get('url', '/user/info')
            if url=='':
                url = '/user/info'
            red = HttpResponseRedirect(url)
            if jizhu=='1':
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '')
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {'title': '登录', 'error_name':0, 'error_pwd': 1, 'uname': uname, 'upwd': upasswd}
            return render(request, 'auser/login.html', context)

    else:
        context = {'title': '登录', 'error_name':1, 'error_pwd': 0, 'uname': uname, 'upwd': upasswd}
        return render(request, 'auser/login.html', context)

def loginout(request):
    request.session.flush()
    return redirect('/goods/index')

@user_decrator.login
def user_center_info(request):
    id = request.session['user_id']
    user = UserInfo.objects.filter(id=id)
    uname = user[0].uname
    uphone = user[0].uphone
    uaddress = user[0].uaddress
    context = {'title': "用户中心", 'uname':uname, 'uphone':uphone, 'uaddress':uaddress}
    return render(request, 'auser/user_center_info.html', context)

@user_decrator.login
def user_center_order(request):
    id = request.session['user_id']
    user = UserInfo.objects.filter(id=id)
    uname = user[0].uname
    context = {'title': "用户中心",'uname':uname}
    return render(request, 'auser/user_center_order.html', context)

def user_center_site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    uname = user.uname
    if request.method=='POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    context = {'title': "用户中心",'uname':uname}
    return render(request, 'auser/user_center_site.html', context)

