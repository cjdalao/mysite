from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogType
from django.db.models import Count
from django.core.paginator import Paginator
from django.conf import settings
from read_statistics.models import ReadCount,ReadDetail
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from comment.models import Comment
from user.forms import LoginForm
# Create your views here.


def blog_get_common_data(blog_all_list,request):
    paginator = Paginator(blog_all_list, settings.PAGE_BLOG_NUM)  # 每（settings文件中）6页进行分页，paginator是Django自带的分页器
    page_num = request.GET.get('page', 1)  # 获取url页面参数（GET请求）
    page_index = paginator.get_page(page_num)
    cur = page_index.number  # 获得当前页码
    page_range = [(cur + i) for i in range(-2, 3) if (cur + i) > 0 and (cur + i) <= paginator.num_pages]
    # 加上省略号
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if page_range[-1] + 1 < paginator.num_pages:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    """获取对应分类的博客数量"""
    '''方法一
    blog_types = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blog_types:
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_types_list.append(blog_type)
    '''
    '''方法二'''
    blog_types_list = BlogType.objects.annotate(blog_count=Count('blog')) #blog是博客模型的类名 （小写）
    #获取日期博客数量
    blog_dates_list = Blog.objects.dates('create_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates_list:
        blog_count = Blog.objects.filter(create_time__year=blog_date.year, create_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {}
    # context['blogs'] = page_index.object_list
    context['blog_dates'] = blog_dates_dict
    context['page_range'] = page_range
    context['page_of_blogs'] = page_index
    #context['blog_types'] = BlogType.objects.all()
    context['blog_types'] = blog_types_list
    return context


def blog_list(request):
    blog_all_list = Blog.objects.all()
    context = blog_get_common_data(blog_all_list,request)
    return render(request, 'blog/blog_list.html', context=context)


def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(Blog, id=blog_pk)
    date = timezone.now().date()
    ct = ContentType.objects.get_for_model(Blog)
    '''获取浏览器发送来的cookie 并查看 对应当前文章是否存在 ，不存在是阅读量+1 '''
    if not request.COOKIES.get('blog_%s_read' % blog_pk):
        #总阅读数加一
        rec, created = ReadCount.objects.get_or_create(content_type=ct, object_id=blog.id)
        rec.read_count += 1
        rec.save()
        #当天阅读数加一
        red, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=blog.id, date=date)
        red.read_count += 1
        red.save()
    context['blog'] = blog
    #context['login_form'] = LoginForm() #登录表单
    context['blog_comment'] = Comment.objects.filter(content_type=ct, object_id=blog.id, parent=None).order_by('-comment_time')  #顶级评论列表
    context['previous_blog'] = Blog.objects.filter(create_time__gt=blog.create_time).last() #筛选器,选择时间较新的
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()
    #context['comment_form'] = CommentForm(initial={'content_type': ct, 'object_id': blog.id, 'reply_comment_id': 0}) #初始化评论表单
    response = render(request, 'blog/blog_detail.html', context)
    response.set_cookie('blog_%s_read' % blog_pk, 'true')  #设置 cookie 把对应的文章设置为已读
    return response


def blog_with_type(request,blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk) #获取该类型的博客
    blog_all_list = Blog.objects.filter(blog_type=blog_type) #筛选器筛选
    context = blog_get_common_data(blog_all_list,request)
    context['type'] = blog_type
    return render(request, 'blog/blog_type_list.html', context=context)


def blogs_with_date(request, year, month):
    blog_all_list = Blog.objects.filter(create_time__year=year, create_time__month=month)  # 筛选器筛选
    context = blog_get_common_data(blog_all_list,request)
    context['blog_date_tag'] = '%s年%s月' % (year, month)
    return render(request, 'blog/blog_date_list.html', context=context)

