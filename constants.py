#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author: chenjiehua@youmi.net
#

import os.path

""" Tornado Server 定义 """
# 接收到关闭信号后多少秒后才真正重启
MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 1
# Listen IPV4 only
IPV4_ONLY = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

COOKIE_SECRET='R2VKSkZ1WWg3RVFucDJYZFRQMW8vVm9zc2RmZXMzaz0='

SETTINGS_FILE = "settings.yaml"
DUIBA_AUDIT_QUEUE = "qianka:duiba_audit_queue"

