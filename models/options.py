#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015 Youmi
#
# @author: chenjiehua@youmi.net
#

"""参数相关操作

"""

import db

def get_options():
    return db.mysql.query("SELECT * FROM `options`")

def get_option(id):
    return db.mysql.get(
        "SELECT * FROM `options` WHERE `id` = %s", id)

def update_option(id, values, description):
    return db.mysql.execute(
        "UPDATE `options` SET `values` = %s, `description` = %s "
        "WHERE `id` = %s", values, description, id)
