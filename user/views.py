from django.shortcuts import render, redirect
from .forms import LoginForm, RegForm, ChangeNicknameForm, BindEmailForm, ChangePasswordForm, ForgotPasswordForm
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings
import string
import random
import time
import threading
# Create your views here.


class SendMail(threading.Thread):
    def __init__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        # 发送邮件，通知密码修改成功
        send_mail(
            self.subject,
            self.text,
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=self.fail_silently,
        )


def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            login(request, user)
            # Redirect to a success page.
            return redirect(request.GET.get('from', reverse('default')))
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request, 'user/login.html', context)


def user_register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST, request=request)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            #创建用户
            user = User.objects.create_user(username=username,email=email,password=password)
            user.save()
            #清除session
            del request.session['register_code']
            #登录用户
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(request.GET.get('from', reverse('default')))
    else:
        reg_form = RegForm()
    context = {}
    context['reg_form'] = reg_form
    return render(request, 'user/register.html', context)


def login_for_modal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    print(data)
    return JsonResponse(data)


def user_logout(request):
    logout(request)
    return redirect(request.GET.get('from', reverse('default')))


def user_info(request):
    context = {}
    return render(request, 'user/user_info.html', context)


def change_nickname(request):
    context = {}
    return_back = request.GET.get('from', reverse('default'))
    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = form.cleaned_data['nickname_new']
            profile.save()
            return redirect(return_back)
    else:
        form = ChangeNicknameForm()
    context['form'] = form
    context['page_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['form_title'] = '修改昵称'
    context['return_back_url'] = return_back
    return render(request, 'form.html', context)


def bind_email(request):
    context = {}
    return_back = request.GET.get('from', reverse('default'))
    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            # 清除session
            del request.session['bind_email_code']
            return redirect(return_back)
    else:
        form = BindEmailForm()

    context['form'] = form
    context['page_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form_title'] = '绑定邮箱'
    context['return_back_url'] = return_back
    return render(request, 'user/bind_email.html', context)


def send_verification_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')
    data = {}
    if email != '':
        #生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now
            #发送邮件
            send_mail(
                '绑定邮箱',
                '验证码：%s ' % code,
                '1209966310@qq.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)


def change_password(request):
    context = {}
    return_back = reverse('default')
    '''判断向当前url提交的请求方法，如果是POST请求是提交数据，如果是GET请求是获取表单数据'''
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            '''修改密码'''
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            logout(request)
            return redirect(return_back)
    else:
        form = ChangePasswordForm()
    context['form'] = form
    context['page_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['form_title'] = '修改密码'
    context['return_back_url'] = return_back
    return render(request, 'form.html', context)


def forgot_password(request):
    context = {}
    return_back = reverse('default')
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = form.cleaned_data['user']
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            # 清除session
            del request.session['forgot_password_code']
            subject = '重置密码'
            text = '重置密码成功'
            send_mail_of_password_forgot = SendMail(subject=subject, text=text, email=email)
            send_mail_of_password_forgot.start()
            return redirect(return_back)
    else:
        form = ForgotPasswordForm()

    context['form'] = form
    context['page_title'] = '忘记密码'
    context['submit_text'] = '修改'
    context['form_title'] = '忘记密码'
    context['return_back_url'] = return_back
    return render(request, 'user/forgot_password.html', context)
