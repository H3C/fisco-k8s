#!/usr/bin/env python

# -*- encoding: utf-8 -*-

'''
@Author  :   xuqiang

@License :   (C) Copyright 2020-, H3C

@Contact :   xu.qiang@h3c.com

@Software:   f8s

@File    :   fisco.py

@Time    :   20200211

@Desc    :

'''


import os
from os import path
from subprocess import call
from string import Template

from config.config import *
from k8s.k8s import K8s

class Fisco():
    def __init__(self,home,net_name):
        self.home=home
        self.net=net_name
        self.k8s=K8s()
        pass

    def create_network(self):

        peers = create_fisco_home(self.home)

        create_net_cfg(self.home)

        ns_yaml = create_k8s_yaml("ns", None, networkName=self.net)
        self.apply_k8s_resource(ns_yaml,"ns")

        port_index=0

        for peer in peers:
            peername = "peer"+peer.replace('.', '').lower()
            ip = ".".join(peer.split(".")[:-1])
            create_org_home(self.home,ip)
            pv_yaml = create_k8s_yaml("pv", peer,
                                      dataPV =peername+"pv",
                                      dataPath = "/fisco_network",
                                      nfsServer = NFS)
            self.apply_k8s_resource(pv_yaml, "pv")
            pvc_yaml = create_k8s_yaml("pvc", peer,
                                       networkName=self.net,
                                       dataPV=peername+"pv")
            self.apply_k8s_resource(pvc_yaml, "pvc")
            dep_yaml = create_k8s_yaml("peer", peer,
                                        podName=peername,
                                        networkName=self.net,
                                        conf="nodes/{}/node0".format(ip),
                                        frontlog="nodes/{}/log".format(ip),
                                        appconf="nodes/{}/application.yml".format(ip),
                                        dataPV=peername + "pv")
            self.apply_k8s_resource(dep_yaml, "dep")
            svc_yaml = create_k8s_yaml("svc", peer,
                                       podName=peername,
                                       networkName=self.net,
                                       clusterip=ip,
                                       rpc=RPC+port_index,
                                       channel=CHANNEL+port_index,
                                       front=FRONT+port_index)
            self.apply_k8s_resource(svc_yaml, "svc")
            port_index=port_index+1

        print("create ok!!")

    def apply_k8s_resource(self,file ,type):
        self.k8s.create(file, type, self.net)

def create_fisco_home(home):
    home = '{}'.format(home)
    deploy = '{}/deploy'.format(home)

    try:
        os.system('mkdir -p {}'.format(home))
        os.system('mkdir -p {}'.format(deploy))
        os.system('cp -rf  {} {}'.format((path.dirname(__file__)+"tools"), home))
    except:
        error_msg = 'fisco home create failed'
        raise error_msg
    try:
        peers = analy_ipconf(home)
        for peer in peers:
            deployorg = '{}/deploy/{}'.format(home,peer)
            os.system('mkdir -p {}'.format(deployorg))
    except:
        error_msg = 'fisco delpoyorg create failed'
        raise error_msg
    return peers

def create_net_cfg(home):
    os.chdir(home)
    try:
        call(["bash", "/root/fisco_network/tools/build_chain.sh", "-f /root/fisco_network/tools/ipconf -p 30300,20200,8545 -o nodes -e /root/fisco_network/tools/fisco-bcos -i"])
    except:
        error_msg = 'fisco home create failed'
        raise error_msg
    return

def create_org_home(home, ip):
    log_path='{}/nodes/{}/log'.format(home,ip)
    sdk_path = '{}/nodes/{}/sdk'.format(home, ip)
    node0_path = '{}/nodes/{}/node0'.format(home, ip)
    appconf_path = '{}/nodes/{}/'.format(home,ip)
    try:
        os.system('mkdir -p {}'.format(log_path))
        os.system('cp -rf  {} {}'.format(("{}/tools/application.yml".format(home)), appconf_path))
        os.system('cp -rf  {} {}'.format(sdk_path, node0_path))
    except:
        error_msg = 'org home create failed'
        raise error_msg

yaml_opterartor={
    "ns":[path.dirname(__file__)+"/deploysample/namespace.yaml", NAMESPACE_YAML],
    "peer":[path.dirname(__file__)+"/deploysample/peer.yaml", PEER_YAML],
    "svc":[path.dirname(__file__)+"/deploysample/svc.yaml", SVC_YAML],
    "pv":[path.dirname(__file__)+"/deploysample/pv.yaml", PV_YAML],
    "pvc":[path.dirname(__file__)+"/deploysample/pvc.yaml", PVC_YAML]
}

def create_k8s_yaml(type, orgname, **kw):
    src = yaml_opterartor.get(type)[0]
    dest = yaml_opterartor.get(type)[1].format(home=FISCO_HOME,orgname=orgname)
    t = Template(open(src, 'r').read())
    with open(dest, 'w') as f:
        f.write(t.substitute(**kw))
    return dest

def analy_ipconf(home):
    peers=[]
    with open((home+"/tools/ipconf"), "r+") as f:
        for line in  f.readlines():
            info = line.split(" ")
            ip = info[0][:-2]
            org = info[1]
            group = info[2]
            peers.append(".".join((ip,org)))
    return peers


if __name__ == '__main__':
    fisco=Fisco(FISCO_HOME,"fisco")
    fisco.create_network()
    pass
