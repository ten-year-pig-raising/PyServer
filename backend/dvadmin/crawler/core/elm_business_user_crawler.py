import time
from datetime import datetime
import json
import requests
from dvadmin.crawler import constant
from dvadmin.crawler.models import ShopModel
from dvadmin.crawler.util import waimai_util
from dvadmin.crawler.views.order import OrderCreateSerializer
from dvadmin.crawler.views.shop_comments import ShopCommentCreateSerializer
import logging

logger = logging.getLogger(__name__)


def req_history_order_by_page(shop_code, md5_str, form_json, offset):
    end_request = False  # 当查找到评论数据md5值等于 md5_str 则停止查找， end_request则为True
    if len(md5_str) == 0:
        end_request = True

    order_dict = {'list': [], 'end_request': end_request, 'session_expired': False}
    url = 'https://app-api.shop.ele.me/fulfill/weborder/queryAllOrders/?method=OrderWebService.queryAllOrders'

    begin_time = waimai_util.get_pre_days_str(waimai_util.get_zero_today_timestamp(), 1)
    end_time = waimai_util.get_last_today_str()

    form_json['params']['condition']['limit'] = 10
    form_json['params']['condition']['offset'] = offset
    form_json['params']['condition']['beginTime'] = begin_time
    form_json['params']['condition']['endTime'] = end_time
    headers = {
        'User-Agent': ('Mozilla/5.0 (Linux; Android 7.1.2; HD1910 Build/N2G48H) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/68.0.3440.70 Mobile Safari/537.36'),
    }
    req = requests.post(url=url, headers=headers, json=form_json)
    status_code = req.status_code
    if status_code != 200:
        logger.error('eleme: req_history_order_info: error ' + str(status_code) + ' shop_code: ' + str(shop_code))
        order_dict['session_expired'] = True
        order_dict['end_request'] = True
        return order_dict

    json_str = req.json()
    result_json = json_str['result']
    if not result_json:
        logger.error('req_history_order_info result_json is null nor empty shop_code: ' + str(shop_code))
        order_dict['session_expired'] = True
        order_dict['end_request'] = True
        return order_dict

    wm_order_json = result_json['orders']

    order_list = []
    for result_item in wm_order_json:
        tmp_order_id = result_item['id']  # 订单ID
        tmp_order_id = str(tmp_order_id)

        if md5_str == tmp_order_id:  # 找到最近的订单
            end_request = True
            break

        header_dict = result_item['header']
        plan_deliver_time = header_dict['planDeliverTime']  # 预计到达时间的 timestamp
        user_info = result_item['userInfo']
        custom_phones = user_info['ticketCustomerPhones']
        custom_phones_len = len(custom_phones)

        # 订单基本信息
        order_seq_id = header_dict['daySn']  # 订单当天的序列号 例如： 1
        order_id = tmp_order_id  # 订单ID
        order_time = result_item['activeTime'].replace('T', ' ')  # 订单的下单时间
        arrival_time = waimai_util.get_time_format_ms_str(plan_deliver_time)  # 预计到达时间

        # 客户信息
        address = user_info['consigneeAddress']
        recipient_name = user_info['consigneeName']  # 客户名
        recipient_phone = ''  # 客户电话
        privacy_phone = ''
        backup_privacy_phones = ''
        if custom_phones_len == 2:
            privacy_phone = custom_phones[0].replace(" ", "")  # 客户私密电话
            backup_privacy_phones = custom_phones[1].replace(" ", "")  # 客户备用电话

        # 菜品信息
        food_list = []
        xiaoji = 0  # 小计 支付
        food_groups = result_item['foodInfo']['groups']
        for food_group in food_groups:
            food_items = food_group['items']
            for food_item in food_items:
                food_name = food_item['name']
                food_price = food_item['price']
                food_quantity = food_item['quantity']
                food_total = food_item['total']
                tmp_food_item = {
                    'food_name': food_name,
                    'food_price': food_price,
                    'food_quantity': food_quantity,
                    'food_total': food_total
                }
                xiaoji += food_total
                food_list.append(tmp_food_item)
        menu_json = json.dumps(food_list, ensure_ascii=False)

        # 结算信息
        settle_info = result_item['settlementInfo']
        custom_paid_info = settle_info['customerPaidInfo']
        merchant_paid_info = settle_info['merchantActivityInfo']
        platform_paid_info = settle_info['platformServiceFeeInfo']
        new_platform_paid_info = settle_info['newPlatformServiceFeeInfo']
        expected_income_info = settle_info['expectedIncomeInfo']

        xiaoji_paid = round(xiaoji, 2)  # 小计

        # 商家活动支出
        if merchant_paid_info:
            tmp_merchant_paid = merchant_paid_info['total']
            if tmp_merchant_paid:
                merchant_paid = 0 - float(tmp_merchant_paid)
            else:
                merchant_paid = ''
        else:
            merchant_paid = ''

        # 平台服务费
        platform_paid = 0
        if platform_paid_info:
            tmp_platform_paid = platform_paid_info['total']
            if tmp_platform_paid:
                platform_paid = 0 - float(tmp_platform_paid)
        elif new_platform_paid_info:
            tmp_platform_paid = new_platform_paid_info['total']
            if tmp_platform_paid:
                platform_paid = 0 - float(tmp_platform_paid)

        expected_income = expected_income_info['total']  # 本单预计收入
        final_paid = custom_paid_info['total']  # 顾客实际支付

        # 结算dict
        settle_dict = {
            'xiaoji_paid': xiaoji_paid,  # 小计
            'merchant_paid': merchant_paid,  # 商家活动支出
            'platform_paid': platform_paid,  # 平台服务费
            'expected_income': expected_income,  # 本单预计收入
            'final_paid': final_paid  # 顾客实际支付
        }
        settle_json = json.dumps(settle_dict, ensure_ascii=False)

        # 数据库data
        order_data = {
            'shop_code': shop_code,
            'shop_type': constant.SHOP_TYPE_ELM,
            'order_seq_id': order_seq_id,
            'order_id': order_id,
            'order_time': datetime.strptime(order_time, "%Y-%m-%d %H:%M:%S"),
            'arrival_time': arrival_time,
            'address': address,
            'recipient_name': recipient_name,
            'recipient_phone': recipient_phone,
            'privacy_phone': privacy_phone,
            'backup_privacy_phones': backup_privacy_phones,
            'menu_json': menu_json,
            'settle_json': settle_json
        }
        order_list.append(order_data)

    order_dict['list'] = order_list
    order_dict['end_request'] = end_request
    return order_dict


def req_history_order_info(shop_code):
    shop = ShopModel.objects.get(shop_code=shop_code, shop_type=constant.SHOP_TYPE_ELM)
    if not shop:
        logger.exception('eleme req_order_info: shop is null shop_code: ' + str(shop_code))
        return

    session_order = shop.session_order
    if waimai_util.is_null_or_empty(session_order):
        logger.exception('eleme: req_order_info session_order is null or empty shop_code: ' + shop_code)
        return

    last_order_md5 = shop.last_order_md5
    if not last_order_md5:
        last_order_md5 = ''

    offset = 0
    form_json = json.loads(session_order)
    order_dict = req_history_order_by_page(shop_code, last_order_md5, form_json, offset)
    while not order_dict['end_request']:
        time.sleep(0.5)
        offset = offset + 10
        tmp_order_dict = req_history_order_by_page(shop_code, last_order_md5, form_json, offset)
        tmp_order_list = tmp_order_dict['list']
        order_dict['end_request'] = tmp_order_dict['end_request']
        if len(tmp_order_list) > 0:
            order_dict['list'].extend(tmp_order_list)

        if len(order_dict['list']) >= 30:  # 强制退出，避免可能出现死循环
            break

    order_list = order_dict['list']
    order_list.reverse()

    # 保存订单信息到数据库
    for order_data in order_list:
        serializer = OrderCreateSerializer(data=order_data)
        serializer.is_valid()
        serializer.create(validated_data=order_data)

    if order_dict['session_expired']:
        shop.session_expired = True

    # 循环结束  更新最新的order_md5值
    order_list_len = len(order_list)
    if order_list_len > 0:
        tmp_order = order_list[order_list_len - 1]
        last_order_md5 = tmp_order['order_id']
        shop.last_order_md5 = last_order_md5
        shop.save()


# begin_time : 2022-11-27T00:00:00
# end_time: 2022-11-28T23:59:59
# 请求正在进行中的订单, 进行中的订单，一次轮循时间不得超过30分钟
def req_order_info(shop_code):
    shop = ShopModel.objects.get(shop_code=shop_code, shop_type=constant.SHOP_TYPE_ELM)
    if not shop:
        logger.exception('eleme req_order_info: shop is null shop_code: ' + str(shop_code))
        return

    session_order = shop.session_order
    if waimai_util.is_null_or_empty(session_order):
        logger.exception('eleme: req_order_info session_order is null or empty shop_code: ' + shop_code)
        return

    last_order_md5 = shop.last_order_md5
    if not last_order_md5:
        last_order_md5 = ''

    # begin_time = waimai_util.get_pre_days_str(waimai_util.get_current_timestamp_ms(), 1)
    # end_time = waimai_util.get_last_today_str()
    url = 'https://app-api.shop.ele.me/fulfill/weborder/queryInProcessOrders/?method=OrderWebService.queryInProcessOrders'
    form_json = json.loads(session_order)

    # offset = 0
    # form_json['params']['condition']['offset'] = offset
    # form_json['params']['condition']['beginTime'] = begin_time
    # form_json['params']['condition']['endTime'] = end_time
    headers = {
        # 'content-type': 'application/json;charset=UTF-8',
        # 'origin': 'https://napos-order-pc.faas.ele.me',
        # 'x-shard': 'shopid=145319098',
        # 'x-eleme-requestid': '9F72508395614A37811D632A2823556B|1669620055537',
        'User-Agent': ('Mozilla/5.0 (Linux; Android 7.1.2; HD1910 Build/N2G48H) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/68.0.3440.70 Mobile Safari/537.36'),
        # 'referer': 'https://napos-order-pc.faas.ele.me/'
    }
    req = requests.post(url=url, headers=headers, json=form_json)
    status_code = req.status_code
    if status_code != 200:
        shop.session_expired = True
        logger.error('eleme: req_order_info: error ' + str(status_code) + ' shop_code: ' + str(shop_code))
        return

    json_str = req.json()
    result_json = json_str['result']
    if not result_json:
        # 数据test 代码
        # with open('/Users/hs/Desktop/X_Project/X_Python/PyServer/backend/crawler/order.json') as f:
        #     json_str = json.load(f)
        # result_json = json_str['result']
        shop.session_expired = True
        logger.error('req_order_info result_json is null nor empty shop_code: ' + str(shop_code))
        return
    # print(result_json)
    latest_order_id = None
    for result_item in result_json:
        tmp_order_id = result_item['id']  # 订单ID

        if not latest_order_id:
            latest_order_id = tmp_order_id  # 记录下最新的订单ID

        if last_order_md5 == tmp_order_id:  # 找到最近的订单
            break

        header_dict = result_item['header']
        plan_deliver_time = header_dict['planDeliverTime']  # 预计到达时间的 timestamp
        user_info = result_item['userInfo']
        custom_phones = user_info['ticketCustomerPhones']
        custom_phones_len = len(custom_phones)

        # 订单基本信息
        order_seq_id = header_dict['daySn']  # 订单当天的序列号 例如： 1
        order_id = tmp_order_id  # 订单ID
        order_time = result_item['activeTime'].replace('T', ' ')  # 订单的下单时间
        arrival_time = waimai_util.get_time_format_ms_str(plan_deliver_time)  # 预计到达时间

        # 客户信息
        address = user_info['consigneeAddress']
        recipient_name = user_info['consigneeName']  # 客户名
        recipient_phone = ''   # 客户电话
        privacy_phone = ''
        backup_privacy_phones = ''
        if custom_phones_len == 2:
            privacy_phone = custom_phones[0].replace(" ", "")  # 客户私密电话
            backup_privacy_phones = custom_phones[1].replace(" ", "")  # 客户备用电话

        # 菜品信息
        food_list = []
        xiaoji = 0  # 小计 支付
        food_groups = result_item['foodInfo']['groups']
        for food_group in food_groups:
            food_items = food_group['items']
            for food_item in food_items:
                food_name = food_item['name']
                food_price = food_item['price']
                food_quantity = food_item['quantity']
                food_total = food_item['total']
                tmp_food_item = {
                    'food_name': food_name,
                    'food_price': food_price,
                    'food_quantity': food_quantity,
                    'food_total': food_total
                }
                xiaoji += food_total
                food_list.append(tmp_food_item)
        menu_json = json.dumps(food_list, ensure_ascii=False)

        # 结算信息
        settle_info = result_item['settlementInfo']
        custom_paid_info = settle_info['customerPaidInfo']
        merchant_paid_info = settle_info['merchantActivityInfo']
        platform_paid_info = settle_info['platformServiceFeeInfo']
        new_platform_paid_info = settle_info['newPlatformServiceFeeInfo']
        expected_income_info = settle_info['expectedIncomeInfo']

        xiaoji_paid = round(xiaoji, 2)                           # 小计

        # 商家活动支出
        if merchant_paid_info:
            tmp_merchant_paid = merchant_paid_info['total']
            if tmp_merchant_paid:
                merchant_paid = 0 - float(tmp_merchant_paid)
            else:
                merchant_paid = ''
        else:
            merchant_paid = ''

        # 平台服务费
        platform_paid = 0
        if platform_paid_info:
            tmp_platform_paid = platform_paid_info['total']
            if tmp_platform_paid:
                platform_paid = 0 - float(tmp_platform_paid)
        elif new_platform_paid_info:
            tmp_platform_paid = new_platform_paid_info['total']
            if tmp_platform_paid:
                platform_paid = 0 - float(tmp_platform_paid)

        expected_income = expected_income_info['total']   # 本单预计收入
        final_paid = custom_paid_info['total']            # 顾客实际支付

        # 结算dict
        settle_dict = {
            'xiaoji_paid': xiaoji_paid,       # 小计
            'merchant_paid': merchant_paid,   # 商家活动支出
            'platform_paid': platform_paid,   # 平台服务费
            'expected_income': expected_income,    # 本单预计收入
            'final_paid': final_paid          # 顾客实际支付
        }
        settle_json = json.dumps(settle_dict, ensure_ascii=False)

        # 数据库data
        order_data = {
            'shop_code': shop_code,
            'shop_type': constant.SHOP_TYPE_ELM,
            'order_seq_id': order_seq_id,
            'order_id': order_id,
            'order_time': datetime.strptime(order_time, "%Y-%m-%d %H:%M:%S"),
            'arrival_time': arrival_time,
            'address': address,
            'recipient_name': recipient_name,
            'recipient_phone': recipient_phone,
            'privacy_phone': privacy_phone,
            'backup_privacy_phones': backup_privacy_phones,
            'menu_json': menu_json,
            'settle_json': settle_json
        }
        # print(order_data)
        # 保存订单信息到数据库
        serializer = OrderCreateSerializer(data=order_data)
        serializer.is_valid()
        serializer.create(validated_data=order_data)

    # 循环结束  更新最新的order_md5值
    shop.last_order_md5 = latest_order_id
    shop.save()


# 请求待出餐订单信息   辅助出餐 complete_meal_time: 出餐时间
def req_all_pre_meal_info(shop_code, complete_meal_time):
    shop = ShopModel.objects.get(shop_code=shop_code, shop_type=constant.SHOP_TYPE_ELM)
    if not shop:
        logger.exception('eleme: req_all_pre_meal_info shop is null shop_code: ' + str(shop_code))
        return

    session_order = shop.session_order
    if waimai_util.is_null_or_empty(session_order):
        logger.exception('eleme: req_all_pre_meal_info session_order is null or empty shop_code: ' + str(shop_code))
        return

    pre_meal_str = '{"service":"OrderWebService","method":"queryInProcessOrders","params":{"shopId":145319098,"queryType":"COOKING"},"id":"AF10B3A8B4AC4AE5B64DF83C8111C417|1682182780375","metas":{"appVersion":"1.0.0","appName":"melody","ksid":"ZDIWN2MTAwNDM2NTc5NTIyOTAxT3kxN3RHNTVQ","shopId":145319098},"ncp":"2.0.0"}'
    pre_meal_json = json.loads(pre_meal_str)
    url = 'https://app-api.shop.ele.me/fulfill/weborder/queryInProcessOrders/?method=OrderWebService.queryInProcessOrders'

    form_json = json.loads(session_order)
    pre_meal_json['id'] = form_json['id']
    pre_meal_json['metas'] = form_json['metas']
    pre_meal_json['params']['shopId'] = form_json['params']['shopId']

    headers = {
        # 'content-type': 'application/json;charset=UTF-8',
        # 'origin': 'https://napos-order-pc.faas.ele.me',
        # 'x-shard': 'shopid=145319098',
        # 'x-eleme-requestid': '9F72508395614A37811D632A2823556B|1669620055537',
        'User-Agent': ('Mozilla/5.0 (Linux; Android 7.1.2; HD1910 Build/N2G48H) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/68.0.3440.70 Mobile Safari/537.36'),
        # 'referer': 'https://napos-order-pc.faas.ele.me/'
    }
    req = requests.post(url=url, headers=headers, json=pre_meal_json)
    status_code = req.status_code
    if status_code != 200:
        shop.session_expired = True
        logger.error('eleme: req_pre_meal_info: error ' + str(status_code) + ' shop_code: ' + str(shop_code))
        return

    json_str = req.json()
    result_json = json_str['result']
    if not result_json:
        # 数据test 代码
        # with open('/Users/hs/Desktop/X_Project/X_Python/PyServer/backend/crawler/order.json') as f:
        #     json_str = json.load(f)
        # result_json = json_str['result']
        shop.session_expired = True
        logger.error('req_order_info result_json is null nor empty shop_code: ' + str(shop_code))
        return
    dinning_url = 'https://app-api.shop.ele.me/fulfill/weborder/mealComplete/?method=ShipmentService.mealComplete'
    dinning_form_json = {
        'service': 'ShipmentService',
        'method': 'mealComplete',
        'params': {
            'orderId': '',
            'shopId': form_json['params']['shopId'],
        },
        'id': form_json['id'],
        'metas': form_json['metas'],
        'ncp': form_json['ncp']
    }
    # print(dinning_form_json)
    for result_item in result_json:
        time.sleep(1)
        order_id = result_item['id']  # 订单ID
        order_time_str = result_item['activeTime'].replace('T', ' ')
        # print(order_id + ' ' + order_time_str)

        # 下单时间
        order_time = datetime.strptime(order_time_str, "%Y-%m-%d %H:%M:%S")
        dinning_time = order_time.timestamp() + complete_meal_time * 60  # 下单时间，往后推5分钟后再可出餐
        current_timestamp = datetime.now().timestamp()
        if current_timestamp < dinning_time:   # 小于出餐时间
            print('eleme: 当前时间小于出餐时间 order_id ' + str(order_id))
            continue

        dinning_form_json['params']['orderId'] = order_id
        re = requests.post(url=dinning_url, headers=headers, json=dinning_form_json)
        # print(re)
        if re.status_code == 200:
            logger.info('eleme: req_all_pre_meal_info 自动出餐成功 order_id: ' + str(order_id))
        else:
            logger.error('eleme: req_all_pre_meal_info 自动出餐失败 order_id: ' + str(order_id))


# 通过商家账号获取评论
def req_comments_by_page(current_page, md5_str, warning_score, session_comment):
    end_request = False  # 当查找到评论数据md5值等于 md5_str 则停止查找， end_request则为True
    if len(md5_str) == 0:
        end_request = True

    comments_dict = {'list': [], 'end_request': end_request, 'session_expired': False}
    start_time = waimai_util.get_pre_days_str(waimai_util.get_zero_today_timestamp(), 5)
    end_time = waimai_util.get_last_today_str()

    # print('start time is: ' + start_time)
    # print('end time is: ' + end_time)

    url = 'https://app-api.shop.ele.me/ugc/invoke/?method=ShopRatingService.getRateResult'
    form_json = session_comment
    form_json['params']['rateQuery']['currentPage'] = current_page
    form_json['params']['rateQuery']['startTime'] = start_time
    form_json['params']['rateQuery']['endTime'] = end_time
    form_json['params']['rateQuery']['offset'] = (current_page - 1) * 10

    shop_code = form_json['metas']['shopId']
    headers = {
        # 'content-type': 'application/json;charset=UTF-8',
        'User-Agent': ('Mozilla/5.0 (Linux; Android 7.1.2; HD1910 Build/N2G48H) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/68.0.3440.70 Mobile Safari/537.36'),
    }
    req = requests.post(url=url, headers=headers, json=form_json)
    status_code = req.status_code
    if status_code != 200:
        logger.error('eleme: req_comments: error ' + str(status_code) + ' shop_code ' + str(shop_code))
        comments_dict['session_expired'] = True
        comments_dict['end_request'] = True
        return comments_dict

    json_str = req.json()
    result_json = json_str['result']
    if not result_json:
        logger.error('eleme: req_comments_by_page: result_json is null shop_code ' + str(shop_code))
        comments_dict['session_expired'] = True
        comments_dict['end_request'] = True
        return comments_dict

    # print(result_json)
    rate_infos = result_json['rateInfos']
    if not rate_infos:
        logger.exception('eleme: req_comments_by_page: rate_infos is null')
        comments_dict['end_request'] = True
        return comments_dict

    comment_list = []
    for rate_info in rate_infos:
        comment_dict = {}
        user_name = rate_info['username']  # 顾客名

        order_id = rate_info['orderId']
        if not order_id:
            order_id = ''
        anonymous_rating = rate_info['anonymousRating']  # 是否是匿名评论
        order_rate_info = rate_info['orderRateInfos'][0]
        rate_id = order_rate_info['rateId']

        comment_dict['md5_code'] = rate_id
        # print('rate id is: ' + rate_id)
        if md5_str == rate_id:
            end_request = True
            break  # 查找到了数据， 可以跳出，不再往后查找

        service_score = order_rate_info['serviceRating']  # 整体评价
        # packaging_score = order_rate_info['packageRating']  # 打包评价
        # quality_score = order_rate_info['qualityRating']  # 味道评分

        if service_score >= warning_score:
            continue

        rate_time = order_rate_info['ratingAt']  # 评价时间
        replied = order_rate_info['replied']  # 是否有回复
        comment = order_rate_info['ratingContent']  # 评价内容
        if not comment:
            comment = ''

        reply_at = order_rate_info['replyAt']  # 回复时间
        # reply_content = order_rate_info['replyContent']  # 回复内容
        # if not reply_content:
        #     reply_content = ''

        comment_dict['user_name'] = user_name
        comment_dict['order_id'] = order_id
        comment_dict['anonymous_rating'] = anonymous_rating
        comment_dict['rate_id'] = rate_id
        comment_dict['rate_time'] = rate_time
        comment_dict['replied'] = replied
        comment_dict['rate_content'] = comment
        comment_dict['reply_at'] = reply_at
        comment_dict['reply_content'] = ''
        comment_dict['service_score'] = service_score
        # comment_dict['package_score'] = packaging_score
        # comment_dict['quality_score'] = quality_score

        # comment_str = str(comment_dict)
        # md5_gen.update(comment_str.encode())
        # tmp_md5_code = md5_gen.hexdigest()
        # comment_dict['md5_code'] = tmp_md5_code

        # if md5_str == tmp_md5_code:
        #     end_request = True
        #     break  # 查找到了数据， 可以跳出，不再往后查找

        comment_list.append(comment_dict)

    comments_dict['list'] = comment_list
    comments_dict['end_request'] = end_request
    return comments_dict


# 请求评论信息 ： 第一次请求评价信息时，只请求第一页的评价信息
# # eleme的接口 不需要cookie信息
def req_all_comments_by_business_account(shop_id, warning_score):
    shop = ShopModel.objects.get(id=shop_id)
    if not shop:
        logger.exception('eleme req_all_comments_by_business_account: shop is null shop_id:  ' + str(shop_id))
        return

    shop_name = shop.shop_name
    # 初始化，当md5_str是NONE时，初始化为空字符串
    md5_str = shop.last_comment_md5
    if not md5_str:
        md5_str = ''

    session_order = shop.session_order
    if waimai_util.is_null_or_empty(session_order):
        logger.exception('eleme: req_all_comments_by_business_account session_comment is null shop_id: ' + str(shop_id))
        return
    else:
        session_order = json.loads(session_order)

    comment_str = '{"service":"ShopRatingService","method":"getRateResult","params":{"rateQuery":{"shopIds":[145319098],"startTime":"2023-03-24T00:00:00","endTime":"2023-04-23T23:59:59","isReplied":null,"rateType":"ALL","rateSourceType":"ELEME","rateContentType":"ALL","currentPage":1,"offset":0,"limit":10}},"id":"03A42948CB4C47F38F49E4EA08FBFD53|1682183348890","metas":{"appVersion":"1.0.0","appName":"melody","ksid":"ZDIWN2MTAwNDM2NTc5NTIyOTAxT3kxN3RHNTVQ","shopId":145319098},"ncp":"2.0.0"}'
    comment_json = json.loads(comment_str)

    shop_id_list = [session_order['params']['shopId']]
    comment_json['id'] = session_order['id']
    comment_json['metas'] = session_order['metas']
    comment_json['params']['rateQuery']['shopIds'] = shop_id_list

    current_page = 1
    md5_len = len(md5_str)

    comments_dict = req_comments_by_page(current_page, md5_str, warning_score, comment_json)
    if md5_len > 0:
        while not comments_dict['end_request']:
            time.sleep(1)
            current_page = current_page + 1
            tmp_comments_dict = req_comments_by_page(current_page, md5_str, warning_score, comment_json)
            tmp_comment_list = tmp_comments_dict['list']
            end_request = tmp_comments_dict['end_request']
            comments_dict['end_request'] = end_request

            comment_len = len(tmp_comment_list)
            if comment_len > 0:
                comments_dict['list'].extend(tmp_comment_list)

    comment_list = comments_dict['list']
    last_md5_code = None
    if len(comment_list) > 0:
        comment = comment_list[0]
        last_md5_code = comment['md5_code']

    # print('last_md5_code -------------- ' + last_md5_code)

    message_list = []
    for tmp_comment in comment_list:
        param1 = '饿了么:' + shop_name
        if len(param1) > 20:
            param1 = param1[0:19]

        param4 = tmp_comment['rate_content']
        if len(param4) > 20:
            param4 = param4[0:19]
        elif len(param4) == 0:
            param4 = '暂无评价'

        tmp_user_name = tmp_comment['user_name']
        user_full_name = tmp_comment['user_name']
        if tmp_user_name == 'UGC_ANONYMOUS_USER':
            tmp_user_name = '匿名用户'
            user_full_name = '匿名用户'
        if len(tmp_user_name) > 12:
            tmp_user_name = tmp_user_name[0:12] + '..'
        tmp_user_name = '(' + tmp_user_name + ')'

        rate_time = tmp_comment['rate_time']
        format_rate_time = rate_time.replace('T', ' ')
        param5 = rate_time[0:10]

        tmp_service_score = tmp_comment['service_score']
        tmp_service_score = float(tmp_service_score)
        param2 = tmp_comment['order_id']
        if waimai_util.is_null_or_empty(param2):
            param2 = tmp_comment['rate_id']
        comment_param = {
            'param1': param1,
            'param2': param2,
            'param3': str(tmp_service_score) + tmp_user_name,
            'param4': param4,
            'param5': param5
        }
        #  todo 存储数据到数据库
        comment_data = {
            'rate_id':  tmp_comment['rate_id'],
            'order_id': tmp_comment['order_id'],
            'user_name':  user_full_name,
            'comment_time': datetime.strptime(format_rate_time, "%Y-%m-%d %H:%M:%S"),
            'score': tmp_comment['service_score'],
            'content': tmp_comment['rate_content'],
            'shop_reply_content': tmp_comment['reply_content'],
            'shop_type': constant.SHOP_TYPE_ELM,
            'shop_id': shop,
            'shop_name': shop_name
        }
        serializer = ShopCommentCreateSerializer(data=comment_data)
        serializer.is_valid()
        serializer.create(validated_data=comment_data)

        message_list.append(comment_param)

    # 将last_comment_md5 更新为最近的评价
    if last_md5_code:
        shop.last_comment_md5 = last_md5_code

    # 如果session 过期，标识出来
    if comments_dict['session_expired']:
        shop.session_expired = True

    shop.save()

    return message_list


# 自动回复： 每一次最多回复10条评价
def auto_reply(shop_code, reply_str):
    shop = ShopModel.objects.get(shop_code=shop_code, shop_type=constant.SHOP_TYPE_ELM)
    if not shop:
        logger.exception('eleme: auto_reply shop is null shop_code: ' + str(shop_code))
        return

    session_order = shop.session_order
    if waimai_util.is_null_or_empty(session_order):
        logger.exception('eleme: auto_reply session_comment is null shop_code: ' + str(shop_code))
        return
    else:
        session_order = json.loads(session_order)

    comment_str = '{"service":"ShopRatingService","method":"getRateResult","params":{"rateQuery":{"shopIds":[145319098],"startTime":"2023-03-24T00:00:00","endTime":"2023-04-23T23:59:59","isReplied":null,"rateType":"ALL","rateSourceType":"ELEME","rateContentType":"ALL","currentPage":1,"offset":0,"limit":10}},"id":"03A42948CB4C47F38F49E4EA08FBFD53|1682183348890","metas":{"appVersion":"1.0.0","appName":"melody","ksid":"ZDIWN2MTAwNDM2NTc5NTIyOTAxT3kxN3RHNTVQ","shopId":145319098},"ncp":"2.0.0"}'
    form_json = json.loads(comment_str)

    shop_id_list = [session_order['params']['shopId']]
    form_json['id'] = session_order['id']
    form_json['metas'] = session_order['metas']
    form_json['params']['rateQuery']['shopIds'] = shop_id_list

    # session_auto_reply = session.session_auto_reply
    # if not session_auto_reply:
    #     session_auto_reply = ''

    start_time = waimai_util.get_pre_days_str(waimai_util.get_zero_today_timestamp(), 5)
    end_time = waimai_util.get_last_today_str()

    url = 'https://app-api.shop.ele.me/ugc/invoke/?method=ShopRatingService.getRateResult'
    form_json['params']['rateQuery']['currentPage'] = 1
    form_json['params']['rateQuery']['startTime'] = start_time
    form_json['params']['rateQuery']['endTime'] = end_time
    form_json['params']['rateQuery']['isReplied'] = False
    # form_json['params']['rateQuery']['offset'] = 0

    headers = {
        # 'content-type': 'application/json;charset=UTF-8',
        'User-Agent': ('Mozilla/5.0 (Linux; Android 7.1.2; HD1910 Build/N2G48H) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/68.0.3440.70 Mobile Safari/537.36'),
    }
    req = requests.post(url=url, headers=headers, json=form_json)
    status_code = req.status_code
    if status_code != 200:
        shop.session_expired = True
        logger.error('eleme: req_unreply_comments: error ' + str(status_code) + ' shop_code: ' + str(shop_code))
        return

    json_str = req.json()
    result_json = json_str['result']
    if not result_json:
        shop.session_expired = True
        logger.error('eleme: auto_reply: result_json is null shop_code: ' + str(shop_code))
        return
    rate_infos = result_json['rateInfos']
    if not rate_infos:
        logger.exception('eleme: auto_reply: rate_infos is null shop_code: ' + str(shop_code))
        return

    # print(rate_infos)
    # rate_infos_count = len(rate_infos)
    # print(rate_infos_count)

    # if len(session_auto_reply) == 0:
    #     print('eleme: auto_reply session_auto_reply is null or empty')
    #     return
    reply_url = 'https://app-api.shop.ele.me/ugc/invoke/?method=ShopRatingService.replyRating'
    # auto_reply_param = json.loads(session_auto_reply)
    # auto_reply_param['params']['reply']['content'] = reply_str
    # auto_reply_param['params']['reply']['ratingId'] = 0

    auto_reply_param = {
        'service': 'ShopRatingService',
        'method': 'replyRating',
        'params': {
            'shopId': form_json['metas']['shopId'],
            'reply': {
                'ratingComeFrom': 'ELEME',
                'ratingId': '',
                'ratingType': 'ORDER',
                'content': reply_str,
                'templateId': ''
            }
        },
        'id': form_json['id'],
        'metas': form_json['metas'],
        'ncp': form_json['ncp']
    }

    for rate_info in rate_infos:
        time.sleep(1)
        order_rate_info = rate_info['orderRateInfos'][0]
        rate_id = order_rate_info['rateId']
        auto_reply_param['params']['reply']['ratingId'] = rate_id
        re = requests.post(url=reply_url, headers=headers, json=auto_reply_param)
        # print(re)
        if re.status_code == 200:
            logger.info('eleme: 自动回复评价成功： rateId ' + str(rate_id))
        else:
            logger.error('eleme: 自动回复评价失败： rateId ' + str(rate_id))


if __name__ == '__main__':
    # req_order_info('2022-11-27T00:00:00', '2022-11-28T23:59:59', 0)
    waimai_util.get_zero_today_str()
    # req_pre_meal_info()
    # current_last_day = get_last_today_str()
    # pre_days_str = get_pre_days_str(get_zero_today_timestamp(), 30)
