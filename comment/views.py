from django.shortcuts import render,redirect
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from .forms import CommentForm
from django.http import JsonResponse
# Create your views here.

def update_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('default'))
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}

    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        parent = comment_form.cleaned_data['parent']
        if parent is not None:
            '''如果当前评论的上一级是最顶层评论时把他设为当前评论的根，否则把上层评论的根设为当前评论的根'''
            comment.root = parent.root if parent.root is not None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()

        #return redirect(referer)
        '''动态加载新添加的评论数据'''
        data['status'] = 'SUCCESS'
        data['username'] = comment.user.get_nickname_or_username()
        data['comment_time'] = comment.comment_time.timestamp()
        data['text'] = comment.text
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        if parent is not None:
            data['reply_to'] = comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if comment.root is not None else ''
    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
        #return render(request, 'login_error.html', {'message': comment_form.errors, 'redirect_to': referer})
    return JsonResponse(data)

