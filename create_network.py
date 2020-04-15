#!/usr/bin/env python

# -*- encoding: utf-8 -*-

'''
@Author  :   xuqiang

@License :   (C) Copyright 2020-, H3C

@Contact :   xu.qiang@h3c.com

@Software:   f8s

@File    :   create_network.py

@Time    :   20200211

@Desc    :

'''
from fisco.fisco import  Fisco
from config.config import *

fisco=Fisco(FISCO_HOME,"fisco")
fisco.create_network()