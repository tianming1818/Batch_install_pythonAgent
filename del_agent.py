#!/usr/bin/env python
# coding:utf-8
__author__ = 'TianM'
'''
卸载探针
'''

from conn_remote import login_ssh
from config import host


for x,y in host.items():
    print "uninstall agent for :",x
    conn = login_ssh(y[0],y[1],y[2],y[3],y[4],y[5],y[6])
    conn.init_ssh()
    conn.stop_app()
    conn.uninstall_agent()
