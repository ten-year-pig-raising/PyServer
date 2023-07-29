# -*- coding: utf-8 -*-
from application.celery import app
from dvadmin.crawler.core import shop_tasks


# 评价预警
@app.task
def task__pingjiayujing(*args, **kwargs):
    # print("=================args===============")
    start_id_str = args[0]
    end_id_str = args[1]

    start_id = int(start_id_str)
    end_id = int(end_id_str)

    # print("=================kwargs===============")
    # print(kwargs)
    shop_tasks.evaluation_of_early_warnings(start_id, end_id)


# 自动出餐
@app.task
def task__zidongchucan(*args, **kwargs):
    start_id_str = args[0]
    end_id_str = args[1]

    start_id = int(start_id_str)
    end_id = int(end_id_str)
    shop_tasks.automatic_dining(start_id, end_id)


# 获取订单
@app.task
def task__huoqudingdan(*args, **kwargs):
    start_id_str = args[0]
    end_id_str = args[1]

    start_id = int(start_id_str)
    end_id = int(end_id_str)

    shop_tasks.req_orders(start_id, end_id)


# 自动回复
@app.task
def task__zidonghuifu(*args, **kwargs):
    start_id_str = args[0]
    end_id_str = args[1]

    start_id = int(start_id_str)
    end_id = int(end_id_str)

    shop_tasks.auto_reply(start_id, end_id)


# 评分管理
@app.task
def task__pingfenjisuan(*args, **kwargs):
    start_id_str = args[0]
    end_id_str = args[1]

    start_id = int(start_id_str)
    end_id = int(end_id_str)

    shop_tasks.scoring_management(start_id, end_id)
