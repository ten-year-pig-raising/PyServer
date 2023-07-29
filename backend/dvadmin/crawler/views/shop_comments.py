import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core import serializers
from rest_framework.decorators import action
from dvadmin.crawler.models import ShopCommentModel
from dvadmin.crawler.util.date_util import date_validate_YMD
from dvadmin.crawler.views.order import CJsonEncoder
from dvadmin.utils.json_response import SuccessResponse
from dvadmin.utils.request_util import get_request_data
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
import dvadmin.crawler.core.mt_normal_user_crawler as mt_client


class ShopCommentSerializer(CustomModelSerializer):
    class Meta:
        model = ShopCommentModel
        fields = "__all__"


class ShopCommentCreateSerializer(CustomModelSerializer):
    class Meta:
        model = ShopCommentModel
        fields = "__all__"


class ShopCommentUpdateSerializer(CustomModelSerializer):
    class Meta:
        model = ShopCommentModel
        fields = "__all__"


class ShopCommentsModelViewSet(CustomModelViewSet):
    """
        list:查询
        create:新增
        update:修改
        retrieve:单例
        destroy:删除
        """
    queryset = ShopCommentModel.objects.all()
    serializer_class = ShopCommentSerializer
    create_serializer_class = ShopCommentCreateSerializer
    update_serializer_class = ShopCommentUpdateSerializer

    # filter_fields = ['goods', 'goods_price']
    # search_fields = ['code']
    @action(methods=['GET'], detail=False, permission_classes=[])
    def list_comments(self, request, *args, **kwargs):
        data = get_request_data(request)
        page = data['page']
        page_size = data['limit']
        shop_id = data['shop_id']
        params = {'shop_id_id': shop_id}
        if 'comment_key_word' in data:
            params['content__contains'] = data['comment_key_word']
        if 'user_name' in data:
            params['user_name__contains'] = data['user_name']
        if 'comment_time_start' in data:
            start = data['comment_time_start']
            validate = date_validate_YMD(start)
            if validate == 1:
                start = start.strip() + " 00:00:00"
            params['comment_time__gte'] = start
        if 'comment_time_end' in data:
            end = data['comment_time_end']
            validate = date_validate_YMD(end)
            if validate == 1:
                end = end.strip() + " 23:59:59"
            params['comment_time__lte'] = end
        order_list = ShopCommentModel.objects.filter(**params).order_by("-comment_time")
        paginator = Paginator(order_list, page_size)
        try:
            orders = paginator.page(page)
        except PageNotAnInteger:
            orders = paginator.page(1)
        except EmptyPage:
            # orders = paginator.page(paginator.num_pages)
            orders = []
        data = json.loads(serializers.serialize("json", orders, ensure_ascii=False, cls=CJsonEncoder))
        return SuccessResponse(data=data)
