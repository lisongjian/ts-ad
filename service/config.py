#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: chenjiehua@youmi.net
#

"""系统配置

"""

import tornado.web
from datetime import datetime
from protocols import WebBaseHandler
from models import options, changelogs,rule,activity



class ConfigHandler(WebBaseHandler):
    """ 参数配置 """

    @tornado.web.authenticated
    def get(self):
        result = options.get_options()
        level_rule = rule.getAll()
        data = {
            "title": "系统参数列表",
            "current_user": self.current_user,
            "options": result,
            "rule" : level_rule
        }
        self.render("config/index.html", **data)



class DownloadHandler(WebBaseHandler):
    """ 下载链接 """

    @tornado.web.authenticated
    def get(self):
        result = changelogs.get_changelogs()
        data = {
            "title": "小助手下载",
            "current_user": self.current_user,
            "changelogs": result,
        }
        self.render("config/download.html", **data)



class EditHandler(WebBaseHandler):
    """ 参数编辑 """

    @tornado.web.authenticated
    def get(self):
        id = self.get_argument('id', 0)
        result = options.get_option(id)
        if not result:
            return self.write("id error!")
        data = {
            "title": "系统参数编辑",
            "current_user": self.current_user,
            "succ": False,
            "errors": [],
            "option": result,
        }
        self.render("config/edit.html", **data)

    @tornado.web.authenticated
    def post(self):
        params = {}
        for key in ['id', 'key', 'values', 'description']:
            params[key] = self.get_argument(key, None)

        data = {
            "title": "系统参数编辑",
            "current_user": self.current_user,
            "succ": True,
            "errors": [],
            "option": params,
        }
        if not options.get_option(params['id']):
            data['errors'].append("ID编号错误，请返回重试！")
        if not params['values']:
            data['errors'].append("请输入数值！")
        if not params['description']:
            data['errors'].append("请输入说明！")

        if data['errors']:
            data['succ'] = False
        else:
            options.update_option(params['id'], params['values'], params['description'])
            self.redis.delete("qianka:option:%s" % params['key'])

        self.render("config/edit.html", **data)

class DownEditHandler(WebBaseHandler):
    """ 参数编辑 """

    @tornado.web.authenticated
    def get(self):
        id = self.get_argument('id', 0)
        result = changelogs.get_changelog(id)
        if not result:
            return self.write("id error!")
        data = {
            "title": "小助手下载编辑",
            "current_user": self.current_user,
            "succ": False,
            "errors": [],
            "changelog": result,
        }
        self.render("config/down_edit.html", **data)

    @tornado.web.authenticated
    def post(self):
        params = {}
        for key in ['id', 'download_url']:
            params[key] = self.get_argument(key, None)

        data = {
            "title": "小助手下载编辑",
            "current_user": self.current_user,
            "succ": True,
            "errors": [],
            "changelog": params,
        }
        if not changelogs.get_changelog(params['id']):
            data['errors'].append("ID编号错误，请返回重试！")
        if not params['download_url']:
            data['errors'].append("请输入下载链接！")

        if data['errors']:
            data['succ'] = False
        else:
            changelogs.update_changelog(params['id'], params['download_url'])
            # FIXME 加入redis
            # self.redis.delete("qianka:download_url:%s" % params['id'])

        self.render("config/down_edit.html", **data)

class LevelEditHandler(WebBaseHandler):
    """参数编辑"""
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument('id', 0)
        result = rule.getById(id)
        if not result:
            return self.write("id error")
        data = {
            "title": "等级参数编辑",
            "current_user": self.current_user,
            "succ": False,
            "errors": [],
            "rule": result,
        }
        self.render("config/level_edit.html",**data)

    @tornado.web.authenticated
    def post(self):
        params = {}
        for key in ['id', 'level', 'value', 'description']:
            params[key] = self.get_argument(key)

        data = {
            "title": "等级参数编辑",
            "current_user": self.current_user,
            "succ": True,
            "errors": [],
            "rule": params,
        }
        if not rule.getById(params['id']):
            data['errors'].append("ID编号错误，请返回重试！")
        if not params['value']:
            data['errors'].append("请输入数值！")
        if not params['description']:
            data['errors'].append("请输入说明！")

        if data['errors']:
            data['succ'] = False
        else:
            rule.updateInfo(params['id'], params['value'], params['description'])
            #self.redis.delete("qianka:option:%s" % params['key'])
        self.render("config/level_edit.html",**data)

class ActivityHandler(WebBaseHandler):
    """ 活动设置 """
    @tornado.web.authenticated
    def get(self):
        result = activity.getAll()
        data = {
            "title": "活动设置",
            "current_user": self.current_user,
            "activity": result
        }

        self.render("config/activity.html",**data)

class ActivityEditHandler(WebBaseHandler):
    """活动编辑"""
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument('id','')
        result = activity.get_id(id)
        if not result:
            return self.write("id error")
        else:
            data = {
                "title": "活动编辑",
                "current_user": self.current_user,
                "succ": False,
                "errors": [],
                "option": result,
            }
            self.render("config/act_edit.html",**data)

    @tornado.web.authenticated
    def post(self):
        params = {}
        for key in ['id', 'key', 'values', 'description', 'sdate','stime', 'edate','etime']:
            params[key] = self.get_argument(key)
        data = {
            "title": "活动设置",
            "current_user": self.current_user,
            "succ": True,
            "errors": [],
        }
        if not activity.get_id(params['id']):
            data['errors'].append("ID编号错误，请返回重试！")
        if not params['values']:
            data['errors'].append("请输入数值！")
        if not params['description']:
            data['errors'].append("请输入说明！")
        if not params['sdate']:
            data['errors'].append("请输入开始时间！")
        if not params['edate']:
            data['errors'].append("请输入结束时间！")
        if data['errors']:
            data['succ'] = False
        else:
            sdate = params['sdate'] + ' ' + params['stime']
            edate = params['edate'] + ' ' + params['etime']
            start_time = datetime.strptime(sdate,"%Y-%m-%d %H:%M:%S")
            end_time = datetime.strptime(edate,"%Y-%m-%d %H:%M:%S")

            activity.updateInfo(params['id'], params['key'], \
            params['values'], params['description'],start_time, end_time)

        result = activity.get_id(params['id'])
        data['option'] = result
        self.render("config/act_edit.html",**data)

