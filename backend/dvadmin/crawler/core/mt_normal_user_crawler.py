import requests
# import dvadmin.crawler.util.mt_decoder as mt_decoder
import dvadmin.crawler.constant as constant
from dvadmin.crawler.views.normal_session import get_db_cookie


def create_header():
    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'i.waimai.meituan.com',
        'Origin': 'https://h5.waimai.meituan.com',
        'Referer': 'https://h5.waimai.meituan.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}
    return headers


def get_mt_normal_user_cookie():
    cookie = get_db_cookie(constant.SHOP_TYPE_MT)
    return cookie


def get_comments(shop_code):
    url = f'https://i.waimai.meituan.com/openh5/poi/comments'
    headers = create_header()
    headers['Cookie'] = get_mt_normal_user_cookie()
    data = {
        'mtWmPoiId': shop_code,
    }
    last_index = 0
    step = 20
    data['startIndex'] = last_index
    for startIndex in range(0, 1):
        print(data['startIndex'])
        req = requests.post(url=url, headers=headers, data=data)
        result = req.text
        print(result)
        last_index = data['startIndex']
        data['startIndex'] = last_index + step

    # req = requests.post(url=url, headers=headers, data=data)
    # result = req.text
    # print(result)


def get_shop_address(shop_code):
    url = 'https://i.waimai.meituan.com/openh5/poi/info'
    headers = create_header()
    headers['Cookie'] = get_mt_normal_user_cookie()

    data = {
        'mtWmPoiId': shop_code,
        'poi_id_str': '',
    }

    shop_address = ''

    req = requests.post(url=url, headers=headers, data=data)
    status_code = req.status_code
    if status_code != 200:
        print(status_code)
        return shop_address

    result = req.json()
    # print(result)
    result_data = result['data']
    shop_address = result_data['shopAddress']
    return shop_address


def get_shop_info(shop_code):
    url = 'https://i.waimai.meituan.com/openapi/v1/poi/food'
    headers = create_header()
    headers['Cookie'] = get_mt_normal_user_cookie()

    data = {
        'wm_poi_id': shop_code,
        'wm_ctype': 'openapi'
    }
    req = requests.post(url=url, headers=headers, data=data)
    status_code = req.status_code
    if status_code != 200:
        print(status_code)
        return

    result = req.json()
    result_data = result['data']['poi_info']
    # print(result_data)
    res = {
        'shop_name': result_data['name'],
        'shop_addr': result_data['address'],
        'front_img': result_data['pic_url'],
        'shipping_time': result_data['shipping_time'],
        'shop_score': result_data['wm_poi_score']
    }

    shop_name_len = len(res['shop_name'])
    if shop_name_len == 0:
        return None

    # time.sleep(1)
    # encode_address = get_shop_address(shop_code)
    # decode_address = mt_decoder.decode_num(encode_address)
    # res['shop_addr'] = decode_address
    # print(res)
    return res


if __name__ == '__main__':
    # https://h5.waimai.meituan.com/waimai/mindex/home
    # get_comments()
    # res = get_shop_food_info('3314440')
    # print(res)
    # 2507774/4190946/10747987/9535945
    # 12536020
    # get_comments('2507774')
    get_shop_info('2507774')
