#-*- coding: utf-8 -*-
import unittest
import sys
from time import sleep
from selenium.webdriver.common.by import By
import random
import string
import lib_version2
import configparser
uti = lib_version2.Utility_function()

class Parameter():
    """Parameter library"""

    name1_admin = "admin"
    name1_password = "123"
    name2_null = " "
    name2_password = "123"
    name3_random = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    name3_password = "123"

    url_ctpqa = ""

class Login(unittest.TestCase):
    """test cases of login"""
    @classmethod
    def setUpClass(cls):
        uti.loginconfig()
    @classmethod
    def tearDownClass(cls):
        uti.driver.quit()

    def fun_login(self, username, password):
        driver = uti.driver
        sleep(0.5)
        clicklogin = driver.find_element_by_xpath('//div/p[4]/*')
        clicklogin.click()
        sleep(0.5)
        nameelement = driver.find_element_by_id('username')
        nameelement.clear()
        nameelement.send_keys(username)
        sleep(0.5)
        passwordelement = driver.find_element_by_id('password')
        passwordelement.clear()
        passwordelement.send_keys(password)
        clicklogin.click()

    def test_login_sucessful(self):
        self.fun_login(uti.cf.get("LoginData", "username"),uti.cf.get("LoginData", "userpw"))
        sleep(1)
        result_status = uti.find_element(By.CLASS_NAME, "logout", "logout", "mainpage")
        assert result_status
        uti.log("\n================== The case: %s status now is END =================== " % sys._getframe().f_code.co_name)

    def test_login_nullname(self):
        self.fun_login(uti.cf.get("LoginData", "usernamenull"),uti.cf.get("LoginData", "userpw"))
        sleep(1)
        result_status = uti.find_element(By.XPATH, "//*[@id='username'][@required='required']", "please fill in this field", "loginpage")
        result_status_display = uti.driver.find_element(By.XPATH,"//*[@id='username'][@required='required']").is_displayed()
        assert result_status
        assert result_status_display
        uti.log("\n================== The case: %s status now is END =================== " % sys._getframe().f_code.co_name)

    def test_login_errorname(self):
        self.fun_login(uti.cf.get("LoginData", "usernamewrong"),uti.cf.get("LoginData", "userpw"))
        sleep(1)
        result_status = uti.find_element(By.ID,"login_error","Error: Incorrect user name or password", "loginpage")
        result_status_dispaly = uti.driver.find_element(By.ID,"login_error").is_displayed()
        assert result_status
        assert result_status_dispaly
        uti.log("\n================== The case: %s status now is END =================== " % sys._getframe().f_code.co_name)


if __name__ == '__main__':
    unittest.TestCase()




