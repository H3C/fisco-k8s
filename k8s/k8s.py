#!/usr/bin/env python

# -*- encoding: utf-8 -*-

'''
@Author  :   xuqiang

@License :   (C) Copyright 2020-, H3C

@Contact :   xu.qiang@h3c.com

@Software:   f8s

@File    :   k8s.py

@Time    :   20200211

@Desc    :

'''

from kubernetes import client, config
import yaml
from os import  path

from config.config import *

class K8s():

    def __init__(self,cfg=(path.dirname(__file__)+'/config')):
        config.kube_config.load_kube_config(cfg)
        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
        self.extend_v1 = client.ExtensionsV1beta1Api()
        self._create={
            "ns": self.create_namespace,
            "dep":self.create_deployment,
            "svc":self.create_service,
            "pv":self.create_pv,
            "pvc": self.create_pvc
        }
        self._delete={
            "ns": self.delete_namespace,
            "dep":self.delete_deployment,
            "svc":self.delete_service,
            "pv":self.delete_pv,
            "pvc": self.delete_pvc
        }

    def create(self,file,type,ns):
        try:
            self._create.get(type)(file=file,namespace=ns)
        except Exception as e:
            raise e

    def delete(self,name, ns):
        try:
            self._delete.get(type)(name=name,namespace=ns)
        except Exception as e:
            raise e

    def create_deployment(self,file,namespace="default"):
        with open(path.join(path.dirname(__file__), file)) as f:
            dep = yaml.safe_load(f)
            resp = self.extend_v1.create_namespaced_deployment(body=dep, namespace=namespace)
            return resp

    def delete_deployment(self, name, namespace="default"):
        api_response = self.extend_v1.delete_namespaced_deployment(name=name, namespace=namespace)
        return api_response

    def create_namespace(self, file, namespace="default"):
        with open(path.join(path.dirname(__file__), file)) as f:
            dep = yaml.safe_load(f)
            api_response = self.core_v1.create_namespace(body=dep)
            return api_response

    def delete_namespace(self, name, namespace="default"):
        api_response = self.core_v1.delete_namespace(name)
        return api_response

    def create_service(self, file, namespace="default"):
        with open(path.join(path.dirname(__file__), file)) as f:
            dep = yaml.safe_load(f)
            api_response = self.core_v1.create_namespaced_service(namespace, body=dep)
            return api_response

    def delete_service(self, name, namespace="default"):
        api_response = self.core_v1.delete_namespaced_service(name, namespace)
        return api_response

    def create_pv(self, file, namespace=None):
        with open(path.join(path.dirname(__file__), file)) as f:
            dep = yaml.safe_load(f)
            api_response = self.core_v1.create_persistent_volume(body=dep)
            return api_response

    def delete_pv(self, name, namespace="default"):
        api_response = self.core_v1.delete_persistent_volume(name)
        return api_response

    def create_pvc(self, file, namespace="default"):
        with open(path.join(path.dirname(__file__), file)) as f:
            dep = yaml.safe_load(f)
            api_response = self.core_v1.create_namespaced_persistent_volume_claim(namespace, body=dep)
            return api_response

    def delete_pvc(self, name, namespace="default"):
        api_response = self.core_v1.delete_namespaced_persistent_volume_claim(name, namespace)
        return api_response

if __name__ == '__main__':
    k8s=K8s()
    ret = k8s.core_v1.list_pod_for_all_namespaces()
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    pass