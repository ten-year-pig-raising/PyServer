import json
import time
from datetime import datetime
import requests
import dvadmin.crawler.util.waimai_util as waimai_util
from dvadmin.crawler.models import ShopModel
from dvadmin.crawler.views.order import OrderCreateSerializer
from dvadmin.crawler.views.shop_comments import ShopCommentCreateSerializer
import dvadmin.crawler.constant as constant
import logging

logger = logging.getLogger(__name__)


# 通过订单ID, 获取顾客地址
def req_order_address(order_id, cookie, cookie_dict):
    url = 'https://e.waimai.meituan.com/v2/order/receive/processed/r/querywithin3h?'
    region_id = cookie_dict['region_id']
    region_version = cookie_dict['region_version']
    wm_poi_id = cookie_dict['wmPoiId']
    device_uuid = cookie_dict['device_uuid']
    optimus_uuid = device_uuid[1:]
    headers = {
        'User-Agent': ('Mozilla/5.0 (Linux; Android 7.1.2; HD1910 Build/N2G48H) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/68.0.3440.70 Mobile Safari/537.36'),
        'Referer': 'https://e.waimai.meituan.com/new_fe/business_gw',
        'Cookie': cookie
    }

    params = {
        'region_id': region_id,
        'region_version': region_version,
        'orderViewId': order_id,
        'wmPoiId': wm_poi_id,
        'optimus_uuid': optimus_uuid,  # 这个是cookie里的 device_id
        'optimus_risk_level': 71,
        'optimus_code': 10,
        'optimus_partner': 19,
    }

    address = ''
    req = requests.get(url, headers=headers, params=params)

    status_code = req.status_code
    if status_code != 200:
        print('req_order_address: error ' + str(status_code))
        return address

    json_str = req.json()
    if not json_str:
        print('meituan request order address response is null order_id: ' + str(order_id))
        return address

    json_data = json_str['data']
    if not json_data:
        print('meituan request order address response data is null order_id: ' + str(order_id))
        return address

    address = json_data['Recipient_Address']
    if not address:
        address = ''
    # distance = json_data['distance']
    # address = address + ' 距离商家:' + str(distance) + '米'
    return address


def req_history_order_info_by_page(shop_code, md5_str, cookie, cookie_dict, day_seq):
    end_request = False  # 当查找到评论数据md5值等于 md5_str 则停止查找， end_request则为True
    if len(md5_str) == 0:
        end_request = True

    order_dict = {'list': [], 'end_request': end_request, 'session_expired': False, 'min_day_seq': 999}

    url = 'https://e.waimai.meituan.com/gw/api/order/mix/history/list/common?'
    headers = {
        'User-Agent': ('Mozilla/5.0 (Linux; Android 7.1.2; HD1910 Build/N2G48H) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/68.0.3440.70 Mobile Safari/537.36'),
        'Referer': 'https://e.waimai.meituan.com/new_fe/business_gw',
        # 'Content-Type:': 'application/x-www-form-urlencoded',
        'Cookie': cookie
    }

    date_str = waimai_util.get_current_day_str()
    day_str = date_str.replace('-', '')
    day_str_int = int(day_str)
    next_label = ''
    if day_seq:
        if day_seq <= 1:
            order_dict['end_request'] = True
            return order_dict

        next_label = {
            "day": day_str_int,
            "day_seq": day_seq,
            "page": 0
        }
        next_label = json.dumps(next_label)

    params = {
        'region_id': cookie_dict['region_id'],
        'region_version': cookie_dict['region_version'],
        'tag': 'all',
        'startDate:': date_str,
        'endDate': date_str,
        'nextLabel': next_label,
        'lastLabel': '',
        'userId': -1
    }

    # data_str = 'region_id=1000430100&region_version=1575275761&tag=all&startDate=2023-04-22&endDate=2023-04-22&nextLabel=%7B%22day%22%3A20230422%2C%22day_seq%22%3A23%2C%22page%22%3A0%7D&lastLabel=&userId=-1'
    # param_json = waimai_util.format_form_data(param_str)
    # param_json['region_id'] = cookie_dict['region_id']
    # param_json['region_version'] = cookie_dict['region_version']
    # param_json['startDate'] = date_str
    # param_json['endDate'] = date_str
    #
    # if day_seq:
    #     param_json['nextLabel']['day'] = day_str_int
    #     param_json['nextLabel']['day_seq'] = day_seq
    #     param_json['nextLabel']['page'] = 0
    # else:
    #     param_json['nextLabel'] = ''

    req = requests.get(url, headers=headers, params=params)
    status_code = req.status_code
    if status_code != 200:
        logger.error('meituan req_history_order_info_by_page: error ' + str(status_code))
        order_dict['session_expired'] = True
        order_dict['end_request'] = True
        return order_dict

    json_str = req.json()
    json_data = json_str['data']
    if not json_data:
        order_dict['session_expired'] = True
        order_dict['end_request'] = True
        logger.error('meituan request history order: data is null')
        return order_dict

    wm_order_list = json_data['wmOrderList']
    if not wm_order_list:
        logger.exception('meituan request history order: wm_order_list is null')
        order_dict['end_request'] = True
        return order_dict

    order_list = []
    min_day_seq = 999  # max
    for wm_order in wm_order_list:
        common_info = wm_order['commonInfo']
        common_json = json.loads(common_info)

        # 基本订单信息
        order_id = common_json['wm_order_id_view']  # 订单的ID
        order_id_str = str(order_id)

        if md5_str == order_id_str:  # 找到最近的订单
            end_request = True
            break

        order_seq_id = common_json['wm_poi_order_dayseq']  # 订单预列号
        if order_seq_id < min_day_seq:
            min_day_seq = order_seq_id

        if order_seq_id == 1:
            end_request = True

        # order_time = common_json['order_time']  # 订单下单时间  timestamp值
        order_time = common_json['confirmTime']   # 订单下单时间, 要使用confirmTime 而不是order_time    timestamp值
        order_time_str = waimai_util.get_normal_time_format_str(order_time)

        arrival_time = common_json['estimateArrivalTime']  # 订单到达时间 timestamp值
        arrival_time_fmt_str = waimai_util.get_normal_time_format_str(arrival_time)

        root_order = wm_order['orderInfo']
        root_order_json = json.loads(root_order)

        # 客户信息
        user_info = root_order_json['userInfo']
        recipient_name = user_info['recipientName']  # 顾客名
        recipient_phone = ''  # 顾客电话
        privacy_phone = ''  # 隐私号码
        backup_privacy_phones = ''  # 备用号码
        address = ''  # 地址

        pc_phones = None
        recipient_phone_vol = user_info['recipientPhoneVo']
        if recipient_phone_vol:
            pc_recepient_phone = recipient_phone_vol['pcRecipientPhoneVo']
            if pc_recepient_phone:
                pc_phones = pc_recepient_phone['pcPhoneVos']

        if pc_phones:
            for pc_phone in pc_phones:
                title = pc_phone['title']
                pc_phones = pc_phone['phones']
                if not title or not pc_phones:
                    continue
                if len(pc_phones) == 0:
                    continue
                tmp_phone = pc_phones[0].replace(" ", "")
                if title == '顾客电话':
                    recipient_phone = tmp_phone
                elif title == '备用号码':
                    privacy_phone = tmp_phone
                elif title == '隐私号码':
                    backup_privacy_phones = tmp_phone
        else:
            logger.exception('meituan req_order pc_phones is null')

        # mask_address = user_info['mask_address']  # 如果是False,表示地址还没有隐藏， 如果是True表示地址隐藏了
        # if not mask_address:
        #     address = req_order_address(order_id, cookie, cookie_dict)

        order_json = root_order_json['orderInfo']
        copy_button_vol = order_json['copyButtonVo']
        click_copy_content = copy_button_vol['clickCopyContent']  # 订单简介
        content_list = click_copy_content.split('  ')
        if len(content_list) >= 6:
            address = content_list[5]
            if address:
                address = address.replace(' ', '')

        # 菜单信息
        food_list = []
        cart_detail_vols = root_order_json['foodInfo']['cartDetailVos']
        for cart_detail in cart_detail_vols:
            details = cart_detail['details']
            for food_detail in details:
                food_name = food_detail['foodName']
                count = food_detail['count']
                food_origin_price = food_detail['originFoodPrice']
                total_price = count * food_origin_price
                total_price = round(total_price, 2)
                # food_price = food_detail['foodPrice']
                tmp_food_item = {
                    'food_name': food_name,
                    'food_price': food_origin_price,
                    'food_quantity': count,
                    'total_price': total_price
                }
                food_list.append(tmp_food_item)

        # 结算信息
        settle_info = root_order_json['chargeInfo']['fixedSettlementInfo']

        # 添加打包费
        box_price = settle_info['boxpriceTotal']
        box_item = {
            'food_name': '打包费',
            'food_price': box_price,
            'food_quantity': 1,
            'total_price': box_price
        }
        food_list.append(box_item)

        # 商家活动补贴
        activity_amount = settle_info['activityAmount']
        if not activity_amount:
            activity_amount = 0
        else:
            activity_amount = 0 - activity_amount
        activity_item = {
            'food_name': '商家对顾客的活动补贴',
            'food_price': activity_amount,
            'food_quantity': 1,
            'total_price': activity_amount
        }
        food_list.append(activity_item)
        menu_json = json.dumps(food_list, ensure_ascii=False)

        # 结算信息json数据
        food_total_amount = settle_info['foodAmount']  # 商品的总价格
        discount_amount = food_total_amount + activity_amount  # 商品优惠后金额
        discount_amount = round(discount_amount, 2)

        commision_amount = settle_info['commisionAmount']  # 佣金
        if not commision_amount:
            commision_amount = 0
        else:
            commision_amount = 0 - commision_amount

        commision_amount = round(commision_amount, 2)

        expected_income = settle_info['settleAmount']  # 预计收入
        final_paid = settle_info['userPayTotalAmount']  # 顾客实际支付
        delivery_amount = expected_income - discount_amount - commision_amount  # 配送服务费
        delivery_amount = round(delivery_amount, 2)
        # 结算dict
        settle_dict = {
            'discount_amount': discount_amount,  # 商品优惠后金额
            'commision_amount': commision_amount,  # 佣金
            'delivery_amount': delivery_amount,  # 配送服务费
            'expected_income': expected_income,  # 预计收入
            'final_paid': final_paid  # 顾客实际支付
        }
        settle_json = json.dumps(settle_dict, ensure_ascii=False)

        order_data = {
            'shop_code': shop_code,
            'shop_type': constant.SHOP_TYPE_MT,
            'order_seq_id': order_seq_id,
            'order_id': order_id_str,
            'order_time': datetime.strptime(order_time_str, "%Y-%m-%d %H:%M:%S"),
            'arrival_time': arrival_time_fmt_str,
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
    order_dict['min_day_seq'] = min_day_seq
    return order_dict


# 根据商家账号获取历史订单信息
def req_history_order_info(shop_code):
    shop = ShopModel.objects.get(shop_code=shop_code, shop_type=constant.SHOP_TYPE_MT)
    if not shop:
        logger.exception('meituan req_order_info: shop is null shop_code: ' + str(shop_code))
        return

    cookie = shop.session_cookie
    if waimai_util.is_null_or_empty(cookie):
        logger.exception('meituan: req_order_info cookie is null or empty shop_code: ' + str(shop_code))
        return

    cookie_dict = waimai_util.extract_cookies(cookie)
    last_order_md5 = shop.last_order_md5
    if not last_order_md5:
        last_order_md5 = ''

    # 每次进来，先查第一页， 找到就不执行下面的while， 第一页 还没找到，往下翻页
    # 特殊情况：
    # 1. 如果跨天，则前一天的 min_day_seq 不能用了， 但是第一次进来，取的是第一页，故min_day_seq也被正常赋值了。 所以逻辑也正常，没有问题
    # 2. 跨天的时候，如果23:59:30 有新订单， 而上一次定时任务是在23:50:00，则新订单没有获取到， 等下一次定时任务的时候， 已经是第二天。 故而会造成 这一个订单会被漏掉

    order_dict = req_history_order_info_by_page(shop_code, last_order_md5, cookie, cookie_dict, None)

    while not order_dict['end_request']:
        time.sleep(0.5)
        tmp_order_dict = req_history_order_info_by_page(shop_code, last_order_md5, cookie, cookie_dict, order_dict['min_day_seq'])
        tmp_order_list = tmp_order_dict['list']
        order_dict['end_request'] = tmp_order_dict['end_request']
        order_dict['min_day_seq'] = tmp_order_dict['min_day_seq']
        if len(tmp_order_list) > 0:
            order_dict['list'].extend(tmp_order_list)

        if len(order_dict['list']) > 30:  # 强制退出，避免可能出现死循环
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


# 根据商家账号获取订单信息
def req_order_info(shop_code):
    shop = ShopModel.objects.get(shop_code=shop_code, shop_type=constant.SHOP_TYPE_MT)
    if not shop:
        logger.exception('meituan req_order_info: shop is null shop_code: ' + str(shop_code))
        return
    # session_order = session.session_order
    # if waimai_util.is_null_or_empty(session_order):
    #     print('meituan: req_order_info session_order is null or empty')
    #     return

    cookie = shop.session_cookie
    if waimai_util.is_null_or_empty(cookie):
        logger.exception('meituan: req_order_info cookie is null or empty shop_code: ' + str(shop_code))
        return

    cookie_dict = waimai_util.extract_cookies(cookie)
    last_order_md5 = shop.last_order_md5
    if not last_order_md5:
        last_order_md5 = ''

    url = 'https://e.waimai.meituan.com/gw/api/order/mix/unprocessed/list/common?'
    headers = {
        'User-Agent': ('Mozilla/5.0 (Linux; Android 7.1.2; HD1910 Build/N2G48H) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/68.0.3440.70 Mobile Safari/537.36'),
        'Referer': 'https://e.waimai.meituan.com/new_fe/business_gw',
        'Cookie': cookie
    }
    params = {
        'region_id': cookie_dict['region_id'],
        'region_version': cookie_dict['region_version'],
        'tag': 'process',
        'pageSize:': 10,
        'pageNum': 1
    }

    req = requests.get(url, headers=headers, params=params)
    status_code = req.status_code
    if status_code != 200:
        shop.session_expired = True
        logger.error('meituan req_order_info: error ' + str(status_code))
        return
    json_str = req.json()

    # with open('/Users/hs/Desktop/X_Project/X_Python/PyServer/backend/crawler/mt_order.json') as f:
    #     json_str = json.load(f)

    json_data = json_str['data']
    if not json_data:
        shop.session_expired = True
        logger.error('meituan request order: data is null')
        return

    wm_order_list = json_data['wmOrderList']
    if not wm_order_list:
        logger.exception('meituan request order: wm_order_list is null')
        return

    latest_order_id = None
    for wm_order in wm_order_list:
        common_info = wm_order['commonInfo']
        common_json = json.loads(common_info)

        # 基本订单信息
        order_id = common_json['wm_order_id_view']  # 订单的ID
        order_id_str = str(order_id)
        if not latest_order_id:
            latest_order_id = order_id_str  # 记录下最新的订单ID

        if last_order_md5 == order_id_str:  # 找到最近的订单
            break

        order_seq_id = common_json['wm_poi_order_dayseq']  # 订单预列号
        order_time = common_json['order_time']  # 订单下单时间  timestamp值
        order_time_str = waimai_util.get_normal_time_format_str(order_time)

        arrival_time = common_json['estimateArrivalTime']  # 订单到达时间 timestamp值
        arrival_time_fmt_str = waimai_util.get_normal_time_format_str(arrival_time)

        root_order = wm_order['orderInfo']
        root_order_json = json.loads(root_order)

        # 客户信息
        user_info = root_order_json['userInfo']
        recipient_name = user_info['recipientName']  # 顾客名
        recipient_phone = ''  # 顾客电话
        privacy_phone = ''  # 隐私号码
        backup_privacy_phones = ''  # 备用号码
        address = ''           # 地址

        pc_phones = None
        recipient_phone_vol = user_info['recipientPhoneVo']
        if recipient_phone_vol:
            pc_recepient_phone = recipient_phone_vol['pcRecipientPhoneVo']
            if pc_recepient_phone:
                pc_phones = pc_recepient_phone['pcPhoneVos']

        if pc_phones:
            for pc_phone in pc_phones:
                title = pc_phone['title']
                pc_phones = pc_phone['phones']
                if not title or not pc_phones:
                    continue
                if len(pc_phones) == 0:
                    continue
                tmp_phone = pc_phones[0].replace(" ", "")
                if title == '顾客电话':
                    recipient_phone = tmp_phone
                elif title == '备用号码':
                    privacy_phone = tmp_phone
                elif title == '隐私号码':
                    backup_privacy_phones = tmp_phone
        else:
            logger.exception('meituan req_order pc_phones is null')

        # mask_address = user_info['mask_address']  # 如果是False,表示地址还没有隐藏， 如果是True表示地址隐藏了
        # if not mask_address:
        #     address = req_order_address(order_id, cookie, cookie_dict)

        order_json = root_order_json['orderInfo']
        copy_button_vol = order_json['copyButtonVo']
        click_copy_content = copy_button_vol['clickCopyContent']  # 订单简介
        content_list = click_copy_content.split('  ')
        if len(content_list) >= 6:
            address = content_list[5]
            if address:
                address = address.replace(' ', '')

        # 菜单信息
        food_list = []
        cart_detail_vols = root_order_json['foodInfo']['cartDetailVos']
        for cart_detail in cart_detail_vols:
            details = cart_detail['details']
            for food_detail in details:
                food_name = food_detail['foodName']
                count = food_detail['count']
                food_origin_price = food_detail['originFoodPrice']
                total_price = count * food_origin_price
                total_price = round(total_price, 2)
                # food_price = food_detail['foodPrice']
                tmp_food_item = {
                    'food_name': food_name,
                    'food_price': food_origin_price,
                    'food_quantity': count,
                    'total_price': total_price
                }
                food_list.append(tmp_food_item)

        # 结算信息
        settle_info = root_order_json['chargeInfo']['fixedSettlementInfo']

        # 添加打包费
        box_price = settle_info['boxpriceTotal']
        box_item = {
            'food_name': '打包费',
            'food_price': box_price,
            'food_quantity': 1,
            'total_price': box_price
        }
        food_list.append(box_item)

        # 商家活动补贴
        activity_amount = settle_info['activityAmount']
        if not activity_amount:
            activity_amount = 0
        else:
            activity_amount = 0 - activity_amount
        activity_item = {
            'food_name': '商家对顾客的活动补贴',
            'food_price': activity_amount,
            'food_quantity': 1,
            'total_price': activity_amount
        }
        food_list.append(activity_item)
        menu_json = json.dumps(food_list, ensure_ascii=False)

        # 结算信息json数据
        food_total_amount = settle_info['foodAmount']  # 商品的总价格
        discount_amount = food_total_amount + activity_amount  # 商品优惠后金额
        discount_amount = round(discount_amount, 2)

        commision_amount = settle_info['commisionAmount']  # 佣金
        if not commision_amount:
            commision_amount = 0
        else:
            commision_amount = 0 - commision_amount

        commision_amount = round(commision_amount, 2)

        expected_income = settle_info['settleAmount']  # 预计收入
        final_paid = settle_info['userPayTotalAmount']  # 顾客实际支付
        delivery_amount = expected_income - discount_amount - commision_amount  # 配送服务费
        delivery_amount = round(delivery_amount, 2)
        # 结算dict
        settle_dict = {
            'discount_amount': discount_amount,  # 商品优惠后金额
            'commision_amount': commision_amount,  # 佣金
            'delivery_amount': delivery_amount,  # 配送服务费
            'expected_income': expected_income,  # 预计收入
            'final_paid': final_paid  # 顾客实际支付
        }
        settle_json = json.dumps(settle_dict, ensure_ascii=False)

        order_data = {
            'shop_code': shop_code,
            'shop_type': constant.SHOP_TYPE_MT,
            'order_seq_id': order_seq_id,
            'order_id': order_id_str,
            'order_time': datetime.strptime(order_time_str, "%Y-%m-%d %H:%M:%S"),
            'arrival_time': arrival_time_fmt_str,
            'address': address,
            'recipient_name': recipient_name,
            'recipient_phone': recipient_phone,
            'privacy_phone': privacy_phone,
            'backup_privacy_phones': backup_privacy_phones,
            'menu_json': menu_json,
            'settle_json': settle_json
        }
        # 保存订单信息到数据库
        serializer = OrderCreateSerializer(data=order_data)
        serializer.is_valid()
        serializer.create(validated_data=order_data)

    # 循环结束  更新最新的order_md5值
    shop.last_order_md5 = latest_order_id
    shop.save()


# 请求所有未出餐订单, complete_meal_time: 出餐时间
def req_all_pre_meal_info(shop_code, complete_meal_time):
    shop = ShopModel.objects.get(shop_code=shop_code, shop_type=constant.SHOP_TYPE_MT)
    if not shop:
        logger.exception('meituan req_all_pre_meal_info shop is null shop_code: ' + str(shop_code))
        return

    cookie = shop.session_cookie
    if waimai_util.is_null_or_empty(cookie):
        logger.exception('meituan: req_all_pre_meal_info cookie is null or empty shop_code: ' + str(shop_code))
        return

    cookie_dict = waimai_util.extract_cookies(cookie)

    url = 'https://e.waimai.meituan.com/gw/api/order/mix/unprocessed/list/common?'
    headers = {
        'User-Agent': ('Mozilla/5.0 (Linux; Android 7.1.2; HD1910 Build/N2G48H) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/68.0.3440.70 Mobile Safari/537.36'),
        'Referer': 'https://e.waimai.meituan.com/new_fe/business_gw',
        'Cookie': cookie
    }
    params = {
        'region_id': cookie_dict['region_id'],
        'region_version': cookie_dict['region_version'],
        'tag': 'prepMeal',
        'pageSize:': 10,
        'pageNum': 1
    }

    req = requests.get(url, headers=headers, params=params)
    status_code = req.status_code
    if status_code != 200:
        shop.session_expired = True
        logger.error('meituan req_all_pre_meal_info: error ' + str(status_code) + ' shop_code: ' + str(shop_code))
        return
    json_str = req.json()

    json_data = json_str['data']
    if not json_data:
        shop.session_expired = True
        logger.error('meituan req_all_pre_meal_info: json_data is null ' + ' shop_code: ' + str(shop_code))
        return

    wm_order_list = json_data['wmOrderList']
    if not wm_order_list:
        logger.exception('meituan request premeal: wm_order_list is null')
        return

    dinning_url = 'https://e.waimai.meituan.com/v2/common/w/reported/completeMealTime?'
    dinning_params = {
        'region_id': cookie_dict['region_id'],
        'region_version': cookie_dict['region_version'],
        'wmPoiId': cookie_dict['wmPoiId'],
        'wmOrderViewId': ''
    }
    for wm_order in wm_order_list:
        time.sleep(1)
        common_info = wm_order['commonInfo']
        common_json = json.loads(common_info)

        order_id = common_json['wm_order_id_view']  # 订单的ID int类型
        order_id_str = str(order_id)
        order_time = common_json['order_time']      # 订单下单时间  timestamp值
        dinning_time = order_time + complete_meal_time * 60          # 下单时间，往后推5分钟后再可出餐
        current_timestamp = datetime.now().timestamp()
        if current_timestamp < dinning_time:  # 小于出餐时间
            print('meituan: 当前时间小于出餐时间 order_id ' + order_id_str)
            continue

        dinning_params['wmOrderViewId'] = order_id_str
        print(dinning_params)
        re = requests.post(url=dinning_url, headers=headers, params=dinning_params)
        # print(re)
        if re.status_code == 200:
            logger.info('meituan: req_all_pre_meal_info 自动出餐成功 order_id: ' + order_id_str)
        else:
            logger.error('meituan: req_all_pre_meal_info 自动出餐失败 order_id: ' + order_id_str)


# 使用商家账号请求评论信息  最近n天的评论数据的评论信息
def req_comments_by_business_account(page_num, md5_str, warning_score, cookie, cookie_dict):
    end_request = False  # 当查找到评论数据md5值等于 md5_str 则停止查找， end_request则为True
    if len(md5_str) == 0:
        end_request = True

    comments_dict = {'list': [], 'end_request': end_request, 'session_expired': False}

    url = 'https://waimaieapp.meituan.com/gw/customer/comment/list?'
    end_time = waimai_util.get_zero_today_timestamp() - 3600 * 24
    begin_time = waimai_util.get_pre_days(end_time, 5)  # 查找往前5天的评论数据

    # 此处param_str 如果使用 param = {}，手写的形式，会出错， 非法入参。 故而最有效的方式是copy参数，然后解析
    param_str = 'ignoreSetRouterProxy=true&acctId=29386830&wmPoiId=3314440&token=047CtHD018pivjE0WPePU7vzkrPTKds2rcaNvasaovw8%2A&appType=3&commScore=0&commType=-1&hasContent=-1&periodType=4&beginTime=1666627200&endTime=1669305600&pageNum=1&onlyAuditNotPass=0&pageSize=10'
    param_json = waimai_util.format_form_data(param_str)

    param_json['acctId'] = cookie_dict['acctId']
    param_json['wmPoiId'] = cookie_dict['wmPoiId']
    param_json['token'] = cookie_dict['token']
    param_json['beginTime'] = begin_time
    param_json['endTime'] = end_time
    param_json['pageNum'] = page_num
    headers = {
        'User-Agent': ('Mozilla/5.0 (Linux; Android 7.1.2; HD1910 Build/N2G48H) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/68.0.3440.70 Mobile Safari/537.36'),
        'Cookie': cookie
    }
    req = requests.get(url, headers=headers, params=param_json)
    status_code = req.status_code
    if status_code != 200:
        logger.error('meituan req_comments_by_business_account: error ' + str(status_code) + ' shop_code: ' + str(cookie_dict['wmPoiId']))
        comments_dict['session_expired'] = True
        comments_dict['end_request'] = True
        return comments_dict

    result = req.json()
    data = result['data']
    if not data:
        logger.error('meituan req_comments_by_business_account: json data is null shop_code: ' + str(cookie_dict['wmPoiId']))
        comments_dict['session_expired'] = True
        comments_dict['end_request'] = True
        return comments_dict

    data_list = data['list']
    if not data_list:
        logger.info('meituan req_comments_by_business_account: json data is null')
        comments_dict['end_request'] = True
        return comments_dict

    comment_list = []
    for comment in data_list:
        comment_dict = {}

        rate_id = comment['id']
        rate_id_str = str(rate_id)
        comment_dict['md5_code'] = rate_id_str
        if md5_str == rate_id_str:
            end_request = True
            break  # 查找到了数据， 可以跳出，不再往后查找

        # 订单评分大于等于 预警分的 则不处理
        score = comment['orderCommentScore']
        order_id = comment['orderId']
        if score > warning_score:
            continue

        user_name = comment['userName']
        comment_content = comment['cleanComment']
        if not comment_content:
            comment_content = ''
        rate_time = comment['createTime']

        # 'orderCommentScore': comment['orderCommentScore'],  # 订单评分
        # 'foodCommentScore': comment['foodCommentScore'],  # 口味评分
        # 'deliveryCommentScore': comment['deliveryCommentScore'],  # 配送评分
        # 'packagingScore': comment['packagingScore'],  # 打包评分

        comment_dict['user_name'] = user_name
        comment_dict['order_id'] = order_id
        comment_dict['anonymous_rating'] = ''
        comment_dict['rate_id'] = rate_id_str
        comment_dict['rate_time'] = rate_time
        comment_dict['rate_content'] = comment_content
        comment_dict['reply_content'] = ''
        comment_dict['service_score'] = score

        comment_list.append(comment_dict)

    comments_dict['list'] = comment_list
    comments_dict['end_request'] = end_request

    return comments_dict


# 请求所有满足条件的评论信息
# 请求到评论数据md5值， 和md5_str相同则不再往下请求，
# 如果md5_str为空，请求最新的10条评论
def req_all_comments_by_business_account(shop_id, warning_score):
    shop = ShopModel.objects.get(id=shop_id)
    if not shop:
        logger.exception('meituan req_all_comments_by_business_account: shop is null shop_id:  ' + str(shop_id))
        return

    shop_name = shop.shop_name
    md5_str = shop.last_comment_md5
    if not md5_str:
        md5_str = ''

    cookie = shop.session_cookie
    if not cookie:
        logger.exception('meitaun req_all_comments_by_business_account cookie is null shop_id: ' + str(shop_id))
        return

    if len(cookie) == 0:
        logger.exception('meitaun req_all_comments_by_business_account cookie is null shop_id: ' + str(shop_id))
        return
    cookie_dict = waimai_util.extract_cookies(cookie)

    current_page = 1
    md5_len = len(md5_str)

    comments_dict = req_comments_by_business_account(current_page, md5_str, warning_score, cookie, cookie_dict)
    if md5_len > 0:
        while not comments_dict['end_request']:
            time.sleep(1)
            current_page = current_page + 1
            tmp_comments_dict = req_comments_by_business_account(current_page, md5_str, warning_score, cookie, cookie_dict)
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

    message_list = []
    for tmp_comment in comment_list:
        param1 = '美团:' + shop_name
        if len(param1) > 20:
            param1 = param1[0:19]

        param4 = tmp_comment['rate_content']
        if len(param4) > 20:
            param4 = param4[0:19]
        elif len(param4) == 0:
            param4 = '暂无评价'

        tmp_user_name = tmp_comment['user_name']
        if tmp_user_name == 'UGC_ANONYMOUS_USER':
            tmp_user_name = '匿名用户'
        if len(tmp_user_name) > 12:
            tmp_user_name = tmp_user_name[0:12] + '..'
        tmp_user_name = '(' + tmp_user_name + ')'

        rate_time = tmp_comment['rate_time']
        # format_rate_time = rate_time.replace('T', ' ')
        # parma5 = rate_time[0:10]
        param5 = rate_time

        tmp_service_score = tmp_comment['service_score']
        tmp_service_score = float(tmp_service_score)

        param2 = ''
        if tmp_comment['order_id'] > 0:
            param2 = str(tmp_comment['order_id'])
        else:
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
            'rate_id': tmp_comment['rate_id'],
            'order_id': tmp_comment['order_id'],
            'user_name': tmp_comment['user_name'],
            'comment_time': datetime.strptime(rate_time, "%Y-%m-%d"),
            'score': tmp_comment['service_score'],
            'content': tmp_comment['rate_content'],
            'shop_reply_content': tmp_comment['reply_content'],
            'shop_type': constant.SHOP_TYPE_MT,
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
    shop = ShopModel.objects.get(shop_code=shop_code, shop_type=constant.SHOP_TYPE_MT)
    if not shop:
        logger.exception('meituan auto_reply shop is null shop_code ' + str(shop_code))
        return

    cookie = shop.session_cookie
    if waimai_util.is_null_or_empty(cookie):
        logger.exception( 'meituan auto_reply cookie is null or empty shop_code: ' + str(shop_code))
        return
    cookie_dict = waimai_util.extract_cookies(cookie)

    url = 'https://waimaieapp.meituan.com/gw/customer/comment/list?'
    # end_time = waimai_util.get_last_today_timestamp()
    end_time = waimai_util.get_zero_today_timestamp() - 86400     # 当天的时间， 往前一天
    end_time = int(end_time)
    begin_time = waimai_util.get_pre_days(end_time, 5)  # 查找往前n天的评论数据
    begin_time = int(begin_time)
    print(end_time)
    print(begin_time)

    # 此处param_str 如果使用 param = {}，手写的形式，会出错， 非法入参。 故而最有效的方式是copy参数，然后解析
    param_str = 'ignoreSetRouterProxy=true&acctId=29386830&wmPoiId=3314440&token=047CtHD018pivjE0WPePU7vzkrPTKds2rcaNvasaovw8%2A&appType=4&commScore=0&commType=-1&hasContent=-1&periodType=1&beginTime=1666627200&endTime=1669305600&pageNum=1&onlyAuditNotPass=0&pageSize=10'
    param_json = waimai_util.format_form_data(param_str)

    param_json['acctId'] = cookie_dict['acctId']
    param_json['wmPoiId'] = cookie_dict['wmPoiId']
    param_json['token'] = cookie_dict['token']
    param_json['appType'] = 3
    param_json['commScore'] = 0
    param_json['commType'] = 0
    param_json['hasContent'] = -1
    param_json['periodType'] = 4
    param_json['beginTime'] = begin_time
    param_json['endTime'] = end_time
    param_json['pageNum'] = 1
    headers = {
        'User-Agent': ('Mozilla/5.0 (Linux; Android 7.1.2; HD1910 Build/N2G48H) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/68.0.3440.70 Mobile Safari/537.36'),
        'Cookie': cookie
    }
    req = requests.get(url, headers=headers, params=param_json)
    status_code = req.status_code
    if status_code != 200:
        shop.session_expired = True
        logger.error('mt: req unreply comments error ' + str(status_code) + ' shop_code: ' + str(shop_code))
        return

    result = req.json()
    data = result['data']
    if not data:
        shop.session_expired = True
        logger.error('meituan: req unreply comments error: data is null shop_code: ' + str(shop_code))
        return

    data_list = data['list']
    if not data_list:
        logger.exception('meituan: req unreply comments error: data_list is null')
        return

    reply_url = 'https://waimaieapp.meituan.com/gw/customer/comment/reply?ignoreSetRouterProxy=true'
    reply_params = {
        'acctId': cookie_dict['acctId'],
        'wmPoiId': cookie_dict['wmPoiId'],
        'token': cookie_dict['token'],
        'appType': 4,
        'toCommentId': '',
        'comment': reply_str,
        'userCommentCtime': ''
    }
    for comment in data_list:
        time.sleep(1)
        rate_id = comment['id']
        create_time = comment['createTime']
        user_name = comment['userName']
        reply_params['toCommentId'] = rate_id
        reply_params['userCommentCtime'] = create_time

        re = requests.post(url=reply_url, headers=headers, params=reply_params)
        # print(re)
        if re.status_code == 200:
            logger.info('meituan: 自动回复评价成功： rateId ' + str(rate_id) + ' ' + user_name)
        else:
            logger.error('meituan: 自动回复评价失败： rateId ' + str(rate_id) + ' ' + user_name)


if __name__ == '__main__':
    # global_cookie = 'uuid=050459a5b19fc4d0b7b8.1668436508.1.0.0; _lxsdk_cuid=1847690c0efc8-07dd2c2a52bb8c-c4a7526-144000-1847690c0efc8; _lxsdk=1847690c0efc8-07dd2c2a52bb8c-c4a7526-144000-1847690c0efc8; device_uuid=!cc4108b8-83aa-4355-8c63-1517eaf55ef2; uuid_update=true; acctId=29386830; token=047CtHD018pivjE0WPePU7vzkrPTKds2rcaNvasaovw8*; brandId=-1; wmPoiId=3314440; isOfflineSelfOpen=0; city_id=430100; isChain=0; existBrandPoi=false; ignore_set_router_proxy=false; region_id=1000430100; region_version=1522824193; newCategory=false; bsid=8_ZxtR45k3ldNS4bibgNDDhrTAxOj7wr1oNrHShCdq4Bjez-IHYi1J7HxOkdqHSbTEhYHX6JqLfFf5FmBSBAOA; city_location_id=430100; location_id=430111; cityId=430100; provinceId=430000; set_info={"wmPoiId":"3314440","region_id":"1000430100","region_version":1522824193}; pushToken=047CtHD018pivjE0WPePU7vzkrPTKds2rcaNvasaovw8*; shopCategory=food; _lx_utm=utm_source=Baidu&utm_medium=organic; wpush_server_url=wss://wpush.meituan.com; logan_session_token=ygrzzscmwb766pulzl94; setPrivacyTime=1_20221120; _lxsdk_s=18493efb557-6f4-a2d-e42||256 '
    # 从21号开始
    req_order_info('2022-11-28')
    # req_order_address(1300294922256285878)
    # req_all_pre_meal_info()
    # req_all_comments_by_business_account()
