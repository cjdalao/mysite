from django.contrib.contenttypes.models import ContentType
from.models import LikeCount,LikeRecord
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
# Create your views here.


def SuccessResponse(like_sum):
    data = {}
    data['status'] = 'SUCCESS'
    data['like_sum'] = like_sum
    return JsonResponse(data)


def ErrorResponse(code, message):
    data = {}
    data['status'] = 'ERROR'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)


def like_change(request):
    #获取数据
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400, "you didn't login")

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))
    try:
        ct = ContentType.objects.get(model=content_type)
        model_class = ct.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401, 'this data is not exist')

    #处理数据
    if request.GET.get('is_like') == 'true':
        #点赞
        like_record, created = LikeRecord.objects.get_or_create(content_type=ct, object_id=object_id, user=user)
        if created:
            like_count, created = LikeCount.objects.get_or_create(content_type=ct, object_id=object_id)
            like_count.like_sum += 1
            like_count.save()
            return SuccessResponse(like_count.like_sum)
        else:
            #已点赞，不能重复点赞
            return ErrorResponse(402, 'you had like')
    else:
        #取消点赞
        if LikeRecord.objects.filter(content_type=ct, object_id=object_id,user=user).exists():
            #有点赞记录，取消点赞
            like_record = LikeRecord.objects.get(content_type=ct, object_id=object_id, user=user)
            like_record.delete()
            #点赞数减一
            like_count, created = LikeCount.objects.get_or_create(content_type=ct, object_id=object_id)
            if not created:
                like_count.like_sum -= 1
                like_count.save()
                return SuccessResponse(like_count.like_sum)
            else:
                return ErrorResponse(404, 'data error')
        else:
            #没有点赞记录， 不能取消
            return ErrorResponse(403, 'you are not like')
