#!/usr/bin/python
# -*-coding=utf-8
'''
@author: allen
@date:20160107
@desc: some utils for autotest
'''
import urllib2
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

import smtplib  
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import os
import zipfile

class SogouUtils:
    '''
        加载配置文件
    '''
    @staticmethod
    def load_config(cfg_path):
        config = {}
        try:
            fp_conf = open(cfg_path)
            for i in fp_conf.readlines():
                if i.startswith("#"):
                    pass
                else:
                    argstr = i.split("#")[0]
                    arg_name = argstr.split("=")[0]
                    arg_val = argstr.split("=")[1]
                    config[arg_name] = arg_val
            
            for s in config:
                print s, config[s]
        except:
            print 'configure file load failed'
        return config

    '''
            压缩文件
    '''
    @staticmethod
    def zip_capture(path):    
        if os.path.exists(path):
            if len(os.listdir(path)) > 0:
                f = zipfile.ZipFile(path + ".zip", 'w', zipfile.ZIP_DEFLATED)
                for dirpath, dirnames, filenames in os.walk(path):
                    for filename in filenames:
                        print filename
                        f.write(os.path.join(dirpath, filename))
                f.close()
    '''
                发送邮件
    '''
    @staticmethod
    def send_mail(bro_type,config,time_stamp):
        msg = MIMEMultipart()
    
        # 构造附件
        if bro_type == '0':
            file_name_1 = config['resfile'] + time_stamp + '-1.html'
            if os.path.exists(file_name_1):
                att1 = MIMEText(open(file_name_1, 'rb').read(), 'base64', 'gb2312')
                att1["Content-Type"] = 'application/octet-stream'
                att1["Content-Disposition"] = 'attachment; filename=' + file_name_1  # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
                msg.attach(att1)
            
            cap_name_1 = 'capture-ff-' + time_stamp + '.zip'
            if os.path.exists(cap_name_1):
                cap1 = MIMEApplication(open(cap_name_1, 'rb').read())
                cap1.add_header('Content-Disposition', 'attachment', filename=cap_name_1)
                msg.attach(cap1)
            
            file_name_2 = config['resfile'] + time_stamp + '-2.html'
            if os.path.exists(file_name_2):
                att2 = MIMEText(open(file_name_2, 'rb').read(), 'base64', 'gb2312')
                att2["Content-Type"] = 'application/octet-stream'
                att2["Content-Disposition"] = 'attachment; filename=' + file_name_2  # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
                msg.attach(att2)
            
            cap_name_2 = 'capture-ch-' + time_stamp + '.zip'
            if os.path.exists(cap_name_2):
                cap2 = MIMEApplication(open(cap_name_2, 'rb').read())
                cap2.add_header('Content-Disposition', 'attachment', filename=cap_name_2)
                msg.attach(cap2)
            
            file_name_3 = config['resfile'] + time_stamp + '-3.html'
            if os.path.exists(file_name_3):
                att3 = MIMEText(open(file_name_3, 'rb').read(), 'base64', 'gb2312')
                att3["Content-Type"] = 'application/octet-stream'
                att3["Content-Disposition"] = 'attachment; filename=' + file_name_3  # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
                msg.attach(att3)   
            
            cap_name_3 = 'capture-ie-' + time_stamp + '.zip'
            if os.path.exists(cap_name_3):
                cap3 = MIMEApplication(open(cap_name_3, 'rb').read())
                cap3.add_header('Content-Disposition', 'attachment', filename=cap_name_3)
                msg.attach(cap3)
        else:
            file_name = config['resfile'] + time_stamp + '-' + bro_type + '.html'
            if os.path.exists(file_name):
                att1 = MIMEText(open(file_name, 'rb').read(), 'base64', 'gb2312')
                att1["Content-Type"] = 'application/octet-stream'
                att1["Content-Disposition"] = 'attachment; filename=' + file_name  # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
                msg.attach(att1)
            
            cap_name_1 = 'capture-' + bro_type + '-' + time_stamp + '.zip'
            if os.path.exists(cap_name_1):
                cap1 = MIMEApplication(open(cap_name_1, 'rb').read())
                cap1.add_header('Content-Disposition', 'attachment', filename=cap_name_1)
                msg.attach(cap1)
    
        # 加邮件头
        # msg['to'] = 'lianying@sogou-inc.com'
        def _construct_p():
            return chr(115)+chr(104)+chr(111)+chr(119)+chr(109)+chr(101)+chr(53)+chr(53)+chr(46)

        
        msg['to'] = config['sendto']
        msg['from'] = 'lianying@sogou-inc.com'
        msg['subject'] = u'测试结果' + time_stamp
        # 发送邮件
        try:
            server = smtplib.SMTP()
            server.connect('mail.sogou-inc.com')
            something = _construct_p()
            server.login('lianying', something)  # XXX为用户名，XXXXX为密码
            server.sendmail(msg['from'], msg['to'], msg.as_string())
            server.quit()
            print u'邮件发送成功'
        except Exception, e:  
            print str(e)

            
    '''
            检查是否为死链
    '''
    @staticmethod
    def check_link(link_url):
        resp = urllib2.urlopen(link_url)
        #print resp.getcode()
        if re.match(r'[45][0-9]{2}',str(resp.getcode())):
            return False
        return True
    
        
    '''
            检查是否为汉字
    '''
    @staticmethod
    def is_chinese(uchar):
        """判断一个unicode是否是汉字"""
        ss = re.match(u"[\xb7\u2460-\u27FF\u2780-\u2789\u2010-\u2026\u2160-\u217F\u3400-\u4DB5\u4E00-\u9FA5\u9FA6-\u9FBB\uF900-\uFA2D\uFA30-\uFA6A\uFA70-\uFAD9\uFF00-\uFFEF\u3000-\u303F]+",uchar)
        if ss:
            return True
        else:
            return False
        '''
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
                return True
        else:
                return False
        '''
       
    '''
            检查是否为数字
    '''
    @staticmethod
    def is_number(uchar):
        """判断一个unicode是否是数字"""
        if uchar >= u'\u0030' and uchar<=u'\u0039':
            return True
        else:
            return False
        
    '''
            检查是否为英文字母
    '''
    @staticmethod
    def is_alphabet(uchar):
        """判断一个unicode是否是英文字母"""
        if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
            return True
        else:
            return False
        
    '''
            检查是否为asc编码
    '''
    @staticmethod
    def is_asc(uchar):
        if uchar>=u'\u0000' and uchar<=u'\u007f':
            return True
        else:
            return False
    
    
    '''
            检查是否为判断是否非汉字，数字和英文字符的乱码
    '''
    @staticmethod
    def is_other(uchar):
        """"""
        if not (SogouUtils.is_chinese(uchar) or SogouUtils.is_number(uchar) or SogouUtils.is_alphabet(uchar) or SogouUtils.is_asc(uchar)):
            return True
        else:
            return False
        
    """半角转全角"""    
    @staticmethod
    def B2Q(uchar):
        inside_code=ord(uchar)
        if inside_code<0x0020 or inside_code>0x7e:      #不是半角字符就返回原来的字符
            return uchar
        if inside_code==0x0020: #除了空格其他的全角半角的公式为:半角=全角-0xfee0
            inside_code=0x3000
        else:
            inside_code+=0xfee0
        return unichr(inside_code)
    
    
    """全角转半角"""
    @staticmethod
    def Q2B(uchar):
        inside_code=ord(uchar)
        if inside_code==0x3000:
            inside_code=0x0020
        else:
            inside_code-=0xfee0
        if inside_code<0x0020 or inside_code>0x7e:      #转完之后不是半角字符返回原来的字符
            return uchar
        return unichr(inside_code)
    
    """把字符串全角转半角"""
    @staticmethod
    def stringQ2B(ustring):
        return "".join([SogouUtils.Q2B(uchar) for uchar in ustring])
    
    
    """格式化字符串，完成全角转半角，大写转小写的工作"""
    @staticmethod
    def uniform(ustring):
        return SogouUtils.stringQ2B(ustring).lower()
    
    
    """将ustring按照中文，字母，数字分开"""
    @staticmethod
    def string2List(ustring):
        retList=[]
        utmp=[]
        for uchar in ustring:
            if SogouUtils.is_other(uchar):
                if len(utmp)==0:
                    continue
                else:
                    retList.append("".join(utmp))
                    utmp=[]
            else:
                utmp.append(uchar)
        if len(utmp)!=0:
            retList.append("".join(utmp))
        return retList
    
    @staticmethod
    def check_element_exist(driver, by, str):
        try:
            el = driver.find_element(by, str)
        except :
            return False
        return True
    
    @staticmethod    
    def check_elements_exist(driver, by, str):
        try:
            els = driver.find_elements(by, str)
            if not els:
                return True
            else:
                return False
        except:
            return False
        
