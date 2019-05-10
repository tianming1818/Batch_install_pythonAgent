#!/usr/bin/env python
# coding:utf-8
__author__ = 'TianM'
'''
安装探针
'''

from conn_remote import login_ssh
from config import host,license_key


for x,y in host.items():
    print "install agent for: ",x
    conn = login_ssh(y[0],y[1],y[2],y[3],y[4],y[5],y[6])
    conn.upload_agent()
    conn.init_ssh()
    conn.install_agent(license_key)
    conn.modify_conf(x)
    conn.stop_app()
    conn.start_app()