from django.urls import path
from . import views
#http://127.0.0.1:8000/blog

urlpatterns = [
    path('<int:blog_pk>', views.blog_detail, name="blog_detail"),
    path('type/<int:blog_type_pk>', views.blog_with_type, name='blog_type_list'),
    path('', views.blog_list, name='blog_list'),
    path('date/<int:year>/<int:month>', views.blogs_with_date, name='blogs_with_date'),
]