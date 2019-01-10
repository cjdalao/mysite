from django.db.models import Sum
from .models import ReadDetail
from django.utils import timezone
from blog.models import Blog
import datetime

def get_seven_days_read_data(content_type):
    date = timezone.now().date()
    result_list = []
    date_list = []
    for i in range(6, -1, -1):
        pre_date = date - datetime.timedelta(days=i)
        date_list.append(pre_date)
        read_details = ReadDetail.objects.filter(content_type=content_type, date__date=pre_date)
        result = read_details.aggregate(pre_read_count=Sum('read_count'))
        result_list.append(result['pre_read_count'] or 0)
    return result_list, date_list

def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date__date=today).order_by('-read_count')
    return read_details[:3]

def get_seven_days_hot_blog():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__date__lte=today, read_details__date__date__gte=date) \
                        .values('id', 'title').annotate(read_num_sum=Sum('read_details__read_count')).order_by('-read_num_sum')
    return blogs[:3]