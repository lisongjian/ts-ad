#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: chenjiehua@youmi.net
#

"""汇总数据相关

"""

import tornado.web
import ujson as json

from datetime import datetime, date, timedelta
from protocols import WebBaseHandler
from models import summary

class SummaryHandler(WebBaseHandler):
    """ 汇总数据 """

    @tornado.web.authenticated
    def get(self):
        key_name = "qianka:summary:%s" % date.today().strftime("%Y-%m-%d")
        today = self.redis.get(key_name)
        if not today:
            keys = ['total_earn', 'total_price', 'total_count', 'total_order',
                    'reject_order', 'total_ios', 'total_aos', 'total_all',
                    'today_ios', 'today_aos', 'today_all', 'average_earn']
            today = {}.fromkeys(keys, 0)
        else:
            today = json.loads(today)

        edate = date.today() + timedelta(days=1)
        sdate = date.today() - timedelta(days=7)
        history = summary.get_summary(sdate, edate)
        data = {
            "title": "汇总数据",
            "current_user": self.current_user,
            "today": today,
            "history": history,
        }
        self.render("summary/index.html", **data)


class UserHandler(WebBaseHandler):
    """ 用户统计 """

    @tornado.web.authenticated
    def get(self):
        strdate, sdate, edate = parse_date(self)
        history = summary.get_summary(sdate, edate)
        data = {
            "title": "近期用户统计",
            "current_user": self.current_user,
            "history": history,
            "strdate": strdate,
        }
        self.render("summary/user.html", **data)


class EarnHandler(WebBaseHandler):
    """ 赚取统计 """

    @tornado.web.authenticated
    def get(self):
        strdate, sdate, edate = parse_date(self)
        history = summary.get_summary(sdate, edate)
        data = {
            "title": "近期赚取统计",
            "current_user": self.current_user,
            "history": history,
            "strdate": strdate,
        }
        self.render("summary/earn.html", **data)


class ExchangeHandler(WebBaseHandler):
    """ 兑换统计 """

    @tornado.web.authenticated
    def get(self):
        strdate, sdate, edate = parse_date(self)
        history = summary.get_summary(sdate, edate)

        #兑吧统计
        countDuiba = 0.0
        #拒绝统计
        countFail = 0.0
        #实际统计
        countFact = 0.0
        #利润统计
        countProfit = 0.0
        #利润率统计
       # countProfitRate = 0.0
        #平台结算统计
        countPrices = 0.0
        for d in history:
            countDuiba += d['duiba']
            countFail += d['fail']
            countFact += d['fact']
            countProfit += d['profit']
            countPrices += d['prices']
        countProfitRate = countProfit / countPrices
        countProfitRate = round(countProfitRate,4)
        data = {
            "title": "近期兑换统计",
            "current_user": self.current_user,
            "history": history,
            "strdate": strdate,
            "countDuiba" : countDuiba,
            "countFail" : countFail,
            "countFact" : countFact,
            "countProfit" : countProfit,
            "countProfitRate" : countProfitRate,
            "countPrices" : countPrices
        }

#	print `countDuiba`
        self.render("summary/exchange.html", **data)


def parse_date(req_handler):
    """ 处理日期 """
    edate = req_handler.get_argument('edate', None)
    sdate = req_handler.get_argument('sdate', None)
    strdate = {}
    if edate:
        strdate['e'] = edate
        edate = datetime.strptime(edate, '%Y-%m-%d')
    else:
        edate = date.today()
        strdate['e'] = edate.strftime("%Y-%m-%d")

    if sdate:
        strdate['s'] = sdate
        sdate = datetime.strptime(sdate, '%Y-%m-%d')
    else:
        sdate = date.today() - timedelta(days=14)
        strdate['s'] = sdate.strftime("%Y-%m-%d")

    return strdate, sdate, edate

