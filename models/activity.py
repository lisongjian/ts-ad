#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: chenjiehua@youmi.net
#

import db


def get(key):
    data = db.mysql.get(
        "SELECT * FROM `activity` WHERE `key` = %s", key)
    return data if data else 0

def getAll():
    return db.mysql.query(
        "SELECT * FROM `activity`"
    )

def get_id(id):
    return db.mysql.get(
        "SELECT * FROM `activity` WHERE `id` =%s", id
    )

def updateInfo(id, key, values, description, start_time, end_time):
    return db.mysql.execute(
        "UPDATE `activity` SET `key` = %s, `values` = %s, `description` = %s, \
        start_time = %s, end_time = %s WHERE `id` = %s",key,values,description, \
        start_time,end_time,id
    )
