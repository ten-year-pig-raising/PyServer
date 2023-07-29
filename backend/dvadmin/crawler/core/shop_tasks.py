import datetime
from dvadmin.crawler.core import wx_msg, elm_business_user_crawler, mt_normal_user_crawler
from dvadmin.crawler.models import ShopModel, ShopServiceModel
from dvadmin.crawler.core import mt_business_user_crawler
import dvadmin.crawler.constant as constant
from dvadmin.crawler.util import waimai_util
import logging

logger = logging.getLogger(__name__)


def get_service_status(shop_id, service_type):
    status = False
    service_config = None
    services = ShopServiceModel.objects.filter(shop_id=shop_id).values()
    for service in services:
        if service['service_code'] == service_type:
            status = service['is_open']
            service_config = service['service_config']
            return status, service_config

    return status, service_config


# 评价预警
# shop_id_start-shop_id_end :  对这个范围内的店铺进行处理，获取评价
def evaluation_of_early_warnings(shop_id_start, shop_id_end):
    warning_score = 4  # < 默认4分预警
    try:
        shop_list = ShopModel.objects.filter(id__gte=shop_id_start, id__lte=shop_id_end).values()
        for shop_data in shop_list:
            shop_code = shop_data['shop_code']
            shop_id = shop_data['id']
            shop_type = shop_data['shop_type']
            status, service_config = get_service_status(shop_id, constant.SERVICE_TYPE_WARNING_COMMENT)
            if not status:
                continue

            if not waimai_util.is_null_or_empty(service_config):
                tmp_warning_score = float(service_config)
                warning_score = tmp_warning_score

            service_end_time = shop_data['service_end_time']
            if service_end_time <= datetime.datetime.now():  # 过期
                # print('服务已过期')
                continue

            # delivery_start_time = shop_data['delivery_start_time']
            # delivery_end_time = shop_data['delivery_end_time']
            # time_validate = waimai_util.check_delivery_time(delivery_start_time, delivery_end_time)
            # # print(str(shop_id) + 'time_validate ' + str(time_validate))
            # if not time_validate:
            #     continue

            if shop_type == constant.SHOP_TYPE_MT:
                comment_list = mt_business_user_crawler.req_all_comments_by_business_account(shop_id, warning_score)
                for comment in comment_list:
                    wx_msg.send_shop_msg(shop_code, shop_type, comment)
                # print(comment_list)
                logger.info('meituan: evaluation_of_early_warnings end: shop_code' + str(shop_code))
            elif shop_type == constant.SHOP_TYPE_ELM:
                comment_list = elm_business_user_crawler.req_all_comments_by_business_account(shop_id, warning_score)
                for comment in comment_list:
                    wx_msg.send_shop_msg(shop_code, shop_type, comment)
                # print(comment_list)
                logger.info('eleme: evaluation_of_early_warnings end shop_code ' + str(shop_code))
    except Exception as e:
        logger.error(e)
        # print(e)
        # raise Exception("找不到店铺")


# 评分管理
def scoring_management(shop_id_start, shop_id_end):
    try:
        shop_list = ShopModel.objects.filter(id__gte=shop_id_start, id__lte=shop_id_end).values()
        for shop_data in shop_list:
            shop_code = shop_data['shop_code']
            shop_id = shop_data['id']
            shop_type = shop_data['shop_type']
            status = get_service_status(shop_id, constant.SERVICE_TYPE_CALCULATE_SCORE)
            if not status:
                continue

            service_end_time = shop_data['service_end_time']
            if service_end_time <= datetime.datetime.now():  # 过期
                # print('服务已过期')
                continue

            delivery_start_time = shop_data['delivery_start_time']
            delivery_end_time = shop_data['delivery_end_time']
            time_validate = waimai_util.check_delivery_time(delivery_start_time, delivery_end_time)
            if not time_validate:
                continue

            net_shop_info = None
            if shop_type == constant.SHOP_TYPE_MT:
                net_shop_info = mt_normal_user_crawler.get_shop_info(shop_code)
            # elif shop_type == constant.SHOP_TYPE_ELM:
            #     net_shop_info = elm_normal_user_crawler.get_shop_info(shop_code)
            if not net_shop_info:
                error_str = '获取商家信息失败:' + str(shop_type) + ": shop_code: " + str(shop_code)
                logger.error(error_str)
                continue

            shop = ShopModel.objects.get(id=shop_id)
            shop.shop_name = net_shop_info.shop_name
            shop.shop_addr = net_shop_info.shop_addr
            shop.front_img = net_shop_info.front_img
            shop.shipping_time = net_shop_info.shipping_time
            shop.shop_score = net_shop_info.shop_score
            shop.save()
        logger.info('评分更新: ' + str(shop_id_start) + ', ' + str(shop_id_end))
    except Exception as e:
        # print(e)
        logger.error(e)


# 获取订单
def req_orders(shop_id_start, shop_id_end):
    try:
        shop_list = ShopModel.objects.filter(id__gte=shop_id_start, id__lte=shop_id_end).values()
        for shop_data in shop_list:
            shop_code = shop_data['shop_code']
            shop_id = shop_data['id']
            shop_type = shop_data['shop_type']
            status = get_service_status(shop_id, constant.SERVICE_TYPE_GET_ORDERS)
            if not status:
                continue

            service_end_time = shop_data['service_end_time']
            if service_end_time <= datetime.datetime.now():  # 过期
                # print('服务已过期')
                continue

            delivery_start_time = shop_data['delivery_start_time']
            delivery_end_time = shop_data['delivery_end_time']
            time_validate = waimai_util.check_delivery_time(delivery_start_time, delivery_end_time)
            if not time_validate:
                continue

            if shop_type == constant.SHOP_TYPE_MT:
                mt_business_user_crawler.req_history_order_info(shop_code)
                logger.info('meituan req_history_order_info end')
            elif shop_type == constant.SHOP_TYPE_ELM:
                elm_business_user_crawler.req_history_order_info(shop_code)
                logger.info('eleme req_history_order_info end')
    except Exception as e:
        # print(e)
        logger.error(e)


# 自动回复
def auto_reply(shop_id_start, shop_id_end):
    try:
        shop_list = ShopModel.objects.filter(id__gte=shop_id_start, id__lte=shop_id_end).values()
        for shop_data in shop_list:
            shop_code = shop_data['shop_code']
            shop_type = shop_data['shop_type']
            shop_id = shop_data['id']
            status, service_config = get_service_status(shop_id, constant.SERVICE_TYPE_SMART_REPLY_COMMENT)
            if not status:
                continue

            service_end_time = shop_data['service_end_time']
            if service_end_time <= datetime.datetime.now():  # 过期
                # print('服务已过期')
                continue

            delivery_start_time = shop_data['delivery_start_time']
            delivery_end_time = shop_data['delivery_end_time']
            time_validate = waimai_util.check_delivery_time(delivery_start_time, delivery_end_time)
            if not time_validate:
                continue

            if waimai_util.is_null_or_empty(service_config):
                continue
            reply_str = service_config

            if shop_type == constant.SHOP_TYPE_MT:
                mt_business_user_crawler.auto_reply(shop_code, reply_str)
                logger.info('meituan auto_reply info end')
            elif shop_type == constant.SHOP_TYPE_ELM:
                elm_business_user_crawler.auto_reply(shop_code, reply_str)
                logger.info('eleme auto_reply info end')
    except Exception as e:
        # print(e)
        logger.error(e)


# 辅助出餐
def automatic_dining(shop_id_start, shop_id_end):
    try:
        shop_list = ShopModel.objects.filter(id__gte=shop_id_start, id__lte=shop_id_end).values()
        for shop_data in shop_list:
            shop_code = shop_data['shop_code']
            shop_id = shop_data['id']
            shop_type = shop_data['shop_type']
            status, service_config = get_service_status(shop_id, constant.SERVICE_TYPE_ASSIST_OUT_ORDER)
            complete_meal_time = 3
            if not status:
                continue

            service_end_time = shop_data['service_end_time']
            if service_end_time <= datetime.datetime.now():  # 过期
                # print('服务已过期')
                continue

            delivery_start_time = shop_data['delivery_start_time']
            delivery_end_time = shop_data['delivery_end_time']
            time_validate = waimai_util.check_delivery_time(delivery_start_time, delivery_end_time)
            if not time_validate:
                continue

            if not waimai_util.is_null_or_empty(service_config):
                tmp_comlete_meal_time = int(service_config)
                if tmp_comlete_meal_time > complete_meal_time:
                    complete_meal_time = tmp_comlete_meal_time

            if shop_type == constant.SHOP_TYPE_MT:
                mt_business_user_crawler.req_all_pre_meal_info(shop_code, complete_meal_time)
                logger.info('meituan automatic_dining info end')
            elif shop_type == constant.SHOP_TYPE_ELM:
                elm_business_user_crawler.req_all_pre_meal_info(shop_code, complete_meal_time)
                logger.info('eleme automatic_dining info end')
    except Exception as e:
        # print(e)
        logger.error(e)
