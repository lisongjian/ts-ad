#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author: chenjiehua@youmi.net
#

import tornado.web
import ujson as json

from models import accounts


class WebBaseHandler(tornado.web.RequestHandler):

    @property
    def config(self):
        return self.application.config

    @property
    def db(self):
        return self.application.db

    @property
    def redis(self):
        return self.application.redis

    def write_json(self, response=None):
        """Write json to client"""
        self.set_header('Content-type', 'application/json; charset=UTF-8')
        self.write(json.dumps(response))
        self.finish()

    def return_success(self):
        self.write_json({"c": 0})

    def return_result(self, result={}):
        self.write_json({"c": 0, "d": result})

    def return_error(self, code, message=None):
        if not message:
            message = code[1]
        self.write_json({"c": code[0], "err": message})

    def get_current_user(self):
        token = self.get_secure_cookie('token')
        if not token:
            return None

        ac = accounts.get_info(self.redis.get(token))
        if ac:
            self.set_secure_cookie('token', token, expires_days=1)
            self.redis.setex(token, ac['id'], 86400)
            return ac
        else:
            return None

