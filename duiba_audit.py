#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2015
#
# @author: chenjiehua@youmi.net
#

"""兑吧订单审核处理

运营人员在自家后台进行兑吧订单的审核，将通过／拒绝的订单号
写入redis队列，此脚本从redis中读取数据，请求兑吧服务器，完
成订单的审核操作。
"""

import yaml
import torndb
import redis
import ujson as json
import requests
import time
import db
import utils
import constants

from utils import YamlLoader
from models import orders

# MySQL数据库连接配置
try:
    config = yaml.load(file(constants.SETTINGS_FILE, 'r'), YamlLoader)
except yaml.YAMLError as e:
    print "Error in configuration file: %s" % e

# 数据库连接实例
db.mysql = torndb.Connection(**config['mysql'])
pool = redis.ConnectionPool(**config['redis'])
db.redis = redis.Redis(connection_pool=pool)

def main():
    while True:
        raw_data = db.redis.blpop(constants.DUIBA_AUDIT_QUEUE)
        if not raw_data:
            continue
        data = json.loads(raw_data[1])
        # data = {"id": 123, "audit": True}
        o = orders.get_exchange_order_by_id(data['id'])
        if not o:
            continue
        if o['platform'] == 2:
            succ, errmsg = duiba(o['order_num'], data['audit'])
        elif o['platform'] == 1:
            succ, errmsg = duiba_aos(o['order_num'], data['audit'])
        if not succ:
            orders.update_note(data['id'], errmsg)

def sign(params={}):
    """ 生成兑吧签名 """
    params = [(k, params[k]) for k in sorted(params.keys())]
    raw_str = ''
    for p in params:
        raw_str += str(p[1])

    return utils.md5(raw_str)

def duiba(ordernum, audit=True):
    params = {
        "passOrderNums": ordernum if audit else '',
        "rejectOrderNums": ordernum if not audit else '',
        "timestamp": int(time.time() * 1000),
        "appKey": config['duiba']['appKey'],
        "appSecret": config['duiba']['appSecret'],
    }
    params['sign'] = sign(params)
    params.pop('appSecret')
    url = 'http://www.duiba.com.cn/audit/apiAudit'
    r = requests.get(url, params=params)
    result = json.loads(r.text.replace('\'', '\"'))
    if result['success']:
        detail = result['details'][ordernum]
        errmsg = detail['message'] if not detail['success'] else ''
        return detail['success'], errmsg
    else:
        return False, result['errorMessage']

def duiba_aos(ordernum, audit=True):
    params = {
        "passOrderNums": ordernum if audit else '',
        "rejectOrderNums": ordernum if not audit else '',
        "timestamp": int(time.time() * 1000),
        "appKey": config['duiba_aos']['appKey'],
        "appSecret": config['duiba_aos']['appSecret'],
    }
    params['sign'] = sign(params)
    params.pop('appSecret')
    url = 'http://www.duiba.com.cn/audit/apiAudit'
    r = requests.get(url, params=params)
    result = json.loads(r.text.replace('\'', '\"'))
    if result['success']:
        detail = result['details'][ordernum]
        errmsg = detail['message'] if not detail['success'] else ''
        return detail['success'], errmsg
    else:
        return False, result['errorMessage']


if __name__ == "__main__":
    main()
