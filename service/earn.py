#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: chenjiehua@youmi.net
#

"""赚取相关

"""

import tornado.web

from datetime import datetime,date, timedelta
from protocols import WebBaseHandler
from models import orders
from utils import paginator


class EarnHandler(WebBaseHandler):
    """ 赚取效果 """

    @tornado.web.authenticated
    def get(self):
        sdate = self.get_argument('sdate', '')
        edate = self.get_argument('edate','')
        page = self.get_argument('page', 1)
        print page
        if not sdate and not edate:
            etime = date.today().strftime("%Y-%m-%d")
            stime = (date.today() + timedelta(days=-14))
        else:
            stime = sdate
           # etime = datetime.strptime(qdate, "%Y-%m-%d") +timedelta(days=1)
            etime = edate
        if stime == etime:
            qdate = etime
        else:
            qdate = str(stime) + ' - ' + str(etime)
        cborders = orders.get_callback_orders(stime, datetime.strptime(etime,"%Y-%m-%d")+timedelta(days = 1))
        result = paginator(cborders, int(page))
        print result
        data = {
            "title": "广告激活列表",
            "current_user": self.current_user,
            "total": len(cborders),
            "qdate": qdate,
            "sdate": stime,
            "edate": etime,
            "orders": result,
        }
        export = self.get_argument('export',0)
        if export:
            ex = {
                "data" : data
            }
            self.set_header("Content-Type", 'application/ms-excel;charset=utf-8')
            self.set_header("Content-Disposition", "attachment; filename=export_file.xls;charset=utf-8")
            return self.render("earn/export_xls.html",**ex)

        self.render("earn/index.html", **data)
