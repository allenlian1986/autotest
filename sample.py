#!/usr/bin/python
# -*-coding=utf-8
from selenium.webdriver.support.ui import WebDriverWait
import pytest

def test_shop_result_001(selenium,word): 
    selenium.maximize_window()
    selenium.get('http://gouwu.sogou.com')            
    WebDriverWait(selenium, 30 ).until(lambda d:d.execute_script('return document.readyState') =='complete')             
    
    elem = selenium.find_element_by_id("upquery")
    elem.send_keys(word)
    elem.send_keys(Keys.ENTER)
    selenium.close()
if __name__ == '__main__':   
    pytest.main()
