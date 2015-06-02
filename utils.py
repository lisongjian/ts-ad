#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2014 Youmi
#
# @author: chenjiehua@youmi.net
#

import yaml
import os.path
import hashlib
import logging
import base64
import time
import random

from hashlib import sha256
from hmac import HMAC

class YamlLoader(yaml.Loader):
    """ Yaml loader

    Add some extra command to yaml.

    !include:
        see http://stackoverflow.com/questions/528281/how-can-i-include-an-yaml-file-inside-another
        include another yaml file into current yaml
    """

    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(YamlLoader, self).__init__(stream)

    def include(self, node):
        filename = os.path.join(self._root, self.construct_scalar(node))
        with open(filename, 'r') as f:
            return yaml.load(f, YamlLoader)

YamlLoader.add_constructor('!include', YamlLoader.include)

class Loggers(object):
    """简单的logging wrapper"""

    def __init__(self):
        self.loggers = {}

    def use(self, log_name, log_path):
        if not log_name in self.loggers:
            logger = logging.getLogger(log_name)
            logger.setLevel(logging.INFO)
            if not logger.handlers:
                fh = logging.FileHandler(log_path)
                fh.setLevel(logging.INFO)
                formatter = logging.Formatter('%(asctime)s - %(message)s')
                fh.setFormatter(formatter)
                logger.addHandler(fh)
            self.loggers[log_name] = logger
        return self.loggers[log_name]

loggers = Loggers()

def paginator(data, page, limit=50):
    """分页器

    data: 分页数据,
    page: 指定页码,
    limit: 每页长度,
    """
    total_count = len(data)
    total_page = (total_count - 1) / limit + 1 if total_count > 0 else 0
    page = total_count / limit if page * limit > total_count else page - 1
    start = page * limit
    data = data[start:start+limit]
    pre_page = page if page > 0 else None
    next_page = page + 2 if page * limit < total_count else None
    result = {
        "data": data,
        "total_count": total_count,
        "total_page": total_page,
        "cur_page": page + 1,
        "pre_page": pre_page,
        "next_page": next_page,
    }
    return result


def md5(raw_str):
    return hashlib.new("md5", str(raw_str)).hexdigest()


def sha1(raw_str):
    return hashlib.new("sha1", str(raw_str)).hexdigest()


def gen_token():
    raw_str = '%s%s' % (time.time(), random.randint(1000000, 9999999))
    return sha1(md5(raw_str))


def encrypt_pwd(pwd, salt=None):
    """ 密码加密 """
    if salt is None:
        salt = os.urandom(8)
    else:
        salt = base64.b64decode(salt)

    result = pwd
    for i in xrange(3):
        result = HMAC(str(result), salt, sha256).hexdigest()

    return base64.b64encode(salt), result


def validate_pwd(enc_pwd, in_pwd, salt):
    """ 验证密码 """
    return enc_pwd == encrypt_pwd(in_pwd, salt)[1]

