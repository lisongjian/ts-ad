#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author: chenjiehua@youmi.net
#

"""用户登陆相关操作

"""

import db

def get_info(id):
    return db.mysql.get(
        "SELECT * FROM `accounts` WHERE `id` = %s "
        "AND `status` = 1", id)

def get_info_by_username(username):
    return db.mysql.get(
        "SELECT * FROM `accounts` WHERE `username` = %s "
        "AND `status` = 1", username)
