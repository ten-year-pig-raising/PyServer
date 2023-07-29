import datetime
import json
import requests


def send_msg(touser):
    data = {
        "touser": touser,
        # "businessid": 1,
        "msgtype": "text",
        "text":
            {
                "content": "Hello World"
            }
    }

    access_token = "63_Bap1_6tk-PMfJuVgfdWYezA4AE6TW2c_-kP0QfxUJIpsAWKaK3978Z4tBp5xBgehhMMhHPM_gfMCFZcIW7QAOuCsdLiHHfZoufXN8LTrvmp1N9q20g69CUPE4qMNCNjAIABQB"
    url = f'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=' + access_token
    # print(data)
    req = requests.post(url=url, data=data)
    # req = requests.post(url=url, json=json.dumps(data))
    result = req.text
    print(result)


if __name__ == '__main__':
    # todo token过期才去获取token
    # access_token = get_wx_access_token()
    send_msg('opyrs0IZyB9sWuscRMcjFHN7I3Bs')
    # get_uid()
