import json
import requests
from dvadmin.crawler.util import waimai_util
from datetime import datetime

form_data = 'jsv=2.6.2&appKey=12574478&t=1669890291562&sign=24470e28ed816a3be531723d44c22d21&api=mtop.alsc.wamai.store.detail.miniapp.business.tab.page&v=1.0&type=originaljson&dataType=json&timeout=15000&subDomain=waimai-guide&mainDomain=ele.me&H5Request=true&ttid=h5%40safari_ios_604.1&data=%7B%22eleStoreId%22%3A%22E8105191740107834450%22%2C%22longitude%22%3A112.979996%2C%22latitude%22%3A28.09225%7D'


def create_header():
    headers = {}
    headers['accept'] = 'application/json'
    headers['accept-encoding'] = 'gzip, deflate, br'
    headers['accept-language'] = 'zh-CN,zh;q=0.9,en;q=0.8'
    headers['connection'] = 'keep-alive'
    headers['content-length'] = '2359'
    headers['content-type'] = 'application/x-www-form-urlencoded'
    headers[
        'cookie'] = 'cna=uGc4GyJpgHICAd73KJbqnDLe; ubt_ssid=u9az2yya4pohp61zxdojjy7hspop633g_2022-11-01; ut_ubt_ssid=au5frs12h69hgz1mzj9wwu5xh99oq1us_2022-11-03; t=a9c947749bc1dc50f02604984ffbe370; _m_h5_tk=286214f18123de64d526e592878fcd22_1669897791324; _m_h5_tk_enc=e9e46be9bebbcfea99bfa9b0175c610a; xlly_s=1; _samesite_flag_=true; cookie2=199252dbfc1669639a188926b3d5fa5e; _tb_token_=e8645e61113b3; sgcookie=E100DgzdWb7pkchvejQxhNX92vp%2BsgXDZ86T63bkEP3W6hesZz%2BZ%2FbKSPX2aoR9f6Z5SdvSD6TUAw8g5sN4HAykK80G0yGPvwZRsPcArCXeyGcc%3D; unb=2210664651987; munb=2210664651987; csg=73fe1713; t_eleuc4=id4=0%40BA%2FvuHCrrAlSWlm2xB%2FsngwC8WonoGw2SkQv%2BQ%3D%3D; USERID=1000158707648; SID=MTk5MjUyZGJmYzE2Njk2MzlhMTg4OTI2YjNkNWZhNWXn_4yDNOZWtjeGccXm-fHe; UTUSER=1000158707648; x5check_ele=TLNXzVCTdNflbl%2BUUnpmbCKkV6AzUeeaAUZS9iK818Q%3D; l=fBx6tsQPTzFHOM7iBOfwPurza77OSIRAguPzaNbMi9fPOsCp5EocW65t6F89C3GRFsiBR38YsXPkBeYBqQd-nxv9C7xZ6fHmnmOk-Wf..; tfstk=cjgPBFbuqULPKF345r4E7oFoWQaRZNo-cQN8qpAaqzqGh-qliLBLiNCqP4jpJuf..; isg=BImJ6Ps4DrDXifKtt_4zcgw6mLXj1n0IanFMqCv-BHCvcquEcyYt2MfgsNBEKhVA'
    headers['origin'] = 'https://h5.ele.me'
    headers['referer'] = 'https://h5.ele.me/'
    headers['sec-fetch-dest'] = 'empty'
    headers['sec-fetch-mode'] = 'cors'
    headers['sec-fetch-site'] = 'same-site'
    headers[
        'User-Agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
    return headers


def format_form_data(data):
    data_array = data.split('&')
    res = {}
    for item in data_array:
        temp = item.split('=')
        res[temp[0]] = temp[1]
    return res


def get_shop_info(shop_code):
    url = 'https://waimai-guide.ele.me/h5/mtop.alsc.wamai.store.detail.miniapp.business.tab.page/1.0/?jsv=2.6.2&appKey=12574478&t=1669890291562&sign=24470e28ed816a3be531723d44c22d21&api=mtop.alsc.wamai.store.detail.miniapp.business.tab.page&v=1.0&type=originaljson&dataType=json&timeout=15000&subDomain=waimai-guide&mainDomain=ele.me&H5Request=true&ttid=h5%40safari_ios_604.1&data=%7B%22eleStoreId%22%3A%22E8105191740107834450%22%2C%22longitude%22%3A112.979996%2C%22latitude%22%3A28.09225%7D'
    headers = create_header()
    # headers[
    #     'Cookie'] = 'uuid=13b3784134d8471ea4be.1667394562.1.0.0; _lxsdk_cuid=1843876cc29c8-06fd288765617e-26021e51-144000-1843876cc2ac8; ci=70; _ga=GA1.1.1016111602.1668953252; wm_order_channel=default; request_source=openh5; au_trace_key_net=default; isIframe=false; WEBDFPID=u65wzzuz3x10589xy2y3458282245xx6815z53zuv8597958x83vuwx5-1984565844800-1669205842725YWQKMWKfd79fef3d01d5e9aadc18ccd4d0c95079036; terminal=i; w_utmz="utm_campaign=(direct)&utm_source=5000&utm_medium=(none)&utm_content=(none)&utm_term=(none)"; iuuid=261E36EA0C923CFDF0EE8F3C119FBEA7CE7684E9B54A7958A5CE697CBA711407; token=AgHMIrk7D4xPIJJqxfO2OPJvgbQO1QkcifwmdcGC5LSl8eUxwbAEh_FNmduY_HG_BuZB9MoMwnY9mwAAAAAkFQAACthpIzsX9YtJt595aNe55sSVhs0wqqhj2FvvuUxpaR2uGDVne04Kd5OYWcES9EJ0; mt_c_token=AgHMIrk7D4xPIJJqxfO2OPJvgbQO1QkcifwmdcGC5LSl8eUxwbAEh_FNmduY_HG_BuZB9MoMwnY9mwAAAAAkFQAACthpIzsX9YtJt595aNe55sSVhs0wqqhj2FvvuUxpaR2uGDVne04Kd5OYWcES9EJ0; oops=AgHMIrk7D4xPIJJqxfO2OPJvgbQO1QkcifwmdcGC5LSl8eUxwbAEh_FNmduY_HG_BuZB9MoMwnY9mwAAAAAkFQAACthpIzsX9YtJt595aNe55sSVhs0wqqhj2FvvuUxpaR2uGDVne04Kd5OYWcES9EJ0; userId=1939188632; _lxsdk=261E36EA0C923CFDF0EE8F3C119FBEA7CE7684E9B54A7958A5CE697CBA711407; openh5_uuid=261E36EA0C923CFDF0EE8F3C119FBEA7CE7684E9B54A7958A5CE697CBA711407; w_token=AgHMIrk7D4xPIJJqxfO2OPJvgbQO1QkcifwmdcGC5LSl8eUxwbAEh_FNmduY_HG_BuZB9MoMwnY9mwAAAAAkFQAACthpIzsX9YtJt595aNe55sSVhs0wqqhj2FvvuUxpaR2uGDVne04Kd5OYWcES9EJ0; openh5_uuid=261E36EA0C923CFDF0EE8F3C119FBEA7CE7684E9B54A7958A5CE697CBA711407; _ga_95GX0SH5GM=GS1.1.1669249551.4.0.1669249551.0.0.0; w_uuid=1iKzfS0Qwz6A_IZWap4Bu9piBl76yFDbZckBhq-mUeNk89hbdWNhdgQ24nerS3vK; utm_source=0; wx_channel_id=0; webp=1; w_cid=430100; w_cpy=changsha; w_cpy_cn="%E9%95%BF%E6%B2%99"; JSESSIONID=uytlxzel6v2b1da9dw9sv72y3; __mta=218881574.1669337850339.1669337876785.1669337876789.6; w_addr=%E5%8C%97%E8%BE%B0%E4%B8%AD%E5%A4%AE%E5%85%AC%E5%9B%ADD%E5%8C%BA%C2%B7%E6%85%A7%E8%BE%B0%E5%9B%AD; bussiness_entry_channel=default; _lx_utm=utm_source%3D; w_visitid=0e335675-fe01-4998-890a-203708043483; channelType={%22default%22:%220%22}; channelConfig={%22channel%22:%22default%22%2C%22type%22:0%2C%22fixedReservation%22:{%22reservationTimeStatus%22:0%2C%22startReservationTime%22:0%2C%22endReservationTime%22:0}}; _yoda_verify_resp=VAo%2FKY64ax8lu%2B8%2BKXxOerUQ9%2BGR3nEsjuRsZJdwK36Np4r153P3eHQDR3yk%2Fk2LEPYk902vy3PMG4ZYPaxTec8WqKpsFW1E5PEo%2F6F6idixYe6GolZZUxLrSFDoqeoy5ZpvfUs90Htbc6O0r%2FdYMhET4nC6O7ZHGKW6bs8g7uv9NnNgoHwY9jBHki90osW0MQFPRcz6e0KD2rHSGW1eVem7FNoqVIuJZ9yVMwCfvmIxC2DV%2BFYCQ4i2cZBiClTx678ZubCgO4nP5WtxKATcLiRyJKoqLw2D05cim4i5zGOkT7aHpq8s7YKQUE3XHs1DQL8cylFpWJW28J1VYH0QctIh4iP2jNXkFGsvqkd7b4DFVs6jL4uXSRfS0ANPj4o%2F; _yoda_verify_rid=162ba1371bc0d05c; cssVersion=1202795c; _lxsdk_s=184c312288d-af6-c15-64a%7C%7C83'
    # params = format_form_data(form_data)
    req = requests.get(url=url, headers=headers)
    result = req.text
    print(result)


def get_shop_score(shop_code, cookie):
    shop_score = '_'
    url = 'https://waimai-guide.ele.me/h5/mtop.alsc.waimai.rate.query.ratescore/1.0/5.0/?jsv=2.7.1&appKey=12574478&t=1678155428386&sign=9a2e9bb68f028a5ae16399ed9146c508&api=mtop.alsc.waimai.rate.query.ratescore&v=1.0&type=originaljson&dataType=json&timeout=10000&subDomain=waimai-guide&mainDomain=ele.me&H5Request=true&ttid=h5@safari_ios_604.1&SV=5.0&data={"restaurantId":"E3261041197452176164"}&bx_et=c4jCByiEq_INt0RZPBwaUVF2hQtcZ-qWIPAcdWXQaXT3-pBCico2GKUNOqLpjd1..'
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'User-Agent': ('Mozilla/5.0 (Linux; Android 7.1.2; HD1910 Build/N2G48H) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/68.0.3440.70 Mobile Safari/537.36'),
        'Cookie': cookie
    }
    req = requests.get(url=url, headers=headers)
    status_code = req.status_code
    if status_code != 200:
        print('eleme: req_waimai_shop_score: error ' + str(status_code))
        return shop_score

    json_str = req.json()
    # print(json_str)
    data_json = json_str['data']
    if not data_json:
        print('req_waimai_shop_info: data_json is null')
        return shop_score

    shop_score = str(data_json['shop_score'])
    return shop_score


# 请求店铺信息
def get_elm_shop_info(shop_code):
    # current_timestamp = waimai_util.get_current_timestamp_ms()
    url = 'https://waimai-guide.ele.me/h5/mtop.alsc.wamai.store.detail.miniapp.business.tab.page/1.0/5.0/?jsv=2.7.1&appKey=12574478&t=1678155189763&sign=ec23c9165d5c288226997147621913f5&api=mtop.alsc.wamai.store.detail.miniapp.business.tab.page&v=1.0&type=originaljson&dataType=json&timeout=10000&subDomain=waimai-guide&mainDomain=ele.me&H5Request=true&ttid=h5@safari_ios_604.1&SV=5.0&data={"eleStoreId":"E3261041197452176164","longitude":113.01582,"latitude":28.121616}&bx_et=c45NBdbcEIjCopCeNBAVU2cKOhiOZuOH1fL6IoGq5UKu8LvGiqmv-zVHWFDYMdf..'
    cookie = 'cna=axv0G0rlvysCAd73XEcwuFVd; ubt_ssid=eb4vwg4riv0ihcc3rn5a2c5yngow35wd_2022-11-24; ut_ubt_ssid=movpj437u0rwdfm240qjg50382xjg8kz_2022-11-24; t=93f51c4aadf662cee99a7e81c03c24d4; tzyy=3beea08db29ebd667a2a4ea1c7b26b77; track_id=1669364120|4f678560b86c72902d247620158291b70a98f567169d8111d3|cbade34aa70dbf3a70f7839219d5b9d4; unb=2208073054573; munb=2208073054573; USERID=1000076227812; UTUSER=1000076227812; x5check_napos=ZGZJZTMTAwNDM2NTc5NTIyOTAxT3VBMjJodjdQ; ksid=ZGZJZTMTAwNDM2NTc5NTIyOTAxT3VBMjJodjdQ; shopId=145319098; _m_h5_tk=072fddd711e306e5e47636e7cdd8c3dd_1678165429919; _m_h5_tk_enc=cbeb3175c66a99a8aee6d9bfc565a201; _samesite_flag_=true; cookie2=17d920d620da5e098eafef4904ddf61b; _tb_token_=5feee7db7a658; sgcookie=E100JQSZYaZrXNqOyPsPU1X8DT9Z9/8Tnnm8cppuIURsjmVfXo9nOpjLij6vP8z8Uzk2KnBqLjhD5FFmSo/Q+WXhmd4icRbmJMVADCk9WsbNkQI=; csg=8876b011; t_eleuc4=id4=0@BA/vuHCrrRUmfD4dizM43ljH1ZjQlOOWuaFGNQ==; SID=MTdkOTIwZDYyMGRhNWUwOThlYWZlZjQ5MDRkZGY2MWLfRss2JSIJO7Nvh104ErN2; x5check_ele=Jpwsk6pcoTTWAiNeZXYKiO5Mj9oBbHUCXQdS29Ibzro=; tfstk=cnWCBVMEEaBNxNTZNeZa4f3qvQpRwawWj5YcAyjQ7k8eLE1D7x8XD57IMBpMf; xlly_s=1; l=fBPdz3S7TBqZafQCBOfZEurza779sIRVguPzaNbMi9fPOT1M5JjcW1GPIVLHCnGdEsk6R38YsXPkBRLKoy4thYPbdqBdjy--3dRClKz3_; isg=BCEhFPYX4fayR0p7gTjWotPbMOs7zpXAMvnU4IP2HCiH6kO8yx4CkRpoSBDsIi34'
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'User-Agent': ('Mozilla/5.0 (Linux; Android 7.1.2; HD1910 Build/N2G48H) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/68.0.3440.70 Mobile Safari/537.36'),
        'Cookie': cookie
    }

    # params = {
    #     'jsv': '2.7.1',
    #     'appKey': 12574478,
    #     't:': 1678028006118,
    #     'sign': '59cc0e7730ea3a6b072d66938ba51711',
    #     'api': 'mtop.alsc.wamai.store.detail.miniapp.business.tab.page',
    #     'v': '1.0',
    #     'type': 'originaljson',
    #     'dataType': 'json',
    #     'timeout': 10000,
    #     'subDomain': 'waimai-guide',
    #     'H5Request': 'true',
    #     'ttid': 'h5@safari_ios_604.1',
    #     'SV': '5.0',
    #     'data': {'eleStoreId': 'E8407665249087482342', 'longitude': '113.01582', 'latitude': '28.121616'},
    #     'bx_et': 'cBrFB-wuo0V_JUrZccmzuxfH-JAdZZoiAHHI-_tQ1pofgW0hiMA-ItjipvYR22f..'
    # }
    req = requests.get(url=url, headers=headers)
    status_code = req.status_code
    if status_code != 200:
        print('eleme: req_waimai_shop_info: error ' + str(status_code))
        return

    json_str = req.json()
    # print(json_str)
    data_json = json_str['data']
    if not data_json:
        print('req_waimai_shop_info: data_json is null')
        return

    tmp_store_info = data_json['resultMap']['businessTabBasicInfo']['storeInfo']
    shop_name = tmp_store_info['storeName']  # 店铺名
    logo = tmp_store_info['storeLogo']
    logo_list = list(logo)
    logo_list.insert(1, '/')
    logo_list.insert(4, '/')
    logo_str = ''.join(logo_list)
    logo_str = 'https://cube.elemecdn.com/' + logo_str

    if 'jpeg' in logo_str:
        logo_str += '.jpeg'
    elif 'jpg' in logo_str:
        logo_str += '.jpg'
    else:
        logo_str += '.png'

    shop_addr = tmp_store_info['details'][0]['description']  # 商家地址
    shipping_time = tmp_store_info['details'][1]['description']  # 配送时间
    shop_score = get_shop_score(shop_code, cookie)
    res = {
        'shop_name': shop_name,
        'shop_addr': shop_addr,
        'front_img': logo_str,
        'shipping_time': shipping_time,
        'shop_score': shop_score
    }
    print(res)
    return res


def req_comments_by_page():
    session_comment = '{"service":"ShopRatingService","method":"getRateResult","params":{"rateQuery":{"shopIds":[2135172253],"startTime":"2023-02-05T00:00:00","endTime":"2023-03-07T23:59:59","isReplied":null,"rateType":"ALL","rateSourceType":"ELEME","rateContentType":"ALL","currentPage":1,"offset":0,"limit":10}},"id":"DEE1814615AA4350A2D72965C04CD39B|1678169647805","metas":{"appVersion":"1.0.0","appName":"melody","ksid":"YJGXYTMTA1MjkwMTExOTU1MjAxT3VEZEJlYzVQ","shopId":2135172253},"ncp":"2.0.0"}'
    cookie = ''
    current_page = 1
    comments_dict = {'list': None, 'end_request': False}

    start_time = waimai_util.get_pre_days_str(waimai_util.get_zero_today_timestamp(), 7)
    end_time = waimai_util.get_last_today_str()

    url = 'https://app-api.shop.ele.me/ugc/invoke/?method=ShopRatingService.getRateResult'
    form_json = json.loads(session_comment)
    form_json['params']['rateQuery']['currentPage'] = current_page
    form_json['params']['rateQuery']['startTime'] = start_time
    form_json['params']['rateQuery']['endTime'] = end_time
    # form_json['params']['rateQuery']['offset'] = 0

    headers = {
        # 'content-type': 'application/json;charset=UTF-8',
        'User-Agent': ('Mozilla/5.0 (Linux; Android 7.1.2; HD1910 Build/N2G48H) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/68.0.3440.70 Mobile Safari/537.36'),
        'Cookie': cookie
    }
    req = requests.post(url=url, headers=headers, json=form_json)
    status_code = req.status_code
    if status_code != 200:
        print('eleme: req_comments: error ' + str(status_code))
        comments_dict['end_request'] = True
        return comments_dict

    json_str = req.json()
    result_json = json_str['result']
    print(result_json)
    if not result_json:
        print('req_comments_by_page: result_json is null')
        comments_dict['end_request'] = True
        return comments_dict
    rate_infos = result_json['rateInfos']
    if not rate_infos:
        print('req_comments_by_page: rate_infos is null')
        return comments_dict


def time_format_test(time_str):
    format_str = time_str.replace('T', ' ')
    date_time = datetime.strptime(format_str, "%Y-%m-%d %H:%M:%S")
    print(date_time)


def parse_order_test():
    with open('eleme_order.json') as f:
        json_str = json.load(f)

    # with open('eleme_order_test.json', 'w') as f1:
    #     json.dump(json_str, f1)

    result_json = json_str['result']
    if not result_json:
        print('req_order_info result_json is null nor empty')
        return

    for result_item in result_json:
        header_dict = result_item['header']
        plan_deliver_time = header_dict['planDeliverTime']  # 预计到达时间的 timestamp
        user_info = result_item['userInfo']
        custom_phones = user_info['ticketCustomerPhones']
        custom_phones_len = len(custom_phones)

        # 订单基本信息
        order_seq_id = header_dict['daySn']  # 订单当天的序列号 例如： 1
        order_id = result_item['id']  # 订单ID
        order_time = result_item['activeTime'].replace('T', ' ')  # 订单的下单时间
        arrival_time = waimai_util.get_time_format_ms_str(plan_deliver_time)  # 预计到达时间

        # 客户信息
        address = user_info['consigneeAddress']
        recipient_name = user_info['consigneeName']  # 客户名
        recipient_phone = ''  # 客户电话
        privacy_phone = ''
        backup_privacy_phones = ''
        if custom_phones_len == 2:
            privacy_phone = custom_phones[0]  # 客户私密电话
            backup_privacy_phones = custom_phones[1]  # 客户备用电话

        # 菜品信息
        food_list = []
        food_groups = result_item['foodInfo']['groups']
        for food_group in food_groups:
            food_items = food_group['items']
            for food_item in food_items:
                food_name = food_item['name']
                food_quantity = food_item['quantity']
                food_price = food_item['price']
                food_total = food_item['total']
                tmp_food_item = {
                    'food_name': food_name,
                    'food_price': food_price,
                    'food_quantity': food_quantity,
                    'food_total': food_total
                }
                food_list.append(tmp_food_item)
        menu_json = json.dumps(food_list)

        # json_menu = json.loads(menu_json)
        # print(json_menu)

        # 结算信息
        settle_info = result_item['settlementInfo']
        custom_paid_info = settle_info['customerPaidInfo']
        merchant_paid_info = settle_info['merchantActivityInfo']
        platform_paid_info = settle_info['platformServiceFeeInfo']
        expected_income_info = settle_info['expectedIncomeInfo']

        xiaoji = ''
        customer_fee_list = custom_paid_info['feeList']
        for customer_fee in customer_fee_list:
            fee_name = customer_fee['name']
            if fee_name == '小计':
                xiaoji = customer_fee['price']
                break

        xiaoji_paid = xiaoji  # 小计
        merchant_paid = 0 - float(merchant_paid_info['total'])  # 商家活动支出
        platform_paid = 0 - float(platform_paid_info['total'])  # 平台服务费
        expected_income = expected_income_info['total']  # 本单预计收入
        final_paid = custom_paid_info['total']  # 顾客实际支付

        # 结算dict
        settle_dict = {
            '小计': xiaoji_paid,
            '商家活动支出': merchant_paid,
            '平台服务费': platform_paid,
            '本单预计收入': expected_income,
            '顾客实际支付': final_paid
        }
        print(settle_dict)
        settle_json = json.dumps(settle_dict)

        # 数据库data
        order_data = {
            'shop_code': 0,
            'shop_type': 0,
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
        print(order_data)


if __name__ == '__main__':
    # https://h5.waimai.meituan.com/waimai/mindex/home
    # get_comments()
    # get_shop_info('3314440')
    # get_elm_shop_info(2135172253)
    # req_comments_by_page()
    # time_format_test('2022-11-28T23:59:59')
    parse_order_test()
