#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author: chenjiehua@youmi.net
#

import tornado.web
import torndb
import redis
import os.path
import server
import db

from protocols import WebBaseHandler
from service import account, user, summary, \
    earn, exchange, config, feedback

try:
    import __pypy__
except ImportError:
    __pypy__ = None

class Application(server.Application):

    def startup(self):
        self.db = db.mysql = torndb.Connection(**self.config['mysql'])
        pool = redis.ConnectionPool(**self.config['redis'])
        self.redis = db.redis = redis.Redis(connection_pool=pool)


class MainHandler(WebBaseHandler):
    """ 测试 """

    @tornado.web.authenticated
    def get(self):
        print self.current_user
        self.write("hello world!")


if __name__ == "__main__":
    static_path = os.path.join(os.path.dirname(__file__), "static")

    handlers = [
        (r'/static/(.*)',
            tornado.web.StaticFileHandler,
            {'path': static_path}),
        (r"/", account.LoginHandler),
        # 登陆相关
        (r"/account/login", account.LoginHandler),
        (r"/account/logout", account.LogoutHandler),
        (r"/account/changepwd", account.ChangePwdHandler),

        # 汇总相关
        (r"/summary", summary.SummaryHandler),
        (r"/summary/user", summary.UserHandler),
        (r"/summary/earn", summary.EarnHandler),
        (r"/summary/exchange", summary.ExchangeHandler),

        # 用户相关
        (r"/user", user.UserHandler),
        (r"/user/detail", user.DetailHandler),
        (r"/user/search", user.SearchHandler),
        (r"/user/detail/(?P<uid>\d+)/$", user.UserDetailHandler),

        # 赚取相关
        (r"/earn", earn.EarnHandler),

        # 兑换管理
        (r"/exchange", exchange.OrdersHandler),
        (r"/exchange/search", exchange.SearchHandler),
        (r"/exchange/audit", exchange.AuditHandler),
        (r"/exchange/note", exchange.NoteHandler),

        # 系统设置
        (r"/config", config.ConfigHandler),
        (r"/config/edit", config.EditHandler),
        (r"/download", config.DownloadHandler),
        (r"/download/edit", config.DownEditHandler),
        (r"/config/leveledit",config.LevelEditHandler),
        (r"/activity",config.ActivityHandler),
        (r"/activity/edit",config.ActivityEditHandler),

        # 用户反馈
        (r"/feedback", feedback.FeedbackHandler),
        (r"/feedback/deal", feedback.DealHandler),

        # 测试
        (r"/test", MainHandler),
    ]

    server.mainloop(Application(handlers))
