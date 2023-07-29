import datetime
import json

import django_filters
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.decorators import action

from dvadmin.crawler.models import OrderModel
from dvadmin.crawler.util.date_util import date_validate_YMD
from dvadmin.utils.json_response import SuccessResponse
from dvadmin.utils.request_util import get_request_data
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class OrderSerializer(CustomModelSerializer):
    class Meta:
        model = OrderModel
        fields = "__all__"


class OrderCreateSerializer(CustomModelSerializer):
    class Meta:
        model = OrderModel
        fields = "__all__"


class OrderUpdateSerializer(CustomModelSerializer):
    class Meta:
        model = OrderModel
        fields = "__all__"


class OrderFilterSet(django_filters.FilterSet):
    order_time = django_filters.BaseRangeFilter(field_name="order_time")
    shop_type = django_filters.CharFilter(field_name="shop_type", lookup_expr="exact")
    shop_code = django_filters.CharFilter(field_name="shop_code", lookup_expr="icontains")
    order_id = django_filters.CharFilter(field_name="order_id", lookup_expr="icontains")
    order_seq_id = django_filters.CharFilter(field_name="order_seq_id", lookup_expr="icontains")

    class Meta:
        model = OrderModel
        fields = ["shop_code", "shop_type", "order_id", "order_time", "order_seq_id"]


class CJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


class OrderModelViewSet(CustomModelViewSet):
    """
        list:查询
        create:新增
        update:修改
        retrieve:单例
        destroy:删除
        """

    queryset = OrderModel.objects.all()
    serializer_class = OrderSerializer
    create_serializer_class = OrderCreateSerializer
    update_serializer_class = OrderUpdateSerializer
    filter_class = OrderFilterSet

    @action(methods=['GET'], detail=False, permission_classes=[])
    def list_order(self, request, *args, **kwargs):
        data = get_request_data(request)
        shop_code = data['shop_code']
        page = data['page']
        page_size = data['limit']
        params = {'shop_code': shop_code}
        if 'recipient_name' in data:
            params['recipient_name__contains'] = data['recipient_name']
        if 'order_time_start' in data:
            start = data['order_time_start']
            validate = date_validate_YMD(start)
            if validate == 1:
                start = start.strip() + " 00:00:00"
            params['order_time__gte'] = start
        if 'order_time_end' in data:
            end = data['order_time_end']
            validate = date_validate_YMD(end)
            if validate == 1:
                end = end.strip() + " 23:59:59"
            params['order_time__lte'] = end
        if 'order_seq_id' in data:
            params['order_seq_id'] = data['order_seq_id']
        if 'order_id' in data:
            params['order_id__contains'] = data['order_id']
        if 'order_key_word' in data:
            params['menu_json__contains'] = data['order_key_word']
        order_list = OrderModel.objects.filter(**params).order_by(
            "-order_time")
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
