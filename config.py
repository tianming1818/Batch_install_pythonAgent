#!/usr/bin/env python
# coding:utf-8
__author__ = 'TianM'
'''
配置环境：
license_key
private_host：私有化主机
private_host：私有化端口
host字典为需要安装的主机：key为主机名，value是列表，分别是主机IP，ssh端口，用户，密码，探针版本号，启动应用的命令，停止应用的命令
'''
license_key = "666-666-666"
private_host = "10.212.4.50"
private_port = 8081

host = {
    'my_virtual1':['192.168.159.128',22,'root','123456','1.3.2',"start app cmd &","stop app cmd"],
    'my_virtual2':['192.168.159.129',22,'root','123456','1.3.2',"start app cmd &","stop app cmd"],
}

