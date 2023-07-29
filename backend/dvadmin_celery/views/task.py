# -*- coding: utf-8 -*-

"""
@author: 阿辉
@contact: QQ:2655399832
@Created on: 2022/9/21 16:30
@Remark:
"""

from django_celery_beat.models import PeriodicTask, CrontabSchedule, cronexp
from rest_framework import serializers
from rest_framework.exceptions import APIException

from dvadmin.utils.json_response import SuccessResponse, ErrorResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin_celery.views.crontab_schedule import CrontabScheduleSerializer

CrontabSchedule.__str__ = lambda self: '{0} {1} {2} {3} {4} {5}'.format(
    cronexp(self.minute), cronexp(self.hour),
    cronexp(self.day_of_month), cronexp(self.month_of_year),
    cronexp(self.day_of_week), str(self.timezone)
)


def get_job_list():
    from application import settings
    task_list = []
    task_dict_list = []
    for app in settings.INSTALLED_APPS:
        try:
            exec(f"""
from {app} import tasks
for ele in [i for i in dir(tasks) if i.startswith('task__')]:
    task_dict = dict()
    task_dict['label'] = '{app}.tasks.' + ele
    task_dict['value'] = '{app}.tasks.' + ele
    task_list.append('{app}.tasks.' + ele)
    task_dict_list.append(task_dict)
                """)
        except ImportError:
            pass
    return {'task_list': task_list, 'task_dict_list': task_dict_list}


# 将cron表达式进行解析
def CronSlpit(cron):
    cron = cron.split(" ")
    result = {
        # "second":cron[0],
        "minute": cron[0],
        "hour": cron[1],
        "day": cron[2],
        "month": cron[3],
        "week": cron[4]
    }
    return result


class CeleryCrontabScheduleSerializer(CustomModelSerializer):
    class Meta:
        model = CrontabSchedule
        exclude = ('timezone',)


class PeriodicTasksSerializer(CustomModelSerializer):
    # crontab = serializers.StringRelatedField(read_only=False)
    #
    # # def to_representation(self, value):
    # #     data = super().to_representation(value)
    # #     data['crontab'] = value.crontab.__str__()
    # #     return data
    #
    # class Meta:
    #     model = PeriodicTask
    #     fields = '__all__'
    crontab_str = serializers.SerializerMethodField()

    class Meta:
        model = PeriodicTask
        fields = '__all__'

    def get_crontab_str(self, instance):
        cron = instance.crontab
        serializers = CrontabScheduleSerializer(cron)
        # return [{"id": instance.crontab.id,"value":instance.crontab.__str__()}]
        # return serializers.data
        return cron.minute + ' ' + cron.hour + ' ' + cron.day_of_week + ' ' + cron.day_of_month + ' ' + cron.month_of_year
        # return instance.crontab.__str__()


class CeleryTaskModelViewSet(CustomModelViewSet):
    """
    CeleryTask 添加任务调度
    """

    queryset = PeriodicTask.objects.exclude(name="celery.backend_cleanup")
    serializer_class = PeriodicTasksSerializer
    filter_fields = ['name', 'task', 'enabled']

    # permission_classes = []
    # authentication_classes = []

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, request=request)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True, request=request)
        return SuccessResponse(data=serializer.data, msg="获取成功")

    def job_list(self, request, *args, **kwargs):
        """获取所有任务"""
        result = get_job_list()
        task_list = result.get('task_dict_list')
        return SuccessResponse(msg='获取成功', data=task_list, total=len(task_list))

    def create(self, request, *args, **kwargs):
        body_data = request.data.copy()
        # cron = body_data.get('crontab')
        crontab_str = body_data.get('crontab_str')
        cron_lisr = CronSlpit(crontab_str)
        minute = cron_lisr["minute"]
        hour = cron_lisr["hour"]
        day = cron_lisr["day"]
        month = cron_lisr["month"]
        week = cron_lisr["week"]
        cron_data = {
            'minute': minute,
            'hour': hour,
            'day_of_week': week,
            'day_of_month': day,
            'month_of_year': month
        }
        task = body_data.get('task')
        result = None
        task_list = get_job_list()
        task_list = task_list.get('task_list')
        if task in task_list:
            # job_name = task.split('.')[-1]
            # path_name = '.'.join(task.split('.')[:-1])

            # 添加crontab
            serializer = CeleryCrontabScheduleSerializer(data=cron_data, request=request)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            # 添加任务
            body_data['crontab'] = serializer.data.get('id')
            body_data['enabled'] = False
            serializer = self.get_serializer(data=body_data, request=request)
            res = serializer.is_valid()
            if not res:
                raise APIException({"msg": f"添加失败，已经有一个名为 {body_data['name']} 的任务了"}, code=4000)
            self.perform_create(serializer)
            result = serializer.data
            return SuccessResponse(msg="添加成功", data=result)
        else:
            return ErrorResponse(msg="添加失败,没有该任务", data=None)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        body_data = request.data
        instance.name = body_data.get('name')  # 更新名称
        instance.task = body_data.get('task')  # 更新任务
        instance.args = body_data.get('args')  # 更新参数
        instance.kwargs = body_data.get('kwargs')  # 更新参数

        # 更新crontab
        cron = body_data.get('crontab')
        crontab_str = body_data.get('crontab_str')
        cron_data = CronSlpit(crontab_str)
        db_corn = CrontabSchedule.objects.get(id=cron)
        # todo 为什么db_corn.day_of_month = cron_data['day']？
        db_corn.minute = cron_data['minute']
        db_corn.hour = cron_data['hour']
        db_corn.day_of_week = cron_data['week']
        db_corn.day_of_month = cron_data['day']
        db_corn.month_of_year = cron_data['month']
        db_corn.save()
        # schedule, created = CrontabSchedule.objects.get_or_create(**cron_data)  # 手动创建crontab，避免重复创建
        # instance.crontab = schedule

        instance.description = body_data.get('description')  # 更新描述
        instance.save()
        return SuccessResponse(msg="修改成功", data=None)

    def destroy(self, request, *args, **kwargs):
        """删除定时任务"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return SuccessResponse(data=[], msg="删除成功")

    def update_status(self, request, *args, **kwargs):
        """开始/暂停任务"""
        instance = self.get_object()
        body_data = request.data
        instance.enabled = body_data.get('enabled')
        instance.save()
        return SuccessResponse(msg="修改成功", data=None)
