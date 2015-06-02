#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author: chenjiehua@youmi.net
#

"""用户相关操作

"""

import db
""" users表 """
def all_users():
	return db.mysql.query("SELECT * FROM `users`")

def get_user(uid):
    return db.mysql.get(
        "SELECT * FROM `users` WHERE `uid` = %s", uid)

def get_users(stime,etime,orderby,platform):
    if platform == "":
        return db.mysql.query(
            "SELECT * FROM `users` "
            "WHERE `create_time`> %s AND `create_time` < %s ORDER BY `"+orderby+"` DESC", stime, etime)
    else:
        return db.mysql.query(
            "SELECT * FROM `users` "
            "WHERE `create_time`> %s AND `create_time` < %s AND `platform` = %s  ORDER BY `"+orderby+"` DESC", stime, etime,platform)


def get_user_time(stime, etime, platform):
    if platform == "":
        return db.mysql.query(
            "SELECT * FROM `users` "
            "WHERE `create_time`> %s AND `create_time` < %s  ORDER BY `uid` DESC", stime, etime)
    else:
        return db.mysql.query(
            "SELECT * FROM `users` "
            "WHERE `create_time`> %s AND `create_time` < %s AND `platform`=%s  ORDER BY `uid` DESC", stime, etime,platform)

def get_users_by_ttsons(stime,etime,platform):
    if platform == "":
        return db.mysql.query(
            "SELECT * FROM `users` "
            "WHERE `create_time`> %s AND `create_time` < %s  ORDER BY `sons` +`grandsons` DESC", stime, etime)
    else:
        return db.mysql.query(
                "SELECT * FROM `users` "
                "WHERE `create_time`> %s AND `create_time` < %s AND `platform`=%s  ORDER BY `sons` +`grandsons` DESC", stime, etime,platform)


def user_summary(stime, etime):
    return db.mysql.query(
        "SELECT count(`uid`) AS dcount, `platform` FROM `users` "
        "WHERE `create_time`> %s AND `create_time` < %s "
        "GROUP BY `platform`", stime, etime)

def user_last_login(stime, etime):
    return db.mysql.query(
        "SELECT count(`uid`) AS dcount, `platform` FROM `users` "
        "WHERE `last_login`> %s AND `last_login` < %s "
        "GROUP BY `platform`", stime, etime)

def all_summary():
    return db.mysql.query(
        "SELECT count(`uid`) AS dcount, `platform` FROM `users` "
        "GROUP BY `platform`")
"""用户ip"""
def get_user_ips(uid):
    return db.mysql.query(
        "SELECT * FROM `ip_info` WHERE `uid` = %s "
        "ORDER BY `id` DESC", uid)

""" devices表 """
def get_device(uid):
    return db.mysql.get(
        "SELECT * FROM `devices` WHERE `uid` = %s", uid)

def get_device_byifa(ifa):
    return db.mysql.get(
        "SELECT * FROM `devices` WHERE `ifa` = %s", ifa)

"""用户状态"""
def set_user_status(uid, status):
    info=db.mysql.execute(
        "UPDATE `users` SET `status`=%s \
        WHERE `uid`=%s", status, uid)
    return info

"""VIP设置"""
def set_user_vip(uid,vip):
    info = db.mysql.execute(
        "UPDATE `users` SET `vip`=%s \
        WHERE `uid`=%s",vip , uid)
    return info

"""当天登录"""
def get_user_last_login(stime,etime):
    return db.mysql.query(
        "SELECT `uid`,`platform`,`last_login` FROM `users` \
        WHERE `last_login` >= %s AND `last_login` < %s" , stime,etime)

"""用户等级"""
def set_user_level(uid,level):
    return db.mysql.execute(
        "UPDATE `users` SET `grade` = %s WHERE `uid` = %s",level,uid
    )

"""用户使用设备"""
def get_user_platform(stime,etime,platform,orderby):
    return db.mysql.query(
        "SELECT * FROM `users` "
		"WHERE `create_time`> %s AND `create_time` < %s AND `platform` = %s ORDER BY `"+orderby+"` DESC", stime, etime , platform)

