#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: chenjiehua@youmi.net
#

"""用户登陆相关

"""

import tornado.escape
import utils

from protocols import WebBaseHandler
from models import accounts

class LoginHandler(WebBaseHandler):
    """ 用户登陆 """

    def get(self):
        if self.current_user:
            return self.redirect(self.get_argument('next', '/summary'))
        self.render('account/login.html', errors=[])

    def post(self):
        errors = []
        next_url = self.get_argument('next', '/summary')
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        if not username:
            errors.append("请输入用户名！")
        if not password:
            errors.append("请输入用户密码!")
        if errors:
            return self.render('account/login.html', errors=errors)

        username = tornado.escape.xhtml_escape(username)
        ac = accounts.get_info_by_username(username)
        if ac and utils.validate_pwd(ac['pwd'], password, ac['salt']):
            token = utils.gen_token()
            self.set_secure_cookie('token', token, expires_days=1)
            self.redis.setex(token, ac['id'], 86400)
            self.redirect(next_url)
        else:
            errors.append("用户名或密码错误！")
            return self.render("account/login.html", errors=errors)


class LogoutHandler(WebBaseHandler):
    """ 用户登出 """

    def get(self):
        self.clear_cookie('token')
        login_url = self.get_login_url()
        self.redirect(login_url)


class ChangePwdHandler(WebBaseHandler):
    """ 修改密码 """

    def get(self):
        pass

    def post(self):
        pass
