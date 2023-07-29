import datetime
import time


def format_form_data(data):
    data_array = data.split('&')
    res = {}
    for item in data_array:
        temp = item.split('=')
        res[temp[0]] = temp[1]
    return res


def get_current_timestamp_ms():
    now = datetime.datetime.now()
    timestamp = int(round(now.timestamp() * 1000))
    return timestamp


def get_current_timestamp():
    now = datetime.datetime.now()
    timestamp = now.timestamp()
    return timestamp


# 得到当天0点的时间戳
def get_zero_today_timestamp():
    now = datetime.datetime.now()
    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                          microseconds=now.microsecond)
    zero_today_timestamp = int(round(zero_today.timestamp()))
    return zero_today_timestamp


# 得到当天 23:59:59的时间戳
def get_last_today_timestamp():
    now = datetime.datetime.now()
    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                          microseconds=now.microsecond)
    last_today = zero_today + datetime.timedelta(hours=23, minutes=59, seconds=59)
    last_today_timestamp = int(round(last_today.timestamp()))
    return last_today_timestamp


# 当前时间往前推 几天
def get_pre_days(current_timestamp, days):
    pre_month_timestamp = current_timestamp - 86400 * days
    return pre_month_timestamp


# 得到当天 00:00:00秒的格式化时间
def get_zero_today_str():
    now = datetime.datetime.now()
    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                          microseconds=now.microsecond)
    zero_today_timestamp = int(round(zero_today.timestamp()))
    time_array = time.localtime(zero_today_timestamp)
    time_str = time.strftime("%Y-%m-%dT%H:%M:%S", time_array)
    return time_str


# 得到当前天的字符串 例: 2023-2-28
def get_current_day_str():
    now = datetime.datetime.now()
    timestamp = now.timestamp()
    time_array = time.localtime(timestamp)
    time_str = time.strftime("%Y-%m-%d", time_array)
    return time_str


# 得到当天 23:59:59秒的格式化时间
def get_last_today_str():
    now = datetime.datetime.now()
    zero_today = now - datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second,
                                          microseconds=now.microsecond)
    last_today = zero_today + datetime.timedelta(hours=23, minutes=59, seconds=59)
    last_today_timestamp = int(round(last_today.timestamp()))
    time_array = time.localtime(last_today_timestamp)
    time_str = time.strftime("%Y-%m-%dT%H:%M:%S", time_array)
    return time_str


# 从 当前时间戳 time_stamp 返前 days天
def get_pre_days_str(time_stamp, days):
    back_time_stamp = days * 24 * 60 * 60
    pre_day_timestamp = time_stamp - back_time_stamp
    time_array = time.localtime(pre_day_timestamp)
    time_str = time.strftime("%Y-%m-%dT%H:%M:%S", time_array)
    return time_str


# 根据timestamp 得到格式化的时间
def get_time_format_ms_str(ms_timestamp):
    timestamp = int(ms_timestamp / 1000)
    time_array = time.localtime(timestamp)
    time_str = time.strftime("%Y-%m-%dT%H:%M:%S", time_array)
    return time_str


def get_normal_time_format_str(timestamp):
    time_array = time.localtime(timestamp)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return time_str


# 通过cookie字符串解析成 cookie dict
def extract_cookies(cookie):
    """从浏览器或者request headers中拿到cookie字符串，提取为字典格式的cookies"""
    cookie_dict = dict([cookie_str.split("=", 1) for cookie_str in cookie.split("; ")])
    return cookie_dict


# 判断字对象是否是NONE或者empty
def is_null_or_empty(str_param):
    if not str_param:
        return True

    length = len(str_param)
    if length == 0:
        return True
    else:
        return False


# 判断配送时间 是否在有效时间内
def check_delivery_time(delivery_start_time, delivery_end_time):
    if not delivery_start_time:
        return False

    if not delivery_end_time:
        return False

    now = datetime.datetime.now()
    now_delta_time = datetime.timedelta(hours=now.hour, minutes=now.minute, seconds=now.second)
    start_delta_time = datetime.timedelta(hours=delivery_start_time.hour, minutes=delivery_start_time.minute, seconds=delivery_start_time.second)
    end_delta_time = datetime.timedelta(hours=delivery_end_time.hour, minutes=delivery_end_time.minute, seconds=delivery_end_time.second)

    if start_delta_time < now_delta_time < end_delta_time:
        return True
    else:
        return False
