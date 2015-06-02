#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015 Youmi
#
# @author: chenjiehua@youmi.net
#

"""统计相关操作

"""

import db

def get_summary(sdate, edate):
    return db.mysql.query(
        "SELECT * FROM `summary` WHERE `date`>= %s "
        "AND `date` <= %s ORDER BY `date` DESC",
        sdate, edate)

def get_summary_by_date(date):
    return db.mysql.query(
        "SELECT * FROM `summary` WHERE `date` = %s" , date
    )



