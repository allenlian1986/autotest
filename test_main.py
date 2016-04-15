#!/usr/bin/python
# -*-coding=utf-8
'''
@author: allen
@date:20160107
@desc: the main module for autotest
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import unittest
import time
import os
import io
import random
import HTMLTestRunner
import threading
import time
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import urllib2
from SogouUtils import SogouUtils
from PicTestCase import Pic_Result_Test
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import zipfile

config = {}
words = []
time_stamp = time.strftime("%Y-%m-%d-%H-%M-%S")

#修改点1：这里的Pic_Result_Test根据自己case的类名设置
class Result_Test_FF(Pic_Result_Test): 
    def setUp(self):
        self.driver = webdriver.Firefox()
        #self.driver = webdriver.Remote(command_executor="http://"+config['hub_addr']+"/wd/hub",
        #desired_capabilities={"browserName":"firefox",
        #"platform":"WINDOWS",})
        self.bro_type = 'ff'
        self.base_url = "http://" + config["url"]
        self.cap_dir = 'capture-ff-' + time_stamp



#修改点2：这里的Pic_Result_Test根据自己case的类名设置
class Result_Test_IE(Pic_Result_Test):
    def setUp(self):
        '''
        iedriver = config['iedriver'].strip()
        os.environ["webdriver.ie.driver"] = iedriver
        self.driver = webdriver.Ie(iedriver)
        '''
        DesiredCapabilities.INTERNETEXPLORER['ignoreProtectedModeSettings'] = True
        self.driver = webdriver.Remote(command_executor="http://"+config['hub_addr']+"/wd/hub",
                                       desired_capabilities={"browserName":"internet explorer",
                                                             "platform":"WINDOWS",})
        self.base_url = "http://" + config["url"]
        self.bro_type = 'ie'
        self.cap_dir = 'capture-ie-' + time_stamp

#修改点3：这里的Pic_Result_Test根据自己case的类名设置
class Result_Test_CH(Pic_Result_Test):
    def setUp(self):
        #chromedriver = config['chromedriver'].strip()
        #os.environ["webdriver.chrome.driver"] = chromedriver
        #self.driver = webdriver.Chrome(chromedriver)

        self.driver = webdriver.Remote(command_executor="http://"+config['hub_addr']+"/wd/hub",
                               desired_capabilities={"browserName":"chrome",
                                                     "platform":"WINDOWS",})
        self.base_url = "http://" + config["url"]
        self.bro_type = 'ch'
        self.cap_dir = 'capture-ch-' + time_stamp

def Pic_Result_Test_Handler(bro_type='ff'):
    suite = unittest.TestLoader().loadTestsFromTestCase(eval('Result_Test_' + bro_type.upper()))
    # 创建报告页
    report = config['resfile'] + time_stamp + '-' + bro_type + '.html'
    fp = open(report, 'w')
    # 启动runner
    runner = HTMLTestRunner.HTMLTestRunner(
                stream=fp,
                title=u'测试结果' + bro_type,
                description=u'测试报告.'
                )
    # runner = unittest.TextTestRunner()
    rc = runner.run(suite)
    print(rc)

def start_task():
    bro_dict = {'0':'0', '1':'ff', '2':'ch', '3':'ie'}
    bro_type = config['browser']


    # 3种浏览器都进行测试
    if bro_type == '0':
        os.mkdir(os.getcwd()+'capture-ff-' + time_stamp)
        os.mkdir(os.getcwd()+'capture-ch-' + time_stamp)
        os.mkdir(os.getcwd()+'capture-ie-' + time_stamp)
        time.sleep(5)

        Pic_Result_Test_Handler(bro_dict['1'])
        time.sleep(5)
        Pic_Result_Test_Handler(bro_dict['2'])
        time.sleep(5)
        Pic_Result_Test_Handler(bro_dict['3'])
        time.sleep(5)

        SogouUtils.zip_capture('capture-ff-' + time_stamp)
        SogouUtils.zip_capture('capture-ch-' + time_stamp)
        SogouUtils.zip_capture('capture-ie-' + time_stamp)
    else:
        os.mkdir('capture-' + bro_dict[bro_type] + '-' + time_stamp)
        Pic_Result_Test_Handler(bro_dict[bro_type])
        time.sleep(5)
        SogouUtils.zip_capture('capture-' + bro_dict[bro_type] + '-' + time_stamp)

    if config['sendmail'] == '1':
        SogouUtils.send_mail(bro_dict[bro_type], config, time_stamp)

    print u'执行完毕'
if __name__ == '__main__':
    # 修改点4：这里的配置文件根据自己的项目设置
    config = SogouUtils.load_config("test_pic.cfg")
    delay = config['delay']
    timer = threading.Timer(int(delay), start_task)
    timer.start()
