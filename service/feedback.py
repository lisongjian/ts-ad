#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2015
#
# @author: chenjiehua@youmi.net
#

"""用户反馈相关

"""

import tornado.web

from utils import paginator
from protocols import WebBaseHandler
from models import feedback

class FeedbackHandler(WebBaseHandler):
    """ 用户反馈列表 """

    @tornado.web.authenticated
    def get(self):
        page = int(self.get_argument('page', 1))
        data = feedback.get_feedbacks()
        result = paginator(data, page)
        data = {
            "title": "用户反馈列表",
            "current_user": self.current_user,
            "fbs": result,
        }
        self.render("feedback/index.html", **data)


class DealHandler(WebBaseHandler):
    """ 标记用户反馈 """

    @tornado.web.authenticated
    def get(self):
        id = self.get_argument('id', None)
        feedback.set_status(id, 1)
