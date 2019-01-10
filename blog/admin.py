from django.contrib import admin
from .models import BlogType, Blog
# Register your models here.
@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'blog_type', 'author', 'create_time', 'last_update_time', 'get_read_count')

'''
@admin.register(ReadCount)
class ReadCountAdmin(admin.ModelAdmin):
    list_display = ('read_count', 'blog')
'''