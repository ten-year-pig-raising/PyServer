import datetime

import django_filters
from django.core.exceptions import ObjectDoesNotExist

from dvadmin.crawler.models import NormalSessionModel
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class NormalSessionSerializer(CustomModelSerializer):
    class Meta:
        model = NormalSessionModel
        fields = "__all__"


class NormalSessionCreateSerializer(CustomModelSerializer):
    class Meta:
        model = NormalSessionModel
        fields = "__all__"


class NormalSessionUpdateSerializer(CustomModelSerializer):
    class Meta:
        model = NormalSessionModel
        fields = "__all__"


# 根据店铺类型，获取到个人账号cookie, 从所有个人账号里选出 最近最久未使用的cookie
def get_db_cookie(shop_type):
    cookie = ''
    tmp_session = None
    try:
        session_list = NormalSessionModel.objects.filter(shop_type=shop_type).values()
        for session in session_list:
            if session['cookie_expires_in'] > datetime.datetime.now():  # 未过期
                if tmp_session:
                    if session['update_datetime'] < tmp_session['update_datetime']:
                        tmp_session = session
                else:
                    tmp_session = session

        if tmp_session:
            cookie = tmp_session['cookie']
            new_session = NormalSessionModel.objects.get(id=tmp_session['id'])
            new_session.save()
        return cookie
    except ObjectDoesNotExist as e:
        print(e)
        return cookie


class NormalSessionFilterSet(django_filters.FilterSet):
    cookie_expires_in = django_filters.BaseRangeFilter(field_name="cookie_expires_in")
    phone_number = django_filters.CharFilter(field_name="phone_number", lookup_expr="icontains")

    class Meta:
        model = NormalSessionModel
        fields = ['phone_number', 'shop_type', 'cookie_expires_in']


class NormalSessionModelViewSet(CustomModelViewSet):
    """
        list:查询
        create:新增
        update:修改
        retrieve:单例
        destroy:删除
        """

    queryset = NormalSessionModel.objects.all()
    serializer_class = NormalSessionSerializer
    create_serializer_class = NormalSessionCreateSerializer
    update_serializer_class = NormalSessionUpdateSerializer
    filter_class = NormalSessionFilterSet
    # filter_fields = {
    #     "phone_number": ["icontains"],
    #     "shop_type": ["icontains"]
    # }
    # search_fields = ["phone_number", "shop_type"]
