import json

import requests

from dvadmin.crawler.util import waimai_util

form_data = 'optimus_code=10&optimus_risk_level=71&lng=112.973829&lat=28.094222&gpsLng=112.973829&gpsLat=28.094222&shopId=-1&mtWmPoiId=916847935130264&poi_id_str=8YAMR43fo7YOe2NiaZOz5wI&startIndex=0&labelId=0&scoreType=0&uuid=261E36EA0C923CFDF0EE8F3C119FBEA7CE7684E9B54A7958A5CE697CBA711407&platform=3&partner=4&originUrl=https%3A%2F%2Fh5.waimai.meituan.com%2Fwaimai%2Fmindex%2Fmenu%3FmtShopId%3D916847935130264%26poi_id_str%3D8YAMR43fo7YOe2NiaZOz5wI%26dishId%3D%26source%3Dshoplist%26utm_source%3D%26channel%3Ddefault%26mtOrderId%3D%26h5_detail_back%3D%26initialLat%3D28.094222%26initialLng%3D112.973829%26actualLat%3D28.094222%26actualLng%3D112.973829&riskLevel=71&optimusCode=10&wm_latitude=28094222&wm_longitude=112973829&wm_actual_latitude=28094222&wm_actual_longitude=112973829&wmUuidDeregistration=0&wmUserIdDeregistration=0&openh5_uuid=261E36EA0C923CFDF0EE8F3C119FBEA7CE7684E9B54A7958A5CE697CBA711407&_token=eJxNktmOozgYRt%2BFW1CMwWx1x1YBQoAABQmjuWBLQsIWcBFIa959iFqtasmSP3%2F%2FOZJl%2BRcxmAXxAWko0JAipnIgPgi4oTc8QRF4XCc8L3GSABkGoRXI%2F%2B4QRIihiGyINOLjH1aiKRGhf9%2BFv55%2Fip%2FEoHW9CXMFiCvG%2FfgBwJXbPNOqSatNU1b4O203edeA3xVoqrYo5%2FU2xOo14duDrEQxHFo7RqQpxMA1QVGkeEZ8Q%2Fc3tO7p3zAVeLLzY1CaGf1YlLnfvk38x9yvr7COx%2BrSrqm0Fny%2Fkx79kg9zBmyjfd6qhAZhL4%2F1NgkfhaXqmaIuy3GxGrQwuHIzM1dbju%2FjxwHzna455OQ0gnHO2CdrT5yijMZut7sv8%2FXCqfHpq7Z3HWpaa3ez7eR1nJTeuPBZ9JqGrBc%2FI4BNbVtdk3p%2BjHTPtGrVvU5%2Bcu8F6RQpo75jHslnvBTOXFhNKUgOM2R5f2FqeMxCOMy9G6YsDDIvrYU6SWg2i4w5qZ1XMLg6EmS5nGLHSIKLmumuf1O97JqEqonBVixC40rXqdz40VWJ09Qu%2Bekyzv6w7wxBj%2FsWtgf%2BbAlTXrpS1Z3cqyhuLfFRk2CpbY07AcE%2FCrJnZ6AuSNbSFWAGxexMkfTVI0MLNI05ON8D7nqLvO%2FjLr681k95QGbqilvui8PB1jkccjv38on0ffmp65oLuQmZkLvVN9iQI%2BbolHcqNlR2av7USAGfLDrmM0nPSeVsYJ89a1U7e%2Bf4EYjgEx0ziSnSDMqOa2DW7NoFwHb4CgGvc1jgisC0LHp%2Fkhl3flplrnvfr8dd0MximDGQl8u3G72iYW73%2FjNa0MmLmuXJTmwMrAiMgPjvf2kQA5s%3D'


def create_header():
    headers = {}
    headers['Accept'] = 'application/json'
    headers['Accept-Encoding'] = 'gzip, deflate, br'
    headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8'
    headers['Connection'] = 'keep-alive'
    headers['Content-Length'] = '2359'
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    headers[
        'Cookie'] = 'uuid=13b3784134d8471ea4be.1667394562.1.0.0; _lxsdk_cuid=1843876cc29c8-06fd288765617e-26021e51-144000-1843876cc2ac8; ci=70; _ga=GA1.1.1016111602.1668953252; wm_order_channel=default; request_source=openh5; au_trace_key_net=default; isIframe=false; WEBDFPID=u65wzzuz3x10589xy2y3458282245xx6815z53zuv8597958x83vuwx5-1984565844800-1669205842725YWQKMWKfd79fef3d01d5e9aadc18ccd4d0c95079036; terminal=i; w_utmz="utm_campaign=(direct)&utm_source=5000&utm_medium=(none)&utm_content=(none)&utm_term=(none)"; iuuid=261E36EA0C923CFDF0EE8F3C119FBEA7CE7684E9B54A7958A5CE697CBA711407; token=AgHMIrk7D4xPIJJqxfO2OPJvgbQO1QkcifwmdcGC5LSl8eUxwbAEh_FNmduY_HG_BuZB9MoMwnY9mwAAAAAkFQAACthpIzsX9YtJt595aNe55sSVhs0wqqhj2FvvuUxpaR2uGDVne04Kd5OYWcES9EJ0; mt_c_token=AgHMIrk7D4xPIJJqxfO2OPJvgbQO1QkcifwmdcGC5LSl8eUxwbAEh_FNmduY_HG_BuZB9MoMwnY9mwAAAAAkFQAACthpIzsX9YtJt595aNe55sSVhs0wqqhj2FvvuUxpaR2uGDVne04Kd5OYWcES9EJ0; oops=AgHMIrk7D4xPIJJqxfO2OPJvgbQO1QkcifwmdcGC5LSl8eUxwbAEh_FNmduY_HG_BuZB9MoMwnY9mwAAAAAkFQAACthpIzsX9YtJt595aNe55sSVhs0wqqhj2FvvuUxpaR2uGDVne04Kd5OYWcES9EJ0; userId=1939188632; _lxsdk=261E36EA0C923CFDF0EE8F3C119FBEA7CE7684E9B54A7958A5CE697CBA711407; openh5_uuid=261E36EA0C923CFDF0EE8F3C119FBEA7CE7684E9B54A7958A5CE697CBA711407; w_token=AgHMIrk7D4xPIJJqxfO2OPJvgbQO1QkcifwmdcGC5LSl8eUxwbAEh_FNmduY_HG_BuZB9MoMwnY9mwAAAAAkFQAACthpIzsX9YtJt595aNe55sSVhs0wqqhj2FvvuUxpaR2uGDVne04Kd5OYWcES9EJ0; openh5_uuid=261E36EA0C923CFDF0EE8F3C119FBEA7CE7684E9B54A7958A5CE697CBA711407; _lx_utm=utm_source%3D; _ga_95GX0SH5GM=GS1.1.1669249551.4.0.1669249551.0.0.0; w_uuid=1iKzfS0Qwz6A_IZWap4Bu9piBl76yFDbZckBhq-mUeNk89hbdWNhdgQ24nerS3vK; utm_source=0; wx_channel_id=0; webp=1; w_cid=430100; w_cpy=changsha; w_cpy_cn="%E9%95%BF%E6%B2%99"; JSESSIONID=uytlxzel6v2b1da9dw9sv72y3; __mta=218881574.1669337850339.1669337876785.1669337876789.6; w_addr=%E5%8C%97%E8%BE%B0%E4%B8%AD%E5%A4%AE%E5%85%AC%E5%9B%ADD%E5%8C%BA%C2%B7%E6%85%A7%E8%BE%B0%E5%9B%AD; w_visitid=debc9244-4aa6-4b9b-b717-1c6395926929; channelType={%22default%22:%220%22}; _yoda_verify_resp=F9fIdRuNHN1s6PXjfspl65w%2FB9%2B6H2SRlKwvA7mnkgIM49Q%2F6Yw%2F0PrF5ksOwFO6xK%2BMa48kIPqFKddEold4f%2F%2BQp%2Fvbdu8VU9vEzGPaUQoFr3uSzJQv4unGdgcCzhBlBlFIi8YgxkcR1YlY%2FnBcLbFBc1OjlARDbmLXkSM%2FFxpFoaZsUHo0vFscqrlkMs7u%2FlQGC%2BxGINzxQPJL2HCYdXKmxwRaUZY%2FCDAb2x2sZF4jGL2KLIn1rQGu1x3ZwIHAMEmKbVPxvyR0EY4LYkbN2xkMUbKHMrD9KQ%2FM4sf%2FYaRJmhjkMOVSsVOLxcMUAkSKfgQGiVzOkSBDKmULDErcyD0WcfBpoahJ1WvSUrOdUi27kl9YXfn2ep%2BFxFxzNJnv; _yoda_verify_rid=1629cbf14d022030; cssVersion=03239a63; channelConfig={%22channel%22:%22default%22%2C%22type%22:0%2C%22fixedReservation%22:{%22reservationTimeStatus%22:0%2C%22startReservationTime%22:0%2C%22endReservationTime%22:0}}; _lxsdk_s=184bbbd83f8-66e-77-ad6%7C%7C64'
    headers['Host'] = 'i.waimai.meituan.com'
    # headers['mtgsig'] = '{"a1":"1.0","a2":1669249676958,"a3":"u65wzzuz3x10589xy2y3458282245xx6815z53zuv8597958x83vuwx5","a4":"4155736865a98705687355410587a965f6c55de6f342f483","a5":"p3awpKvPtr3tMHbtTwv4br8ZLQ+vP556TDIlOBbfMIJhK2fXFT9g971Wocv8k8dxSVlYYhgS0ObbTU6mlNmmtrurNLXO","a6":"h1.2meCgGeFKojlg6pJvS1B4lKleNo4lEh6kgTGpdta36VH10kxoXC/3WfAA1FsaYroVhr9qn7JnEpMUxYcWaj1FeXSC2exf4orlQTikBPBm+/ED1OQ0WUBHA9OM/RUxLlUc0vPoaKCiA5tzQCNKEhdxD6IL6Wjo3LpeXVdqHh0+rDmrfkqoHkj0dcZd56HbAwsd/7BI30lNZQfkTpHACXoYm6ZLHapdlggGlT3/5kwJk4GszorKn5ydIXh0FKs5EdznlZk/CdOOot8lGdhDnQaYWO9uFz3meBRyJGnW7EaX98wQ0CjRbpByyk6SwXNLznmXHpsmGGQUSyC0vCL0NNNlDdebUgF4s2/qGl/NalmX1fJWa2d88yw77vqeQCN0ciLLeXJx1Y123xK1CAo3p6cg7CkHbc9V1ztS77CawPbiz0ndP9v0fLC4hwn3nYJhoQgtO55cGoh7DiwqI5c6hYdiK0KdWQfCvv8k2WwHK5XMoIeVFcTfXtvyneKwr1pkJrnlN5EVxxdft/p1NMpCglnRrG7GBUJw5ncGjbluvXu87M3ungsr31BmdcvqF02Z0Im4Wss0i68C3OhDTXxjVplXDSUr9PojZYvjqH2N9K8qK2Gj2ci/3AuGpbV6OAK7nJLyDqt2kcDpiclL05z7mvD9uKTfMUlnf/eW6KfHhvB/CfFcuEJi6tHYV8LewuMa/NMqlGybVxN/Y3EU3dBVeKNrDl8/Y7o9uiAa0XsU3eYLsKDSYupSQUgrPDhHLqpFtiF6luOL7Y2vacn/E5RQqROeC4EA4esMAX+5/C8VX3YO5/K6M9uYC2TrbgGJ++JA0V1RhrOeaHXiSl0b3JNef9p9TtNfSUwvO5K7l8MlRpjrU9pY4ogRTNSCv6X/Xieg+oYr","a7":"","x0":4,"d1":"eaea9403a4a633d19ba6c6eb6d37d3a7"}'
    headers['Origin'] = 'https://h5.waimai.meituan.com'
    headers['Referer'] = 'https://h5.waimai.meituan.com/'
    headers['Sec-Fetch-Dest'] = 'empty'
    headers['Sec-Fetch-Mode'] = 'cors'
    headers['Sec-Fetch-Site'] = 'same-site'
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


def get_comments():
    url = f'https://i.waimai.meituan.com/openh5/poi/comments?_=1669337925809'
    headers = create_header()
    data = format_form_data(form_data)
    data['mtWmPoiId'] = '955425331386563'
    print(url)
    print(headers)
    print(data)
    last_index = 0
    step = 20
    data['startIndex'] = last_index
    for startIndex in range(0, 10):
        print(data['startIndex'])
        req = requests.post(url=url, headers=headers, data=data)
        result = req.text
        print(result)
        last_index = data['startIndex']
        data['startIndex'] = last_index + step

    # req = requests.post(url=url, headers=headers, data=data)
    # result = req.text
    # print(result)


shop_info_form_data = 'optimus_code=10&optimus_risk_level=71&shopId=-1&orderPlatform=&mtWmPoiId=983527302492402&poi_id_str=zzH36wUuODX6mJmIWAs3kAI&source=shoplist&address=&cityId=&channel=6&gpsLng=112.973865&gpsLat=28.094283&uuid=261E36EA0C923CFDF0EE8F3C119FBEA7CE7684E9B54A7958A5CE697CBA711407&platform=3&partner=4&originUrl=https%3A%2F%2Fh5.waimai.meituan.com%2Fwaimai%2Fmindex%2Fmenu%3FmtShopId%3D983527302492402%26poi_id_str%3DzzH36wUuODX6mJmIWAs3kAI%26dishId%3D%26source%3Dshoplist%26utm_source%3D%26channel%3Ddefault%26mtOrderId%3D%26h5_detail_back%3D%26initialLat%3D28.094283%26initialLng%3D112.973865%26actualLat%3D28.094283%26actualLng%3D112.973865&riskLevel=71&optimusCode=10&wm_latitude=28094283&wm_longitude=112973865&wm_actual_latitude=28094283&wm_actual_longitude=112973865&wmUuidDeregistration=0&wmUserIdDeregistration=0&openh5_uuid=261E36EA0C923CFDF0EE8F3C119FBEA7CE7684E9B54A7958A5CE697CBA711407&_token=eJzdVNtuqzgU%2FRck%2BpKo2AYMVKqOAiQl95Dmymh0ZMAkhEsSriGj%2BfcxaaueI83DPI9kwVprr72N947zF5cNfe4FAqgA2OUqmnEvHHwGz5jrckXOIhhrCgIQAKCgLuf9qiGIkNzl3Gxjci9%2FiBroqpL0ZyssGf8WvhGS2GodQ2bgjkVxyV8E4Sg%2F1yRMSPic0LAoSfrsnRPhQxKSMPXpTTieE%2FrDO%2Fv0lW0LZPyU5IdXvq%2FyvQGvK3wf8zrkVcT3ZV43voDKVreNqTqvMUnhdQbMVtFEXmVA4nWT14ynjOaXc5rTn48tKNZcAGUa%2BF4guYrv%2Bn6AiKd6hABIMWT2a0nz4sOtQEmkPkWAaqrkiqoKYQABdWWPSB7LY538Oinrbxg0vx2zQgK5XIQDTWlG4p8XcqA%2FPssb%2F6X6E02r10t2fspLzzNIHLvEi8YzfVCmr79p6yx%2BfXwHL%2FZ4NGDrX%2FvO9A%2BRgY%2Fet07WfV4ctMflRfNjAjzCbAaM8khmc0AymwSS2SwYxS2C7MEGwajcUuN3qn4%2BjC8%2FmxGStYehraE%2FqPkVZfNilgeV2miL2NwCEsb%2F5wNy7LIkq%2FayQHaHkKywHxPSYFdCgCGMuipsJVGUuqqIWnfUutmb%2FJrVNYeb78xP9pH9ST4rPBjLLr6qTNn%2FAQvn4SFliI6aIoo6C9T07JsrTKzstJmVhhBvzHg%2BxIRcN%2F51f0UzKSfwqAwOva1EgmA1uAfOxl8koD9fVFY0VUXFtJaB8V56exzRsnBu%2B1Oa1QuBGOftAGlafV9Hzih2xu%2FCcQJqs5esNzt7mndsNRKuYK3Xm2Y3e%2B%2F3V1G8j1b2ocm15QmGYGL0nUacjdXMmSfDbOW4O3%2BE5L2CEt1TVk6xWy2LyPEvW4SawsDXbNzcLznKzkW61j3nsj4vE6tYhW%2FhNKrrqNlEJ2VuWYI7voWSfTDxcO6j%2BUlTZoqlOsfBqMZjG9tRZ7jLrqZ3XUTlrReKkQaPo2p3s4VqdpaP1ele73F%2FJN7jDKnBeCVjt6e6EyHClwVZaNu5VeZavzTfBs70HnZA7GFrqU%2Fx6Uaq8pxBfRCMnYk8XVS6skW%2Bn%2FX22E7zxTqgOy16t2xpOFhAdRncttW16nUcIdVp8cb2HYs7kA3Xd9IBeKL1844x14SR%2Bza595oRGFXeTBgJoGru6HKA5dIdbzc2OmalTU9bd7itD1NRnktecSidOnXNtDHjozeqZmRueXerLue9IWRtddNTFRwm2Ktki%2Fv7H0Cf2SY%3D'


def get_shop_info(shop_code):
    url = 'https://i.waimai.meituan.com/openh5/poi/info'
    # url = 'https://openapi.waimai.meituan.com/openapi/v2/poi/detailinfo'
    headers = create_header()
    headers[
        'Cookie'] = 'uuid=13b3784134d8471ea4be.1667394562.1.0.0; _lxsdk_cuid=1843876cc29c8-06fd288765617e-26021e51-144000-1843876cc2ac8; ci=70; _ga=GA1.1.1016111602.1668953252; wm_order_channel=default; request_source=openh5; au_trace_key_net=default; isIframe=false; WEBDFPID=u65wzzuz3x10589xy2y3458282245xx6815z53zuv8597958x83vuwx5-1984565844800-1669205842725YWQKMWKfd79fef3d01d5e9aadc18ccd4d0c95079036; terminal=i; w_utmz="utm_campaign=(direct)&utm_source=5000&utm_medium=(none)&utm_content=(none)&utm_term=(none)"; iuuid=261E36EA0C923CFDF0EE8F3C119FBEA7CE7684E9B54A7958A5CE697CBA711407; token=AgHMIrk7D4xPIJJqxfO2OPJvgbQO1QkcifwmdcGC5LSl8eUxwbAEh_FNmduY_HG_BuZB9MoMwnY9mwAAAAAkFQAACthpIzsX9YtJt595aNe55sSVhs0wqqhj2FvvuUxpaR2uGDVne04Kd5OYWcES9EJ0; mt_c_token=AgHMIrk7D4xPIJJqxfO2OPJvgbQO1QkcifwmdcGC5LSl8eUxwbAEh_FNmduY_HG_BuZB9MoMwnY9mwAAAAAkFQAACthpIzsX9YtJt595aNe55sSVhs0wqqhj2FvvuUxpaR2uGDVne04Kd5OYWcES9EJ0; oops=AgHMIrk7D4xPIJJqxfO2OPJvgbQO1QkcifwmdcGC5LSl8eUxwbAEh_FNmduY_HG_BuZB9MoMwnY9mwAAAAAkFQAACthpIzsX9YtJt595aNe55sSVhs0wqqhj2FvvuUxpaR2uGDVne04Kd5OYWcES9EJ0; userId=1939188632; _lxsdk=261E36EA0C923CFDF0EE8F3C119FBEA7CE7684E9B54A7958A5CE697CBA711407; openh5_uuid=261E36EA0C923CFDF0EE8F3C119FBEA7CE7684E9B54A7958A5CE697CBA711407; w_token=AgHMIrk7D4xPIJJqxfO2OPJvgbQO1QkcifwmdcGC5LSl8eUxwbAEh_FNmduY_HG_BuZB9MoMwnY9mwAAAAAkFQAACthpIzsX9YtJt595aNe55sSVhs0wqqhj2FvvuUxpaR2uGDVne04Kd5OYWcES9EJ0; openh5_uuid=261E36EA0C923CFDF0EE8F3C119FBEA7CE7684E9B54A7958A5CE697CBA711407; _ga_95GX0SH5GM=GS1.1.1669249551.4.0.1669249551.0.0.0; w_uuid=1iKzfS0Qwz6A_IZWap4Bu9piBl76yFDbZckBhq-mUeNk89hbdWNhdgQ24nerS3vK; utm_source=0; wx_channel_id=0; webp=1; w_cid=430100; w_cpy=changsha; w_cpy_cn="%E9%95%BF%E6%B2%99"; JSESSIONID=uytlxzel6v2b1da9dw9sv72y3; __mta=218881574.1669337850339.1669337876785.1669337876789.6; w_addr=%E5%8C%97%E8%BE%B0%E4%B8%AD%E5%A4%AE%E5%85%AC%E5%9B%ADD%E5%8C%BA%C2%B7%E6%85%A7%E8%BE%B0%E5%9B%AD; bussiness_entry_channel=default; _lx_utm=utm_source%3D; w_visitid=0e335675-fe01-4998-890a-203708043483; channelType={%22default%22:%220%22}; channelConfig={%22channel%22:%22default%22%2C%22type%22:0%2C%22fixedReservation%22:{%22reservationTimeStatus%22:0%2C%22startReservationTime%22:0%2C%22endReservationTime%22:0}}; _yoda_verify_resp=VAo%2FKY64ax8lu%2B8%2BKXxOerUQ9%2BGR3nEsjuRsZJdwK36Np4r153P3eHQDR3yk%2Fk2LEPYk902vy3PMG4ZYPaxTec8WqKpsFW1E5PEo%2F6F6idixYe6GolZZUxLrSFDoqeoy5ZpvfUs90Htbc6O0r%2FdYMhET4nC6O7ZHGKW6bs8g7uv9NnNgoHwY9jBHki90osW0MQFPRcz6e0KD2rHSGW1eVem7FNoqVIuJZ9yVMwCfvmIxC2DV%2BFYCQ4i2cZBiClTx678ZubCgO4nP5WtxKATcLiRyJKoqLw2D05cim4i5zGOkT7aHpq8s7YKQUE3XHs1DQL8cylFpWJW28J1VYH0QctIh4iP2jNXkFGsvqkd7b4DFVs6jL4uXSRfS0ANPj4o%2F; _yoda_verify_rid=162ba1371bc0d05c; cssVersion=1202795c; _lxsdk_s=184c312288d-af6-c15-64a%7C%7C83'
    # data = format_form_data(shop_info_form_data)
    data = {
        'mtWmPoiId': shop_code,
        'platform': '4',
    }
    # print(url)
    # print(headers)
    # print(data)
    req = requests.post(url=url, headers=headers, data=data)
    result = req.text
    print(result)


def param_test():
    comments_param = 'ignoreSetRouterProxy=true&acctId=29386830&wmPoiId=3314440&token=047CtHD018pivjE0WPePU7vzkrPTKds2rcaNvasaovw8%2A&appType=3&commScore=0&commType=-1&hasContent=-1&periodType=1&beginTime=1666627200&endTime=1669305600&pageNum=1&onlyAuditNotPass=0&pageSize=20'
    auto_reply_param = 'ignoreSetRouterProxy=true&acctId=29386830&wmPoiId=3314440&token=047CtHD018pivjE0WPePU7vzkrPTKds2rcaNvasaovw8%2A&appType=3&commScore=0&commType=-1&hasContent=-1&periodType=1&beginTime=1666627200&endTime=1669305600&pageNum=1&onlyAuditNotPass=0&pageSize=20'
    comments_param_json = waimai_util.format_form_data(comments_param)
    auto_reply_param_json = waimai_util.format_form_data(auto_reply_param)
    print(comments_param_json)
    print(auto_reply_param_json)


def mt_order_test():
    # with open('mt_order.json') as f:
    #     json_str = json.load(f)
    #
    # print(json_str)
    cookie = 'wm_order_channel=default; request_source=openh5; _lxsdk_cuid=186e900a918c8-003d55d634cdbb-1e525634-13c680-186e900a918c8; WEBDFPID=u340zv9x7w9251v51u1v3wv080ux72z0813v099zz4y97958yz0626vu-1994306380366-1678946379714OGOIEEQ75613c134b6a252faa6802015be905511304; iuuid=75DC0047498DF0BC5C2A53C31DCF55E56104AF79E9D95766E454AB642CF3E455; _lxsdk=75DC0047498DF0BC5C2A53C31DCF55E56104AF79E9D95766E454AB642CF3E455; device_uuid=!a87c87b2-7f9a-4960-b89b-32f274845dda; uuid_update=true; acctId=122553861; token=0g7X8lCfZgD6jBSI_PlwTuZP8WKa1HQbqYuMPEH7vZrQ*; wmPoiId=14148924; isOfflineSelfOpen=0; city_id=430100; isChain=0; ignore_set_router_proxy=false; region_id=1000430100; region_version=1647067009; bsid=RvL2JR-suFlXbMPYXJrm6YrG9hHq6mRKNGoX9Al8Ci6FNRt6GqFuz7aEGUnEMfquWs5aVqbWsBOGVgr9skw7ow; city_location_id=430100; location_id=430111; cityId=430100; provinceId=430000; set_info=%7B%22wmPoiId%22%3A%2214148924%22%2C%22region_id%22%3A%221000430100%22%2C%22region_version%22%3A1647067009%7D; pushToken=0g7X8lCfZgD6jBSI_PlwTuZP8WKa1HQbqYuMPEH7vZrQ*; setPrivacyTime=1_20230317; shopCategory=food; wpush_server_url=wss://wpush.meituan.com; logan_session_token=5b3p0ff8syf596l9a17s; _lxsdk_s=186edac920a-451-44a-3c%7C%7C328'
    cookie_dict = waimai_util.extract_cookies(cookie)
    param_url = f'https://e.waimai.meituan.com/gw/api/order/mix/unprocessed/list/common?region_id={0}&region_version={1}'
    url = param_url.format(cookie_dict['region_id'], cookie_dict['region_version'])
    print(cookie_dict['region_id'], cookie_dict['region_version'])
    print(url)


def mt_order_parse():
    with open('mt_order.json') as f:
        json_str = json.load(f)

    json_data = json_str['data']
    if not json_data:
        print('meituan request order: data is null')
        return

    wm_order_list = json_data['wmOrderList']
    if not wm_order_list:
        print('meituan request order: wm_order_list is null')
        return

    for wm_order in wm_order_list:
        common_info = wm_order['commonInfo']
        common_json = json.loads(common_info)

        # 基本订单信息
        order_id = common_json['wm_order_id_view']  # 订单的ID
        order_seq_id = common_json['wm_poi_order_dayseq']  # 订单预列号
        order_time = common_json['order_time']  # 订单下单时间  timestamp值
        arrival_time = common_json['estimateArrivalTime']  # 订单到达时间 timestamp值
        arrival_time_fmt_str = waimai_util.get_normal_time_format_str(arrival_time)

        root_order = wm_order['orderInfo']
        root_order_json = json.loads(root_order)

        print(order_seq_id)

        # 客户信息
        user_info = root_order_json['userInfo']
        recipient_name = user_info['recipientName']  # 顾客名
        recipient_phone = ''   # 顾客电话
        privacy_phone = ''     # 隐私号码
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
            print('meituan req_order pc_phones is null')

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
        commision_amount = settle_info['commisionAmount']   # 佣金
        if not commision_amount:
            commision_amount = 0
        else:
            commision_amount = 0 - commision_amount

        expected_income = settle_info['settleAmount']    # 预计收入
        final_paid = settle_info['userPayTotalAmount']   # 顾客实际支付
        delivery_amount = expected_income - discount_amount - commision_amount  # 配送服务费
        delivery_amount = round(delivery_amount, 2)
        # 结算dict
        settle_dict = {
            'discount_amount': discount_amount,    # 商品优惠后金额
            'commision_amount': commision_amount,  # 佣金
            'delivery_amount': delivery_amount,    # 配送服务费
            'expected_income': expected_income,    # 预计收入
            'final_paid': final_paid               # 顾客实际支付
        }
        settle_json = json.dumps(settle_dict, ensure_ascii=False)
        print(menu_json)
        print(settle_json)


if __name__ == '__main__':
    # https://h5.waimai.meituan.com/waimai/mindex/home
    # get_comments()
    # get_shop_info('3314440')
    # param_test()
    # mt_order_test()
    mt_order_parse()
