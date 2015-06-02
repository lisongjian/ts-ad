#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015 Youmi
#
# @author: chenjiehua@youmi.net
#

"""用户反馈相关操作

"""

import db

def get_feedbacks():
    return db.mysql.query("SELECT * FROM `feedbacks`")

def get_feedback(id):
    return db.mysql.get(
        "SELECT * FROM `feedbacks` WHERE `id` = %s", id)

def set_status(id, status):
    return db.mysql.execute(
        "UPDATE `feedbacks` SET `status` = %s "
        "WHERE `id` = %s", status, id)
