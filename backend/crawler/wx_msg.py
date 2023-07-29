import json

import requests
from django.core.exceptions import ObjectDoesNotExist

from dvadmin.crawler.models import SystemVarModel

appid = 'wx0fb2061401ae94e6'
secret = 'adee70d7bb0659f33eafb3d6774b260d'
template_id = '5qGSe-TR0b5t56NsNBIrKBnYyhMDuuK7GmNUMBULxmo'

def get_wx_access_token():
    url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}'
    print(url)
    # url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx0fb2061401ae94e6&secret=adee70d7bb0659f33eafb3d6774b260d'
    req = requests.get(url)
    result = req.text
    print(result)
    return json.loads(result)['access_token']


def send_msg(access_token, touser):
    url = f'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=' + access_token
    print(url)
    data = {
        "touser": touser,
        "template_id": template_id,
        "page": 'pages/work/index',
        "miniprogram_state": 'developer',
        "lang": 'zh_CN',
        "data": {
            "thing1": {
                "value": '1123'
            },
            "amount2": {
                "value": '20'
            },
            "thing3": {
                "value": '说明'
            }
        }
    }
    print(data)
    req = requests.post(url=url, data=json.dumps(data))
    result = req.text
    print(result)


def get_uid():
    "https://api.weixin.qq.com/sns/jscode2session?appid=APPID&secret=SECRET&js_code=JSCODE&grant_type=authorization_code"
    url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code=023XO5200jHRXO104o300cKVd61XO527&grant_type=authorization_code'
    req = requests.get(url)
    result = req.text
    print(result)


if __name__ == '__main__':
    # todo token过期才去获取token
    access_token = get_wx_access_token()
    send_msg(access_token, 'opyrs0IZyB9sWuscRMcjFHN7I3Bs')
    # get_uid()
