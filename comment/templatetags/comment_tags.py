from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm
'''自定义模板标签'''

register = template.Library()

@register.simple_tag()
def count_comment(obj):
    ct = ContentType.objects.get_for_model(obj)
    count = Comment.objects.filter(content_type=ct, object_id=obj.pk).count()
    return count


'''评论标点标签'''
@register.simple_tag()
def get_comment_form(obj):
    ct = ContentType.objects.get_for_model(obj)
    form = CommentForm(initial={'content_type': ct, 'object_id': obj.id, 'reply_comment_id': 0})
    return form