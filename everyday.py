#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2015
#
# @author: chenjiehua@youmi.net
#

"""每日数据统计

使用crontab定时任务，每天01:15统计前天数据，部分数据如：
兑换订单由于审核状态修改，需重复统计前3天以获得准确数据。
"""

from __future__ import division
import yaml
import torndb
import db
from utils import YamlLoader
from datetime import date, timedelta
from models import orders, users

SETTINGS_FILE = "settings.yaml"

# MySQL数据库连接配置
try:
    config = yaml.load(file(SETTINGS_FILE, 'r'), YamlLoader)
except yaml.YAMLError as e:
    print "Error in configuration file: %s" % e

# 数据库连接实例
db.mysql = torndb.Connection(**config['mysql'])
def users_stat(day):
    """ 统计用户 """
    nextday = day + timedelta(days=1)
    stats = users.user_summary(day, nextday)
    result = {}.fromkeys(['user_ios', 'user_aos'], 0)
    for s in stats:
        result['user_aos'] += s['dcount'] if s['platform'] == 1 else 0
        result['user_ios'] += s['dcount'] if s['platform'] == 2 else 0

    return result

def last_login(day):
    """ 活跃用户 """
    nextday = day + timedelta(days=1)
    stats = users.user_last_login(day, nextday)
    result = {}.fromkeys(['last_ios', 'last_aos', 'last_login'], 0)
    for s in stats:
        result['last_aos'] += s['dcount'] if s['platform'] == 1 else 0
        result['last_ios'] += s['dcount'] if s['platform'] == 2 else 0
        result['last_login'] = result['last_aos'] + result['last_ios']
    return result

def earns_stat(day):
    """ 赚取统计 """
    nextday = day + timedelta(days=1)
    stats = orders.callback_summary(day, nextday)
    result = {
        "earns": stats['dpoints'] if stats['dpoints'] else 0,
        "prices": stats['dprice'] if stats['dprice'] else 0,
        "tasks": stats['dcount'],
    }
    return result

def finance_stat(day):
    """ 财务统计 """
    nextday = day + timedelta(days=1)
    stats = orders.exchange_summary(day, nextday)
    result = {}.fromkeys(['duiba', 'fail', 'fact'], 0)
    for s in stats:
        result['duiba'] += s['dprice']
        if s['status'] in [12, 14]:
            result['fail'] += s['dprice']

    result['fact'] = result['duiba'] - result['fail']
    return result

def save_stat(day, d):
    """ 保存统计数据 """
    flag = db.mysql.get(
        "SELECT `id` FROM `summary` WHERE `date` = %s", day)
    if not flag:
        db.mysql.execute(
            "INSERT INTO `summary`(`date`, `user_ios`, `user_aos`, `earns`, `prices`, "
            "`tasks`, `duiba`, `fail`, `fact`, `profit`, `profit_rate`)"
            "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            day, d['user_ios'], d['user_aos'], d['earns'], d['prices'], d['tasks'],
            d['duiba'], d['fail'], d['fact'], d['profit'], d['profit_rate'])
    else:
        db.mysql.execute(
            "UPDATE `summary` SET `user_ios` = %s, `user_aos` = %s, `earns` = %s, "
            "`prices` = %s, `tasks` = %s, `duiba` = %s, `fail` = %s, `fact` = %s, "
            "`profit` = %s, `profit_rate` = %s WHERE `date` = %s", d['user_ios'],
            d['user_aos'], d['earns'], d['prices'], d['tasks'], d['duiba'], d['fail'],
            d['fact'], d['profit'], d['profit_rate'], day)

def main():
    today = date.today()
    for i in range(4)[1:]:
        day = today - timedelta(days=i)
        result = {}
        result.update(users_stat(day))
        result.update(earns_stat(day))
        result.update(finance_stat(day))
        result.update(last_login(day))
        result['profit'] = result['prices'] - result['fact']
        result['profit_rate'] = result['profit'] / result['prices'] \
            if result['prices'] else 0
        result['profit_rate'] = '%.4f' % result['profit_rate']
        save_stat(day, result)
if __name__ == "__main__":
    main()
