#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright Youmi 2014
#
# @author: chenyongjian@youmi.net
#

import db

def get(level):
    data = db.mysql.get(
        "SELECT `value` FROM `level_rule` WHERE `level` = %s", level)
    return data['value'] if data else 0

def getAll():
    return db.mysql.query("SELECT * FROM `level_rule` ORDER BY `id` DESC")

def getById(id):
    data = db.mysql.get("SELECT * FROM `level_rule` WHERE `id` = %s",id)
    return data if data else 0

def updateInfo(id,value,description):
    return db.mysql.execute(
        "UPDATE `level_rule` SET `value`=%s, `description`=%s \
        WHERE `id` = %s",value,description,id)

