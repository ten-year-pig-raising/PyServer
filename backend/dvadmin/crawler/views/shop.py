import datetime
import django_filters
from rest_framework import serializers
from rest_framework.decorators import action
import dvadmin.crawler.constant as constant
import dvadmin.crawler.core.mt_normal_user_crawler as mt_normal_user_crawler
from dvadmin.crawler.models import ShopModel, ShopServiceModel, InvitationCodeModel
from dvadmin.utils.json_response import SuccessResponse, ErrorResponse
from dvadmin.utils.request_util import get_request_data
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
import logging

logger = logging.getLogger(__name__)


def get_service(shop):
    return [
        {
            "shop_id": shop.id,
            "is_open": False,
            "service_code": constant.SERVICE_TYPE_CALCULATE_SCORE,
            "service_name": "评分计算",
        },

        {
            "shop_id": shop.id,
            "is_open": False,
            "service_code": constant.SERVICE_TYPE_SMART_REPLY_COMMENT,
            "service_name": "智能评论回复",
        },

        {
            "shop_id": shop.id,
            "is_open": False,
            "service_code": constant.SERVICE_TYPE_ASSIST_OUT_ORDER,
            "service_name": "辅助出餐",
        },

        {
            "shop_id": shop.id,
            "is_open": False,
            "service_code": constant.SERVICE_TYPE_GET_ORDERS,
            "service_name": "获取订单",
        },

        {
            "shop_id": shop.id,
            "is_open": False,
            "service_code": constant.SERVICE_TYPE_WARNING_COMMENT,
            "service_name": "评价预警",
        },
    ]


def get_shop_info(shop_code, shop_type):
    if shop_type == constant.SHOP_TYPE_MT:
        return mt_normal_user_crawler.get_shop_info(shop_code)
    # elif shop_type == constant.SHOP_TYPE_ELM:
    #     return elm_normal_user_crawler.get_shop_info(shop_code)
    raise Exception('暂时不支持商家类型:' + shop_type)


class ShopModelSerializer(CustomModelSerializer):
    """
    序列化器
    """
    # inviter_name = serializers.CharField(source='inviter.username', read_only=True)
    shop_type_label = serializers.SerializerMethodField()
    inviter_name = serializers.SlugRelatedField(slug_field="name", source="inviter", read_only=True)
    register_username = serializers.SlugRelatedField(slug_field="username", source="register_user", read_only=True)

    @staticmethod
    def get_shop_type_label(obj: ShopModel):
        if obj.shop_type == constant.SHOP_TYPE_MT:
            return "美团"
        elif obj.shop_type == constant.SHOP_TYPE_ELM:
            return "饿了么"
        return obj.shop_type

    class Meta:
        model = ShopModel
        # exclude = ["password"]
        fields = "__all__"


class ShopModelUpdateSerializer(CustomModelSerializer):
    """
    创建/更新时的列化器
    """

    class Meta:
        model = ShopModel
        fields = '__all__'


class ShopModelCreateSerializer(CustomModelSerializer):
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

    # def validate_password(self, value):
    #     """
    #     对密码进行验证
    #     """
    #     password = self.initial_data.get("password")
    #     # if password:
    #     #     return make_password(value)
    #     return value

    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.save()
        # data.post.set(self.initial_data.get("post", []))
        self.create_shop_services(request=self.request, shop=data)
        return data

    def create_shop_services(self, request, shop):
        # service = ShopServiceModel()
        # service.shop = shop
        # service.is_open = False
        # service.record = 5.6
        # service.save()
        services = get_service(shop)
        for service in services:
            serializer = ShopServiceCreateSerializer(data=service)
            serializer.request = request
            serializer.is_valid()
            serializer.create(validated_data=service)

    class Meta:
        model = ShopModel
        fields = "__all__"
        read_only_fields = ["id"]
        extra_kwargs = {
            "post": {"required": False},
        }


class ShopServiceCreateSerializer(CustomModelSerializer):
    """
    创建列化器
    """

    class Meta:
        model = ShopServiceModel
        fields = '__all__'


class ShopFilterSet(django_filters.FilterSet):
    service_end_time = django_filters.BaseRangeFilter(field_name="service_end_time")
    shop_name = django_filters.CharFilter(field_name="shop_name", lookup_expr="icontains")
    shop_code = django_filters.CharFilter(field_name="shop_code", lookup_expr="icontains")
    invitation_code = django_filters.CharFilter(field_name="invitation_code", lookup_expr="icontains")
    session_expired = django_filters.CharFilter(field_name="session_expired", lookup_expr="icontains")

    class Meta:
        model = ShopModel
        fields = ["shop_name", "shop_type", "shop_code", "invitation_code", "service_end_time", "session_expired"]


class ShopModelViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = ShopModel.objects.all()
    serializer_class = ShopModelSerializer
    create_serializer_class = ShopModelCreateSerializer
    update_serializer_class = ShopModelUpdateSerializer
    filter_class = ShopFilterSet

    # filter_fields = {
    #     "shop_name": ["icontains"],
    #     "shop_type": ["exact"],
    #     "shop_code": ["icontains"],
    #     "invitation_code": ["exact"],
    #     # "service_end_time": ["range"],
    # }
    # search_fields = ["shop_name", "shop_type", "shop_code", "invitation_code", "service_end_time"]

    @action(methods=['GET'], detail=False, permission_classes=[])
    def shop_list(self, request, *args, **kwargs):
        # from dvadmin.crawler.core import shop_tasks
        # shop_tasks.evaluation_of_early_warnings(1, 80)
        # shop_tasks.auto_reply(1, 80)
        # shop_tasks.req_orders(1, 100)
        # shop_tasks.evaluation_of_early_warnings(32, 100)
        # shop_tasks.auto_reply(32, 100)
        # shop_tasks.automatic_dining(32, 100)

        """我的店铺列表接口"""
        data = get_request_data(request)
        if 'register_user_id' not in data:
            return ErrorResponse(msg="未获取到用户信息，请刷新程序")
        # todo 通过类型校验账号密码
        shop_list = ShopModel.objects.filter(register_user_id=data['register_user_id']).values()
        now = datetime.datetime.now()
        for shop in shop_list:
            if not shop['service_end_time'] or now < shop['service_end_time']:
                shop["is_expired"] = True
            else:
                shop["is_expired"] = False
        return SuccessResponse(data=shop_list)

    @action(methods=['GET'], detail=False, permission_classes=[])
    def get_shop_service(self, request, *args, **kwargs):
        params = request.query_params
        shop = ShopModel.objects.get(id=params['id'])

        # # 更新店铺信息
        # net_shop_info = None
        # try:
        #     net_shop_info = get_shop_info(shop_code=shop.shop_code, shop_type=shop.shop_type)
        #     print("net_shop_info", net_shop_info)
        # except Exception as e:
        #     print(e)
        # if net_shop_info:
        #     shop.shop_name = net_shop_info['shop_name']
        #     shop.shop_addr = net_shop_info['shop_addr']
        #     shop.shop_score = net_shop_info['shop_score']
        #     shop.shipping_time = net_shop_info['shipping_time']
        #     shop.save()

        services = ShopServiceModel.objects.filter(shop_id=shop.id).values()
        if not services:
            # 添加店铺服务
            services = get_service(shop)
            for service in services:
                serializer = ShopServiceCreateSerializer(data=service)
                serializer.request = request
                serializer.is_valid()
                serializer.create(validated_data=service)

        result = {
            "id": shop.id,
            "shop_code": shop.shop_code,
            "shop_name": shop.shop_name,
            "shop_type": shop.shop_type,
            "shop_addr": shop.shop_addr,
            "is_bind": shop.is_bind,
            "front_img": shop.front_img,
            "shop_score": shop.shop_score,
            "shipping_time": shop.shipping_time,
            "service_end_time": shop.service_end_time,
            # "inviter": shop.inviter,
            # "register_user": shop.register_user,
            "shop_service": services,
        }
        if not shop.service_end_time:
            result["is_expired"] = True
        elif datetime.datetime.now() < shop.service_end_time:
            result["is_expired"] = False
        else:
            result["is_expired"] = True
        return SuccessResponse(data=result)

    @action(methods=['POST'], detail=False, permission_classes=[])
    def add_shop(self, request, *args, **kwargs):
        """添加店铺接口"""
        data = get_request_data(request)
        # 参数校验
        if 'register_user' not in data:
            return ErrorResponse(msg="未获取到用户信息")
        # 获取邀请码信息
        # todo 获取邀请码，要加上日期，过滤掉过期的code
        invitation_code_model = InvitationCodeModel.objects.get(code=data['invitation_code'])

        if not invitation_code_model:
            return ErrorResponse(msg="邀请码不存在")
        # 同一店铺，不允许多次绑定
        shop = ShopModel.objects.filter(shop_code=data['shop_code'], shop_type=data['shop_type']).first()
        if shop:
            return ErrorResponse(msg="店铺已被添加，如非本人添加，请联系管理人员")
        # 调用美团、饿了吗爬虫接口获取店铺信息
        # todo 新增的时候，还没有店铺cookie，如何去获取店铺信息呢？
        try:
            net_shop_info = get_shop_info(shop_code=data['shop_code'], shop_type=data['shop_type'])
            if net_shop_info:
                data['shop_name'] = net_shop_info['shop_name']
                data['front_img'] = net_shop_info['front_img']
                data['shop_addr'] = net_shop_info['shop_addr']
                data['shipping_time'] = net_shop_info['shipping_time']
                data['shop_score'] = net_shop_info['shop_score']
                # print("net_shop_info", net_shop_info)
                logger.info(net_shop_info)
            else:
                return ErrorResponse(msg="获取店铺信息失败")
        except Exception as e:
            logger.error(e)
            return

        creator = invitation_code_model.creator
        data['inviter'] = creator.id
        data['dept_belong_id'] = creator.dept_id
        data['is_deleted'] = False
        data['creator'] = creator.id
        data['modifier'] = creator.id
        data['is_bind'] = False
        data['session_expired'] = False
        data['service_end_time'] = datetime.datetime.now()
        data['delivery_start_time'] = datetime.datetime.now()
        data['delivery_end_time'] = datetime.datetime.now()
        serializer = ShopModelSerializer(data=data)
        serializer.request = request
        serializer.is_valid()
        shop = serializer.save()
        # 添加店铺服务
        services = get_service(shop)
        for service in services:
            serializer = ShopServiceCreateSerializer(data=service)
            serializer.request = request
            serializer.is_valid()
            serializer.create(validated_data=service)

        # 查找是否有同名的eleme店铺, 没有则添加
        eleme_shop = ShopModel.objects.filter(shop_name=data['shop_name'], shop_type=constant.SHOP_TYPE_ELM).first()
        if not eleme_shop:
            eleme_data = data
            eleme_data['shop_type'] = constant.SHOP_TYPE_ELM
            serializer = ShopModelSerializer(data=eleme_data)
            serializer.request = request
            serializer.is_valid()
            eleme_shop = serializer.save()

            services = get_service(eleme_shop)
            for service in services:
                serializer = ShopServiceCreateSerializer(data=service)
                serializer.request = request
                serializer.is_valid()
                serializer.create(validated_data=service)

        return SuccessResponse(data=data)

    @action(methods=['POST'], detail=False, permission_classes=[])
    def bind_shop(self, request, *args, **kwargs):
        """绑定接口"""
        data = get_request_data(request)
        if data['id'] is None:
            return ErrorResponse(msg="未获取到店铺id")
        # todo 通过类型校验账号密码
        shop = ShopModel.objects.get(id=data['id'])
        shop.is_bind = True
        shop.login_type = data['login_type']
        if data['login_type'] == "account":
            shop.login_name = data['login_name']
            shop.password = data['password']
        if data['login_type'] == "phone":
            shop.login_phone = data['login_phone']
            # shop.verification_code = data['verification_code']
        shop.save()
        return SuccessResponse(data=data)

    @action(methods=['POST'], detail=False, permission_classes=[])
    def bind_shop_verification_code(self, request, *args, **kwargs):
        """绑定接口"""
        data = get_request_data(request)
        if data['id'] is None:
            return ErrorResponse(msg="未获取到店铺id")
        if data['verification_code'] is None:
            return ErrorResponse(msg="请输入验证码")
        shop = ShopModel.objects.get(id=data['id'])
        shop.verification_code = data['verification_code']
        shop.save()
        return SuccessResponse(data=data)

    @action(methods=['GET'], detail=False, permission_classes=[])
    def unbind_shop(self, request, *args, **kwargs):
        """解绑接口"""
        data = get_request_data(request)
        shop = ShopModel.objects.get(id=data['id'])
        shop.is_bind = False
        shop.login_name = None
        shop.password = None
        shop.save()
        return SuccessResponse(data=data)

    @action(methods=['GET'], detail=False, permission_classes=[])
    def delete_shop(self, request, *args, **kwargs):
        """删除接口"""
        data = get_request_data(request)
        shop_id = data['id']
        try:
            ShopModel.objects.filter(id=shop_id).delete()
            ShopServiceModel.objects.filter(shop_id=shop_id).delete()
        except Exception as e:
            logger.error(e)
        return SuccessResponse(data=data)

    @action(methods=['GET'], detail=False, permission_classes=[])
    def update_shop_service_state(self, request, *args, **kwargs):
        """更新店铺服务开启、关闭状态"""
        data = get_request_data(request)
        service = ShopServiceModel.objects.get(id=data['id'])
        service.is_open = True if data['is_open'] == 'true' else False
        service.save()
        return SuccessResponse(data=data)

    @action(methods=['GET'], detail=False, permission_classes=[])
    def update_shop_service_config(self, request, *args, **kwargs):
        """更新店铺服务开启、关闭状态"""
        data = get_request_data(request)
        service = ShopServiceModel.objects.get(id=data['id'])
        if 'record' in data:
            service.record = data['record']
        if 'service_config' in data:
            service.service_config = data['service_config']
        service.save()
        return SuccessResponse(data=data)
