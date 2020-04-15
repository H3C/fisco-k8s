# fisco-k8s
Deploy FISCO through k8s
基于python的使用K8s部署Fisco网络工具
方便在k8s上快速部署fisco网络，用户可以根据实自己情况对项目进行修改配置；

1、环境配置
准备k8s（v1.15.0）环境，python3.5，nfs（作为持久化存储使用）

2、工具配置
2.1在fisco/tools/ 文件夹一下放置ipconf（网络配置文件，不要改名字），fisco-bcos（二进制工具），application.yml，build_chain.sh；
2.2在k8s文件夹下，放置k8s的config文件
2.3在node节点，导入 fiscoorg/front:2.0.0-rc2
2.4在代码部署的哪台主机，在该主机上安装nfs，作为节点的持久化存储使用；

3、启动网络
启动create_network.py
