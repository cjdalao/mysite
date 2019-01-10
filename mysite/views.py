from django.shortcuts import render
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_seven_days_hot_blog
from blog.models import Blog


def default(request):
    context = {}
    ct = ContentType.objects.get_for_model(Blog)
    result_list, date_list = get_seven_days_read_data(ct)
    seven_days_hot_data = cache.get('seven_days_hot_data')
    if seven_days_hot_data is None:
        seven_days_hot_data = get_seven_days_hot_blog()
        cache.set('seven_days_hot_data', seven_days_hot_data,3600)  #设置缓存

    context['today_hot_list'] = get_today_hot_data(ct)
    context['seven_days_date'] = date_list
    context['seven_days_count'] = result_list
    context['seven_days_hot_data'] = seven_days_hot_data
    return render(request, 'default.html', context=context)



