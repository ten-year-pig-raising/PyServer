from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import action

from dvadmin.crawler.models import SubMsgConfigModel
from dvadmin.utils.json_response import ErrorResponse, SuccessResponse
from dvadmin.utils.request_util import get_request_data
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet


class SubMsgConfigSerializer(CustomModelSerializer):
    class Meta:
        model = SubMsgConfigModel
        fields = "__all__"


class SubMsgConfigCreateSerializer(CustomModelSerializer):
    class Meta:
        model = SubMsgConfigModel
        fields = "__all__"


class SubMsgConfigUpdateSerializer(CustomModelSerializer):
    class Meta:
        model = SubMsgConfigModel
        fields = "__all__"


class SubMsgConfigModelViewSet(CustomModelViewSet):
    """
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = SubMsgConfigModel.objects.all()
    serializer_class = SubMsgConfigSerializer
    create_serializer_class = SubMsgConfigCreateSerializer
    update_serializer_class = SubMsgConfigUpdateSerializer

    # filter_fields = {
    #     "code": ["icontains"],
    #     "code_type": ["exact"]
    # }
    # search_fields = ["code", "code_type"]

    @action(methods=['GET'], detail=False, permission_classes=[])
    def update_sub_msg(self, request, *args, **kwargs):
        data = get_request_data(request)
        # 参数校验
        if 'register_user' not in data:
            return ErrorResponse(msg="未获取到用户信息")
        try:
            sub_msg_config_model = SubMsgConfigModel.objects.get(register_user=data['register_user'])
            if sub_msg_config_model.sub_times >= 100:
                return ErrorResponse(msg="达到订阅上限")
            sub_msg_config_model.sub_times = sub_msg_config_model.sub_times + 1
            sub_msg_config_model.save()
        except ObjectDoesNotExist:
            data['sub_times'] = 0
            serializer = SubMsgConfigCreateSerializer(data=data)
            serializer.request = request
            serializer.is_valid()
            serializer.save()

        return SuccessResponse()

    @action(methods=['GET'], detail=False, permission_classes=[])
    def get_sub_msg(self, request, *args, **kwargs):
        data = get_request_data(request)
        # 参数校验
        if 'register_user' not in data:
            return ErrorResponse(msg="未获取到用户信息")

        sub_times = 0
        # print(data)
        try:
            sub_msg_config_model = SubMsgConfigModel.objects.get(register_user=data['register_user'])
            sub_times = sub_msg_config_model.sub_times
            # print(sub_times)
        except ObjectDoesNotExist:
            data['sub_times'] = 0
            serializer = SubMsgConfigCreateSerializer(data=data)
            serializer.request = request
            serializer.is_valid()
            serializer.save()
        result = {
            'sub_times': sub_times
        }
        # print(result)
        return SuccessResponse(data=result)
