#!/usr/bin/env python

# -*- encoding: utf-8 -*-

'''
@Author  :   xuqiang

@License :   (C) Copyright 2020-, H3C

@Contact :   xu.qiang@h3c.com

@Software:   f8s

@File    :   config.py

@Time    :   20200211

@Desc    :

'''

#k8s cfg
K8S_CFG = "/root/f8s/kubeconfig.yaml"

FISCO_HOME = '/root/fisco_network'

NFS = "10.114.134.46"

NET="fisco"

PEER_YAML = "{home}/deploy/{orgname}/peer.yaml"
SVC_YAML = "{home}/deploy/{orgname}/svc.yaml"
PV_YAML = "{home}/deploy/{orgname}/pv.yaml"
PVC_YAML = "{home}/deploy/{orgname}/pvc.yaml"
NAMESPACE_YAML = "{home}/deploy/namespace.yaml{orgname}"

RPC=20000
CHANNEL=20200
FRONT=30000


