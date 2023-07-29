import datetime
import json

import requests

import dvadmin.crawler.views.system_var as system_var
from dvadmin.crawler.models import ShopModel, SubMsgConfigModel, RegisterUserModel


def get_wx_access_token(appid, secret):
    access_token_model = system_var.get_system_var_object('appid_access_token')
    access_token = access_token_model.value
    if datetime.datetime.now() < access_token_model.expires_time:
        return access_token
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}'
    print(url)
    # url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx0fb2061401ae94e6&secret=adee70d7bb0659f33eafb3d6774b260d'
    req = requests.get(url)
    result = req.text
    print(result)
    access_token_json = json.loads(result)
    access_token_model.value = access_token_json['access_token']
    access_token_model.expires_time = datetime.datetime.now() + datetime.timedelta(
        seconds=access_token_json['expires_in'])
    access_token_model.save()
    return access_token_json['access_token']


def create_post_data(touser, template_id, data_dict):
    data = {
        "touser": touser,
        "template_id": template_id,
        "page": 'pages/work/index',
        "miniprogram_state": 'developer',
        "lang": 'zh_CN',
        "data": {
            "thing10": {
                "value": data_dict['param1']
            },
            "character_string6": {
                "value": data_dict['param2']
            },
            "thing4": {
                "value": data_dict['param3']
            },
            "thing3": {
                "value": data_dict['param4']
            },
            "time5": {
                "value": data_dict['param5']
            }
        }
    }
    return data


# data_dcit 格式：
# 门店名称: param1 (thing10.DATA)             GZ天河城市店    ：20个字符以内
# 订单编号: param2 (character_string6.DATA)   Y123456       : 32位以内
# 评价星级: param3 (thing4.DATA)              4.5           ： 20个字符以内
# 评价内容: param4 (thing3.DATA)              味道不好，服务态度差 ：20个字符以内
# 订单时间: param5 (time5.DATA)               2023年2月1日 18:36
def send_msg(touser, data_dict):

    if type(touser) == list:
        touser = touser[0]
    elif type(touser) != str:
        raise Exception('touser 参数错误')

    register_user_model = RegisterUserModel.objects.get(openid=touser)
    sub_msg_config_model = SubMsgConfigModel.objects.get(register_user=register_user_model.id)
    if sub_msg_config_model.sub_times <= 0:
        raise Exception("订阅次数小于0")
    appid = system_var.get_system_var_value('appid')
    secret = system_var.get_system_var_value('secret')
    template_id = system_var.get_system_var_value('template_id')
    access_token = get_wx_access_token(appid, secret)
    url = f'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=' + access_token
    # print(url)
    data = create_post_data(touser, template_id, data_dict)
    # print(data)
    req = requests.post(url=url, data=json.dumps(data))
    result = json.loads(req.text)
    print(result)
    try:
        if result['errmsg'] == 'ok':
            # 发送成功，数据库中订阅次数减少一次
            sub_msg_config_model.sub_times = sub_msg_config_model.sub_times - 1
        elif 'user refuse to accept the msg' in result['errmsg']:
            # 错误信息提示'user refuse to accept the msg'，把数据库中的订阅数量清零
            sub_msg_config_model.sub_times = 0
        sub_msg_config_model.save()
    except Exception as e:
        print(e)
    return result


def send_shop_msg(shop_code, shop_type, data_dict):
    # 通过店铺ID获取绑定用户的openid
    try:
        shop = ShopModel.objects.get(shop_code=shop_code, shop_type=shop_type)
    except Exception as e:
        raise Exception("找不到店铺")
    touser = shop.register_user.openid
    send_msg(touser=touser, data_dict=data_dict)


#
# def get_uid():
#     "https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code"
#     url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code=023XO5200jHRXO104o300cKVd61XO527&grant_type=authorization_code'
#     req = requests.get(url)
#     result = req.text
#     print(result)


if __name__ == '__main__':
    # todo token过期才去获取token
    # access_token = get_wx_access_token()
    send_msg('opyrs0IZyB9sWuscRMcjFHN7I3Bs')
    # get_uid()
