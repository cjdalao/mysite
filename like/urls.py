from django.urls import path
from . import views

urlpatterns = [
    #127.0.0.1:8000/like
    path('like_change', views.like_change, name='like_change')
]