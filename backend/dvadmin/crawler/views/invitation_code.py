import datetime

import django_filters
from rest_framework.decorators import action
from rest_framework.exceptions import APIException

from dvadmin.crawler.models import InvitationCodeModel
from dvadmin.utils.json_response import DetailResponse, ErrorResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class InvitationCodeModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = InvitationCodeModel
        fields = "__all__"


class InvitationCodeModelCreateUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    def update(self, instance, validated_data):
        db_invitation_code = InvitationCodeModel.objects.filter(code=validated_data["code"]).exclude(
            id=instance.id)
        if db_invitation_code:
            raise APIException(detail="邀请码已存在")
        super().update(instance, validated_data)
        return instance

    class Meta:
        model = InvitationCodeModel
        fields = '__all__'


class InvitationCodeCreateSerializer(CustomModelSerializer):
    """
    用户新增-序列化器
    """

    # username = serializers.CharField(
    #     max_length=50,
    #     validators=[
    #         CustomUniqueValidator(queryset=InvitationCodeModel.objects.all(), message="账号必须唯一")
    #     ],
    # )
    # password = serializers.CharField(
    #     required=False,
    # )

    # def validate_password(self, value):
    #     """
    #     对密码进行验证
    #     """
    #     password = self.initial_data.get("password")
    #     # if password:
    #     #     return make_password(value)
    #     return value

    def create(self, validated_data):
        db_invitation_code = InvitationCodeModel.objects.filter(code=validated_data["code"])
        if db_invitation_code:
            raise APIException(detail="邀请码已存在")
        return super(InvitationCodeCreateSerializer, self).create(validated_data)

    class Meta:
        model = InvitationCodeModel
        fields = "__all__"
        read_only_fields = ["id"]
        extra_kwargs = {
            "post": {"required": False},
        }


class InvitationCodeFilterSet(django_filters.FilterSet):
    valid_end_time = django_filters.BaseRangeFilter(field_name="valid_end_time")
    code = django_filters.CharFilter(field_name="code", lookup_expr="icontains")

    class Meta:
        model = InvitationCodeModel
        fields = ['code', 'code_type', 'valid_end_time']


class InvitationCodeModelViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = InvitationCodeModel.objects.all()
    serializer_class = InvitationCodeModelSerializer
    create_serializer_class = InvitationCodeCreateSerializer
    update_serializer_class = InvitationCodeModelCreateUpdateSerializer
    filter_class = InvitationCodeFilterSet
    # filter_fields = {
    #     "code": ["icontains"],
    #     "code_type": ["exact"]
    # }
    # search_fields = ["code", "code_type"]

    @action(methods=['GET'], detail=False, permission_classes=[])
    def check_code(self, request, *args, **kwargs):
        """校验邀请码接口"""
        params = request.query_params
        invitation_code = InvitationCodeModel.objects.filter(code=params['code']).first()
        if not invitation_code:
            return ErrorResponse(msg="邀请码不正确")
        if datetime.datetime.now() >= invitation_code.valid_end_time:
            return ErrorResponse(msg="邀请码已过期")
        return DetailResponse(msg="获取成功")
