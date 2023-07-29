import django_filters

from dvadmin.crawler.models import BusinessSessionModel
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class BusinessSessionSerializer(CustomModelSerializer):
    class Meta:
        model = BusinessSessionModel
        fields = "__all__"


class BusinessSessionCreateSerializer(CustomModelSerializer):
    class Meta:
        model = BusinessSessionModel
        fields = "__all__"


class BusinessSessionUpdateSerializer(CustomModelSerializer):
    class Meta:
        model = BusinessSessionModel
        fields = "__all__"


class BusinessSessionFilterSet(django_filters.FilterSet):
    session_expires_in = django_filters.BaseRangeFilter(field_name="session_expires_in")
    shop_code = django_filters.CharFilter(field_name="shop_code", lookup_expr="icontains")

    class Meta:
        model = BusinessSessionModel
        fields = ["shop_code", "shop_type", "session_expires_in"]


class BusinessSessionModelViewSet(CustomModelViewSet):
    """
        list:查询
        create:新增
        update:修改
        retrieve:单例
        destroy:删除
        """

    queryset = BusinessSessionModel.objects.all()
    serializer_class = BusinessSessionSerializer
    create_serializer_class = BusinessSessionCreateSerializer
    update_serializer_class = BusinessSessionUpdateSerializer
    filter_class = BusinessSessionFilterSet
    # filter_fields = {
    #     "shop_code": ["icontains"],
    #     "shop_type": ["exact"]
    # }
    # search_fields = ["shop_code", "shop_type"]
