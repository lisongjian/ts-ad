#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: chenjiehua@youmi.net
#

"""数据统计脚本

每隔一定时间间隔统计一次数据，将其写入redis，提高后台数据加载速度
"""

import yaml
import torndb
import redis
import ujson as json
import time
import db

from utils import YamlLoader
from datetime import date, timedelta
from models import orders, users,summary


SETTINGS_FILE = "settings.yaml"

# MySQL数据库连接配置
try:
    config = yaml.load(file(SETTINGS_FILE, 'r'), YamlLoader)
except yaml.YAMLError as e:
    print "Error in configuration file: %s" % e

# 数据库连接实例
db.mysql = torndb.Connection(**config['mysql'])
pool = redis.ConnectionPool(**config['redis'])
db.redis = redis.Redis(connection_pool=pool)

def earn_stat(stime, etime):
    """ 赚取效果 """
    earn_data = orders.callback_summary(stime, etime)
    result = {
        "total_earn": earn_data['dpoints'] if earn_data['dpoints'] else 0,
        "total_price": earn_data['dprice'] if earn_data['dprice'] else 0,
        "total_count": earn_data['dcount'],
    }
    average_earn = float(result['total_earn']) / float(result['total_count']) \
        if result['total_count'] else 0
    result['total_earn'] = int(result['total_earn'])
    result['total_price'] = '%.2f' % result['total_price']
    result['average_earn'] = '%.2f' % average_earn
    return result

def exchange_stat(stime, etime):
    exchange_data = orders.exchange_summary(stime, etime)
    result = {
        "total_order": 0,
        "reject_order": 0,
    }
    if exchange_data:
        for ex_data in exchange_data:
            result['total_order'] += ex_data['dprice']
            if ex_data['status'] in [12, 14]:
                result['reject_order'] += ex_data['dprice']
    result['total_order'] = '%.2f' % result['total_order']
    result['reject_order'] = '%.2f' % result['reject_order']
    return result

def user_stat(stime, etime):
    user_today = users.user_summary(stime, etime)
    user_all = users.all_summary()
    user_last_login = users.user_last_login(stime, etime)
    result = {
        "total_ios": 0,
        "total_aos": 0,
        "total_all": 0,
        "today_ios": 0,
        "today_aos": 0,
        "today_all": 0,
        "last_ios":  0,
        "last_aos":  0,
        "last_login":  0,
    }
    if user_today:
        for ud in user_today:
            result['today_aos'] += ud['dcount'] if ud['platform'] == 1 else 0
            result['today_ios'] += ud['dcount'] if ud['platform'] == 2 else 0
            result['today_all'] += ud['dcount']
    if user_all:
        for ud in user_all:
            result['total_aos'] += ud['dcount'] if ud['platform'] == 1 else 0
            result['total_ios'] += ud['dcount'] if ud['platform'] == 2 else 0
            result['total_all'] += ud['dcount']
    if user_last_login:
        for ud in user_last_login:
            result['last_aos'] += ud['dcount'] if ud['platform'] == 1 else 0
            result['last_ios'] += ud['dcount'] if ud['platform'] == 2 else 0
            result['last_login'] += ud['dcount']
    return result

"""Now Day Login Users Sum"""
def day_sum_login():
    stime = date.today()
    etime = stime + timedelta(days=1)
    last_login = users.get_user_last_login(stime,etime)
    for l in last_login:
        today_login = db.redis.hget(stime,l['uid'])
        if not today_login:
            db.redis.hset(stime,l['uid'],l['platform'])
    count = db.redis.hlen(stime)
    sum_last = summary.get_summary_by_date(stime)
    if not sum_last:
        db.mysql.execute("INSERT INTO `summary` VALUES(\
        NULL,%s,0,0,0,0,0,0,0,0,0,0,%s)",stime,count)
    else:
        if sum_last[0]['last_login'] != count :
            db.mysql.execute("UPDATE `summary` SET `last_login` = %s \
                            WHERE `date` = %s" ,count,stime)


def main():
    while True:
        stime = date.today().strftime("%Y-%m-%d")
        etime = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        result = {}
        result.update(earn_stat(stime, etime))
        result.update(exchange_stat(stime, etime))
        result.update(user_stat(stime, etime))
        db.redis.setex("qianka:summary:%s" % stime, json.dumps(result), 1000)
        day_sum_login()
        time.sleep(900)

if __name__ == "__main__":
    main()
