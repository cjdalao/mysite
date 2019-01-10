from django.urls import path
from . import views

urlpatterns = [
    #127.0.0.1:8000/user
    path('login/', views.user_login, name='user_login'),  # 登录
    path('login_for_modal/', views.login_for_modal, name='login_for_modal'),  # 博客页面内动态请求实现登录
    path('register/', views.user_register, name='user_register'),  # 注册
    path('logout/', views.user_logout, name='user_logout'),  # 注销
    path('user_info/', views.user_info, name='user_info'),  # 用户信息
    path('change_nickname/', views.change_nickname, name='change_nickname'),  # 昵称
    path('bind_email/', views.bind_email, name='bind_email'),   #绑定邮箱
    path('send_verification_code/', views.send_verification_code, name='send_verification_code'),  #发送验证码
    path('change_password/', views.change_password, name='change_password'),   #修改密码
    path('forgot_password/', views.forgot_password, name='forgot_password'),   #忘记密码
]
