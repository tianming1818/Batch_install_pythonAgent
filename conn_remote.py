#!/usr/bin/env python
# coding:utf-8
__author__ = 'TianM'
'''
批量安装python探针脚本, version: 1.0
'''

import os
import time
import paramiko
from config import private_host,private_port


class login_ssh:
    '''
    使用paramiko模块连接ssh,实现批量安装探针，探针放在agent_dir目录下，版本号与config配置文件中一致
    '''
    def __init__(self,hostname,port,username,password,agent_ver,startapp,stopapp):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.agent_ver = agent_ver
        self.agent_name = 'tingyun-agent-python-%s.tar.gz' % agent_ver
        self.startapp = startapp
        self.stopapp = stopapp


    def init_ssh(self):
        '''
        初始化ssh连接
        '''
        self.myssh = paramiko.SSHClient()
        self.myssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.myssh.connect(hostname=self.hostname,port=self.port,username=self.username,password=self.password)

    def upload_agent(self):
        '''
        上传探针文件
        '''
        try:
            basedir = os.path.dirname(os.path.abspath(__file__))
            t=paramiko.Transport(self.hostname,self.port)
            t.connect(username=self.username,password=self.password)
            self.sftp = paramiko.SFTPClient.from_transport(t)
            local_dir = basedir + '\\agent_dir'
            self.sftp.put(os.path.join(local_dir,self.agent_name),os.path.join("/tmp/",self.agent_name))
            t.close()
        except Exception,err:
            print "connect error!",err

    def exec_cmd(self,cmd):
        '''
        执行指定的命令
        '''
        stdin, stdout, stderr = self.myssh.exec_command(cmd)
        rights = stdout.read()
        error = stderr.read()
        result = rights if rights else error
        return result

    def install_agent(self,licensekey):
        '''
        安装探针初始化
        '''
        #解压缩
        self.exec_cmd("cd /tmp/;tar -xzf %s -C /tmp/" % self.agent_name)
        #安装agent
        info = "Finished processing dependencies for tingyun-agent-python"
        inst = self.exec_cmd("python /tmp/tingyun-agent-python-%s/setup.py install" % self.agent_ver)
        if info in inst:
            print "Agent install success"
        else:
            print "Agent install Failed, info: ",inst
            exit()
        #探针初始化
        init = self.exec_cmd("tingyun-admin generate-config %s /tmp/tingyun.ini" % licensekey)
        init_info = "You use license key:"
        if init_info in init:
            print "Agent init success, %s" % init
        else:
            print "Agent init failed, %s" % init
            exit()
        #添加环境变量
        resu_info = self.exec_cmd("export TING_YUN_CONFIG_FILE=/tmp/tingyun.ini;tingyun-admin check-config")
        conf_info = "Validate agent config file success"
        if conf_info in resu_info:
            print "Agent check config success"
        else:
            print "Agent check config Failed",resu_info
            exit()
    def modify_conf(self,hostname):
        '''
        修改探针配置文件
        '''
        self.exec_cmd("sed -i 's/app_name = Python App/app_name = %s/g' /tmp/tingyun.ini" % hostname)
        self.exec_cmd("sed -i 's/ssl = True/ssl = False/g' /tmp/tingyun.ini")
        self.exec_cmd("echo '[tingyun:private]' >> /tmp/tingyun.ini")
        self.exec_cmd("echo 'host = %s' >> /tmp/tingyun.ini" % private_host)
        self.exec_cmd("echo 'port = %s' >> /tmp/tingyun.ini" % private_port)

    def start_app(self):
        '''
        加载探针启动应用
        '''
        time.sleep(2)
        startcmd = "nohup tingyun-admin run-program %s" % self.startapp
        self.myssh.exec_command(startcmd)

    def stop_app(self):
        '''
        停止应用
        '''
        self.myssh.exec_command(self.stopapp)
        time.sleep(2)


    def uninstall_agent(self):
        '''
        卸载探针后重新启动应用
        '''
        self.myssh.exec_command("find / -path '/tmp' -prune -o -name tingyun-admin -exec rm -f {} \;")
        self.myssh.exec_command("export -n TING_YUN_CONFIG_FILE")
        #启动应用
        time.sleep(2)
        self.myssh.exec_command(self.startapp)





