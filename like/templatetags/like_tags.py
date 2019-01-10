from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import LikeCount, LikeRecord
register = template.Library()


@register.simple_tag()
def get_like_sum(obj):
    ct = ContentType.objects.get_for_model(obj)
    like_count, created = LikeCount.objects.get_or_create(content_type=ct, object_id=obj.pk)
    return like_count.like_sum


@register.simple_tag(takes_context=True)
def get_like_status(context, obj):
    ct = ContentType.objects.get_for_model(obj)
    user = context['user']
    if not user.is_authenticated:
        return ''
    if LikeRecord.objects.filter(content_type=ct, object_id=obj.pk, user=user).exists():
        return 'active'
    else:
        return ''

@register.simple_tag()
def get_content_type(obj):
    ct = ContentType.objects.get_for_model(obj)
    return ct.model