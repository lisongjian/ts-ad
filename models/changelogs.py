#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author: lisongjian@youmi.net
#

"""小助手下载链接

"""

import db

""" changelogs """

def get_changelogs():
    return db.mysql.query("SELECT * FROM `changelogs`")

def get_changelog(id):
    return db.mysql.get("SELECT * FROM `changelogs` WHERE `id` = %s ", id)

def update_changelog(id, download_url):
        return db.mysql.execute(
                "UPDATE `changelogs` SET `download_url` = %s "
                "WHERE `id` = %s", download_url, id)

