from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action
from rest_framework.exceptions import APIException

from dvadmin.crawler.constant import TEMPLATE_ID_KEY
from dvadmin.crawler.core.wx_msg import send_msg, send_shop_msg
from dvadmin.crawler.models import SystemVarModel, ShopModel
from dvadmin.utils.json_response import SuccessResponse, ErrorResponse
from dvadmin.utils.request_util import get_request_data
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


def get_system_var_value(key):
    try:
        system_var = SystemVarModel.objects.get(key=key)
        return system_var.value
    except ObjectDoesNotExist:
        return None


def get_system_var_object(key):
    try:
        system_var = SystemVarModel.objects.get(key=key)
        return system_var
    except ObjectDoesNotExist:
        return None


class SystemVarSerializer(CustomModelSerializer):
    class Meta:
        model = SystemVarModel
        fields = "__all__"


class SystemVarCreateSerializer(CustomModelSerializer):
    class Meta:
        model = SystemVarModel
        fields = "__all__"


class SystemVarUpdateSerializer(CustomModelSerializer):
    class Meta:
        model = SystemVarModel
        fields = "__all__"


class SystemVarModelViewSet(CustomModelViewSet):
    """
        list:查询
        create:新增
        update:修改
        retrieve:单例
        destroy:删除
        """
    queryset = SystemVarModel.objects.all()
    serializer_class = SystemVarSerializer
    create_serializer_class = SystemVarCreateSerializer
    update_serializer_class = SystemVarUpdateSerializer

    # filter_fields = ['goods', 'goods_price']
    # search_fields = ['code']

    @action(methods=['POST'], detail=False, permission_classes=[])
    def send_msg(self, request, *args, **kwargs):
        """我的店铺列表接口"""

        data = get_request_data(request)
        if not data['user_type']:
            raise APIException(detail="参数user_type不能为空")
        if not data['tousers']:
            raise APIException(detail="参数tousers不能为空")
        # if not data['thing1'] or not data['thing3'] or not data['amount2']:
        #     raise APIException(detail="参数不能为空")
        tousers = []
        if 'shop' == data['user_type']:
            shop_ids = data['tousers'].split(';')
            for shop_id in shop_ids:
                shop = ShopModel.objects.get(id=shop_id)
                openid = shop.register_user.openid
                tousers.append(openid)
        else:
            tousers.append(data['tousers'].split(';'))
        for touser in tousers:
            rs = send_msg(touser=touser, data_dict=data)
        if rs['errmsg'] != 'ok':
            return ErrorResponse(msg=rs['errmsg'])
        return SuccessResponse()

    @action(methods=['POST'], detail=False, permission_classes=[])
    def send_shop_msg(self, request, *args, **kwargs):
        """我的店铺列表接口"""
        data = get_request_data(request)
        if not data['shop_code'] or not data['shop_type']:
            raise APIException(detail="参数shop_code不能为空")
        if not data['thing1'] or not data['thing3'] or not data['amount2']:
            raise APIException(detail="参数不能为空")
        send_shop_msg(touser=data['shop_code'], shop_type=data['shop_type'], data_dict=data)
        return SuccessResponse()

    @action(methods=['GET'], detail=False, permission_classes=[])
    def get_msg_temp_id(self, request, *args, **kwargs):
        system_var = get_system_var_object(TEMPLATE_ID_KEY)
        if not system_var:
            return ErrorResponse(msg="未找到模板id")
        temp_ids = system_var.value.split(';')
        return SuccessResponse(data=temp_ids)
