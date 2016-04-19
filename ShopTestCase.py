#!/usr/bin/python
# -*-coding=utf-8

'''
@author: allen
@date:20160107
@desc: the testcase module for autotest
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import unittest
from SogouUtils import SogouUtils
import time
import random
import math
from selenium.webdriver.common import keys
from selenium.webdriver.support.select import Select
from _mysql import result


class Shop_Result_Test(unittest.TestCase):
    words = []
    
    def __init__(self, methodName='runTest'):
        def isParameterizedMethod(attrname):
            return attrname.startswith("parameterized") and \
                hasattr(getattr(self, attrname), '__call__')

        testFnNames = filter(isParameterizedMethod, dir(self))
        for func in testFnNames:
            name = func.split("_", 1)[1]
            collect = "collection_test_search"
            if hasattr(getattr(self, collect), '__call__'):
                collectFunc = getattr(self, collect)
                array = collectFunc()
                for index in xrange(len(array)):
                    test = "%s_%d" % (name, index)
                    setattr(self.__class__, test, getattr(self, func)(array[index]))

        # print dir(self)
        # must called at last
        unittest.TestCase.__init__(self, methodName) 
   
    def setUp(self):
        unittest.TestCase.setUp(self)


    @classmethod
    def collection_test_search(cls):
        words = []
        config = SogouUtils.load_config("test_shop.cfg")
        # file = open("new_sogou_cate.txt")
        file = open(config['casefile'])
        for i in file.readlines():
            words.append(i)  
        return words
    def parameterized_test_search(self, x):
        #generate test body
        def test_body(self):
            self.driver.maximize_window()    
            self.driver.implicitly_wait(5)
            self.base_url = "http://" + config["url"]

            # start search word
            self.driver.get(self.base_url)         
            elem = self.driver.find_element_by_id("query")
            stb = self.driver.find_element_by_id('stb')
            elem.send_keys(x.decode('utf-8').strip('\n'))
            stb.click()            
            time.sleep(1)
        return test_body
    
    def tearDown(self):
        self.driver.quit()
        unittest.TestCase.tearDown(self)


    
            
class Loader(unittest.TestLoader):
    def getTestCaseNames(self, testCaseClass):
        """Return a sorted sequence of method names found within testCaseClass
        """
        testFnNames = unittest.TestLoader.getTestCaseNames(self, testCaseClass)

        def isParameterizedMethod(attrname, testCaseClass=testCaseClass,
                         prefix="parameterized"):
            return attrname.startswith(prefix) and \
                hasattr(getattr(testCaseClass, attrname), '__call__')

        testFnNames0 = filter(isParameterizedMethod, dir(testCaseClass))
        for func in testFnNames0:
            name = func.split("_", 1)[1]
            collect = "collection_test_search" 
            if hasattr(getattr(testCaseClass, collect), '__call__'):
                collectFunc = getattr(testCaseClass, collect)
                words = collectFunc()
                for item in xrange(len(words)):
                    testFnNames.append("%s_%d" % (name, item))

        # if self.sortTestMethodsUsing:
            # testFnNames.sort(key=_CmpToKey(self.sortTestMethodsUsing))
        return testFnNames
    
    def loadTestsFromTestCase(self, testCaseClass, browser=0):
        return unittest.TestLoader.loadTestsFromTestCase(self, testCaseClass)
