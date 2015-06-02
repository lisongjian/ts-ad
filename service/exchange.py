#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: chenjiehua@youmi.net
#

"""兑换相关

"""

import tornado.web
import constants
import ujson as json
from utils import paginator
from protocols import WebBaseHandler
from models import orders

class OrdersHandler(WebBaseHandler):
    """ 兑换订单 """

    @tornado.web.authenticated
    def get(self):
        page = int(self.get_argument('page', 1))
        status = int(self.get_argument('status', 10))
        data = orders.get_exchange_orders(status)
        result = paginator(data, page)
        data = {
            "title": "兑换订单列表",
            "current_user": self.current_user,
            "orders": result,
            "status": status,
        }
        self.render('exchange/index.html', **data)


class SearchHandler(WebBaseHandler):
    """ 订单搜索 """

    @tornado.web.authenticated
    def get(self):
        keys = ['uid', 'address', 'ip', 'sdate', 'edate', 'status', 'ip_address']
        params = {}
        for key in keys:
            params[key] = self.get_argument(key, '').encode('utf-8')

        where_clause = []
        for key in ['uid', 'address', 'ip', 'status' , 'ip_address']:
            if params[key] == '':
                continue
           # where_clause.append("%s = '%s'" % (key,params[key]))
           # print params[key] + '========================'
           # print 'key'
            if params[key] != params['ip_address']:
                where_clause.append("%s = '%s'" % (key, params[key]))
            else:
                where_clause.append("%s REGEXP '%s'" % (key, params[key]))
        if params['sdate']:
            where_clause.append("create_time>='%s'" % params['sdate'])
        if params['edate']:
            where_clause.append("create_time<='%s'" % params['edate'])

        if where_clause:
            sql = "SELECT * FROM `exchange_orders` WHERE " + ' AND '.join(where_clause)
        else:
            sql = "SELECT * FROM `exchange_orders` ORDER BY `id` DESC"
        data = self.db.query(sql)
        export = self.get_argument('export', 0)
        count = 0
        for d in data:
           str(data[count]['create_time'])
           data[count]['create_time'] = d.create_time.strftime("%Y-%m-%d %H:%M:%S")
           count += 1
        if export:
            ex = {
                "data": data
            }
            """导出订单"""
            #data_json = tornado.escape.json_encode(data)

            self.set_header("Content-Type", 'application/ms-excel;charset=utf-8 ')
            self.set_header("Content-Disposition", "attachment; filename=export_file.xls;charset=utf-8")
            #self.write(data_json)
            return self.render("exchange/export_xls.html", **ex)
            #response['Content-Disposition'] = 'attachment; filename=export_file.xls'
            #response['Content-Type'] = 'application/ms-excel; charset=utf-8'

        #self.web.header('Content-type','application/vnd.ms-excel')
        #self.web.headerheader('Transfer-Encoding','chunked')
        #self.web.header('Content-Disposition','attachment;filename="export.xls"')
        #h = HTTPHeaders({"Content-type", "application/ms-excel"})
        #print h
        #response = self.render("exchange/export_xls.html", data)
        #response['Content-Disposition'] = 'attachment; filename=export_file.xls'
        #response['Content-Type'] = 'application/ms-excel; charset=utf-8'
        #return response


        page = int(self.get_argument('page', 1))
        result = paginator(data, page)
        data = {
            "title": "订单搜索结果",
            "current_user": self.current_user,
            "orders": result,
            "params": params,
        }
        self.render("exchange/search.html", **data)


class AuditHandler(WebBaseHandler):
    """ 审核订单 """

    @tornado.web.authenticated
    def post(self):
        accept = self.get_argument('accept', '')
        reject = self.get_argument('reject', '')
        result = [{"id": 388, "status": 11}]
        result.extend(self._deal_order(accept, True))
        result.extend(self._deal_order(reject, False))
        self.write_json(result)

    def _deal_order(self, orderids, audit=True):
        """ 处理订单，写入redis缓存 """
        result = []
        if not orderids:
            return result
        oids = orderids[:-1].split(',')
        for oid in oids:
            status = 11 if audit else 12
            orders.set_status(oid, status)
            result.append({"id": oid, "status": status})
            self.redis.rpush(constants.DUIBA_AUDIT_QUEUE,
                             json.dumps({"id":oid, "audit": audit}))

        return result


class NoteHandler(WebBaseHandler):
    """ 订单备注 """

    @tornado.web.authenticated
    def post(self):
        pass
