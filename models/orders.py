#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author: chenjiehua@youmi.net
#

"""订单操作

"""

import db

""" callback_orders """
def get_callback_orders(stime, etime):
    return db.mysql.query(
        "SELECT * FROM `callback_orders` WHERE `create_time` >= %s "
        "AND `create_time` <= %s order by create_time DESC", stime, etime)

def callback_summary(stime, etime):
    return db.mysql.get(
        "SELECT count(`id`) AS dcount, sum(`points`) AS dpoints, "
        "sum(`price`) AS dprice FROM `callback_orders` "
        "WHERE `create_time` > %s AND `create_time` <= %s",
        stime, etime)


""" global_orders """
def get_global_orders(uid):
    return db.mysql.query(
        "SELECT * FROM `global_orders` WHERE `uid` = %s "
        "ORDER BY `id` DESC", uid)


""" exchange_orders """
def exchange_summary(stime, etime):
    return db.mysql.query(
        "SELECT sum(`actual_price`) AS dprice, `status` FROM `exchange_orders` "
        "WHERE `create_time` > %s AND `create_time` <= %s GROUP BY `status`",
        stime, etime)

def get_exchange_orders(status):
    return db.mysql.query(
        "SELECT * FROM `exchange_orders` WHERE `status` = %s "
        "ORDER BY `id` DESC ", status)

def get_exchange_order_by_id(id):
    return db.mysql.get(
        "SELECT * FROM `exchange_orders` WHERE `id` = %s", id)

def update_note(id, errmsg):
    return db.mysql.execute(
        "UPDATE `exchange_orders` SET `notes` = %s "
        "WHERE `id` = %s", errmsg, id)

def set_status(id, status):
    return db.mysql.execute(
        "UPDATE `exchange_orders` SET `status`= %s "
        "WHERE `id` = %s", status, id)
