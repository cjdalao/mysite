from django.contrib import admin
from .models import ReadCount, ReadDetail
# Register your models here.


@admin.register(ReadCount)
class ReadCountAdmin(admin.ModelAdmin):
    list_display = ('read_count', 'content_object')


@admin.register(ReadDetail)
class ReadDetailAdmin(admin.ModelAdmin):
    list_display = ('read_count', 'date', 'content_object')