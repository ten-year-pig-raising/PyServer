import requests
from dvadmin.crawler.util import waimai_util


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
def get_shop_info(shop_code):
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


if __name__ == '__main__':
    get_shop_info('E12144740021053163341')
