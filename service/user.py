#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: chenjiehua@youmi.net
#

"""用户信息相关

"""

import tornado.web

from utils import paginator
from protocols import WebBaseHandler
from models import users, orders
from datetime import datetime, date, timedelta


class UserHandler(WebBaseHandler):
    """ 用户列表 """

    @tornado.web.authenticated
    def get(self):
        page = int(self.get_argument('page', 1))
        platform = self.get_argument('platform','')
        orderby = self.get_argument('orderby', 'uid')
        data = []
        strdate, sdate, edate = parse_date(self)
# if strdate:
#           data = users.get_user_time(sdate, edate)##
#       if orderby == 'total_sons':
#           data = users.get_users_by_ttsons(sdate,edate)
#elif orderby != 'uid':
        if orderby == 'total_sons':
            data = users.get_users_by_ttsons(sdate,edate,platform)
        elif orderby != 'uid':
            data = users.get_users(sdate,edate,orderby,platform)
        else:
		    data = users.get_user_time(sdate, edate,platform)
        #test = users.get_user_platform(sdate,edate,2,orderby)
        #print test
        result = paginator(data, page)
        data = {
            "title": "用户信息列表",
            "current_user": self.current_user,
            "users": result,
            "orderby": orderby,
            "strdate": strdate,
	   	    "sdate" : strdate['s'],
	        "edate" : strdate['e'],
            "platform" : platform
        }
        self.render("user/index.html", **data)


class DetailHandler(WebBaseHandler):
    """ 用户详细信息 """

    @tornado.web.authenticated
    def get(self):
        uid = self.get_argument('uid', 0)
        status = self.get_argument('status', 0)
        vip = self.get_argument('vip',"")
        if vip != "":
            users.set_user_vip(uid,vip)
        if status:
            users.set_user_status(uid, status)
        page = int(self.get_argument('page', 1))
        user_info = users.get_user(uid)
        ip_info = users.get_user_ips(uid)
        device_info = users.get_device(uid)
        if not device_info:
            device_info = {}
        data = orders.get_global_orders(uid)
        result = paginator(data, page)
        data = {
            "title": "用户详细信息",
            "current_user": self.current_user,
            "user": user_info,
            "device": device_info,
            "orders": result,
            "ips": ip_info,
        }
        self.render("user/detailaos.html", **data)


class SearchHandler(WebBaseHandler):
    """ 用户搜索 """

    @tornado.web.authenticated
    def get(self):
        field = {}
        page = self.get_argument('page',1)
        sdate = self.get_argument('sdate','')
        edate = self.get_argument('edate','')
        keys = ['tid', 'phone', 'username', 'uid', 'pkg']
        key_ifa = ['ifa']
        key_un = ['un']
        where_clause = []
        where_clause_ifa = []
        where_clause_un = []
        for k in keys:
            value = self.get_argument(k, '')
            field[k] = value
            if value:
                where_clause.append("%s='%s'" % (k, value))
        if sdate != '':
            where_clause.append("`create_time`>='%s'" % (sdate))
        if edate != '':
            where_clause.append("`create_time`<='%s'" % (edate))
        for k in key_ifa:
            value_ifa = self.get_argument(k, '')
            field[k] = value_ifa
            if value_ifa:
                ifa=value_ifa.replace('-','').lower()
                where_clause_ifa.append("%s='%s'" % (k, ifa))
        for k in key_un:
            value_un = self.get_argument(k, '')
            field[k] = value_un
            if value_un:
                where_clause_un.append("%s='%s'" % (k, value_un))

        result = {
            "data": [],
        }
        if where_clause_ifa and self.get_argument('ifa', '') !='':
            '''通过ifa查找'''
            userinfo = self.db.get("SELECT * FROM `devices` WHERE `ifa`= %s", ifa)
            if userinfo:
                uid = int(userinfo['uid'])
                where = "uid = '%s'" % uid
                result['data'] = self.db.query("SELECT * FROM `users` WHERE " + where)
        if where_clause_un and self.get_argument('un', '') !='':
            '''通过设备名称查找'''
            userinfo = self.db.get("SELECT * FROM `devices` WHERE `device_name` REGEXP %s", value_un)
            if userinfo:
                uid = int(userinfo['uid'])
                where = "uid = '%s'" % uid
                result['data'] = self.db.query("SELECT * FROM `users` WHERE " + where)
        if where_clause and self.get_argument('ifa') == '':
            where = ' AND '.join(where_clause)
            result['data'] = self.db.query("SELECT * FROM `users` WHERE " + where)
        field['sdate'] = sdate
        field['edate'] = edate
        result = paginator(result['data'], int(page))
        data = {
            "title": "用户搜索结果",
            "current_user": self.current_user,
            "users": result,
            "field": field
        }
        self.render("user/search.html", **data)

class UserDetailHandler(WebBaseHandler):
    """用户详细"""
    def get(self):
        keys = ['uid']
        where_clause = []
        for k in keys:
            value = self.get_argument(k, '')
            if value:
                where_clause.append("%s='%s'" % (k, value))
        result = {
            "data": [],
        }
        if where_clause:
            where = ' AND '.join(where_clause)
            result['data'] = self.db.query("SELECT * FROM `users` WHERE " + where)

        data = {
            "title": "用户详情",
            "current_user": self.current_user,
            "users": result,
        }
        self.render("user/detail.html", **data)

def parse_date(req_handler):
    """处理日期"""
    edate = req_handler.get_argument('edate', None)
    sdate = req_handler.get_argument('sdate', None)
    strdate = {}
    if edate:
        strdate['e'] = edate
        edate = datetime.strptime(edate, "%Y-%m-%d")
    else:
        edate = date.today()
        strdate['e'] = edate.strftime("%Y-%m-%d")
    if sdate:
        strdate['s'] = sdate
        sdate = datetime.strptime(sdate, "%Y-%m-%d")
    else:
        sdate = date.today() - timedelta(days=14)
        strdate['s'] = sdate.strftime("%Y-%m-%d")

    return strdate, sdate, edate
