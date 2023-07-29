from rest_framework.decorators import action
from dvadmin.crawler.models import RegisterUserModel
from dvadmin.utils.json_response import SuccessResponse, ErrorResponse
from dvadmin.utils.request_util import get_request_data
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from django.core.exceptions import ObjectDoesNotExist
import requests


class RegisterUserModelSerializer(CustomModelSerializer):
    """
    序列化器
    """

    class Meta:
        model = RegisterUserModel
        fields = "__all__"


class RegisterUserModelUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = RegisterUserModel
        fields = '__all__'


class RegisterUserModelCreateSerializer(CustomModelSerializer):
    """
    用户新增-序列化器
    """

    # username = serializers.CharField(
    #     max_length=50,
    #     validators=[
    #         CustomUniqueValidator(queryset=RegisterUserCodeModel.objects.all(), message="账号必须唯一")
    #     ],
    # )
    # password = serializers.CharField(
    #     required=False,
    # )

    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.save()
        # data.post.set(self.initial_data.get("post", []))
        return data

    class Meta:
        model = RegisterUserModel
        fields = "__all__"
        read_only_fields = ["id"]
        extra_kwargs = {
            "post": {"required": False},
        }


class RegisterUserModelViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = RegisterUserModel.objects.all()
    serializer_class = RegisterUserModelSerializer
    create_serializer_class = RegisterUserModelCreateSerializer
    update_serializer_class = RegisterUserModelUpdateSerializer
    filter_fields = {
        "alias_name": ["icontains"],
        "openid": ["icontains"]
    }
    search_fields = ["alias_name", "openid"]

    @action(methods=['GET'], detail=False, permission_classes=[])
    def get_register_user_by_openid(self, request, *args, **kwargs):
        """更新店铺服务开启、关闭状态"""
        data = get_request_data(request)
        # 参数校验
        if 'openid' not in data:
            return ErrorResponse(msg="未获取到用户的openid")
        # print(data)
        # 如果不存就新增一条数据
        try:
            register_user = RegisterUserModel.objects.get(openid=data['openid'])
        except ObjectDoesNotExist:
            serializer = RegisterUserModelCreateSerializer(data=data)
            serializer.request = request
            serializer.is_valid()
            register_user = serializer.save()

        result = {
            "id": register_user.id,
            "alias_name": register_user.alias_name,
            "username": register_user.username,
            "telephone": register_user.telephone,
            "avatar": register_user.avatar,
            "union_id": register_user.union_id,
            "openid": register_user.openid,
        }
        return SuccessResponse(data=result)

    @action(methods=['POST'], detail=False, permission_classes=[])
    def update_register_user(self, request, *args, **kwargs):
        data = get_request_data(request)
        id_status = ('id' in data)
        if not id_status:
            return ErrorResponse(msg="用户ID不存在")

        register_user = RegisterUserModel.objects.get(id=data['id'])

        alias_name_status = ('alias_name' in data)
        if alias_name_status:
            register_user.alias_name = data['alias_name']
        if 'telephone' in data:
            register_user.telephone = data['telephone']
        if 'username' in data:
            register_user.username = data['username']
        register_user.save()
        return SuccessResponse()

    @action(methods=['GET'], detail=False, permission_classes=[])
    def get_openid(self, request, *args, **kwargs):
        data = get_request_data(request)
        res = {}
        appId = 'wx0fb2061401ae94e6'  # 开发者appid
        secret = 'adee70d7bb0659f33eafb3d6774b260d'  # 开发者AppSecret(小程序密钥)
        grant_type = "authorization_code"  # 默认authorization_code
        js_code = data['js_code']  # wx.login登录获取的code值

        data = {'appId': appId, 'secret': secret, "grant_type": grant_type, "js_code": js_code}
        url = "https://api.weixin.qq.com/sns/jscode2session"
        jscode = requests.get(url, data)
        res = jscode.json()
        return SuccessResponse(data=res)
