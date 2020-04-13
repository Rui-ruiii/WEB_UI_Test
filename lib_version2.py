import random
import string
import logging,unittest
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support import expected_conditions as EC



class Parameter():
    """Parameter library"""

    name1_admin = "admin"
    name1_password = "123"
    name2_null = " "
    name2_password = "123"
    name3_random = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    name3_password = "123"

    url_ctpqa = "http://ctpqa.cidanash.com:8083"


class Utility_function(unittest.TestCase):

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # driver_Chrome_slient = webdriver.Chrome(chrome_options=chrome_options)
    # driver_Chrome_up = webdriver.Chrome()
    #
    # driver = driver_Chrome_up

    cf = configparser.ConfigParser()
    cf.read(".\config.ini")
    url = cf.get("Default", "url")
    username = cf.get("LoginData", "username")
    userpw = cf.get("LoginData", "userpw")
    # driver=webdriver.Edge()
    driver = cf.get("Default", "driver")
    if driver == 'edgebeta':
        driver = webdriver.EdgeBeta()
    elif driver == 'firefox':
        driver = webdriver.Firefox()
    elif driver == 'edge':
        driver = webdriver.Edge()
    elif driver == 'opera':
        driver = webdriver.Opera()
    else:
        driver = webdriver.Chrome()

    def loginconfig(self):

        driver = self.driver
        driver.get(self.url)
        sleep(0.5)
        alert = EC.alert_is_present()(driver)
        sleep(2)
        if alert:
            self.log('\n-- ！！--Warning-- A popup appears: %s ' % alert.text)
            alert.accept()
            # self.log(driver.current_url)
            sleep(5)
        else:
            sleep(5)
            pass
        return True

    def config(self):
        driver=self.driver
        self.assertTrue(self.loginconfig())
        sleep(2)
        driver.find_element_by_id("username").send_keys(self.username)
        sleep(1)
        driver.find_element_by_id("password").send_keys(self.userpw)
        driver.find_element_by_xpath('//div/p[4]/*').click()
        return True


    def log(self,message):
        # 创建info级别的记录器
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            logger.setLevel(logging.INFO)

        # console中输出日志信息
            handler_info = logging.StreamHandler()
            handler_info.setLevel(logging.INFO)

        # 将日志处理程序加入到记录器
            logger.addHandler(handler_info)
        logger.info(message)

        return logger

    def find_element(self,how, what,element_desc,page_name):

        try:
            self.driver.find_element(how, what)
            self.log('\nPASSED: \'%s\' is exist on %s' % (element_desc,page_name))
            return True
        except:
            self.log('\nFAILURE: \'%s\' isn\'t exist on %s!'% (element_desc,page_name))
            return False

    def click_element(self, how, button, element,button_desc,page_name):
        driver=self.driver
        try:
            assert self.find_element(how,button,button_desc,page_name)
            driver.find_element(how,button).click()
            sleep(3)
            assert driver.find_element(By.XPATH, element).is_displayed()
            self.log('\nPASSED: click %s button successed on %s!'%(button_desc,page_name))
            return True
        except:
            self.log('\nFailure: click %s button failed %s!'%(button_desc,page_name) )
            return False

    def switch_window(self,by, button, string, title):
        driver=self.driver
        before_handle = driver.current_window_handle
        self.log("before switch handle: %s" % before_handle)
        before_title = driver.title
        self.log("before switch title: %s" % before_title)
        # time.sleep(3)
        driver.find_element(by, button).click()
        all_handle = driver.window_handles
        self.log("All handles: %s" % all_handle)
        for i in all_handle:
            if i != before_handle:
                driver.switch_to.window(i)
                after_handle = driver.current_window_handle
                after_title = driver.title
                if after_title==title:
                    break
        self.log("After switch handle: %s" % after_handle)
        self.log("After switch title: %s" % after_title)
        try:
            assert after_title == title
            self.log('PASSED: Switch %s page successfully!' % string)
            return True
        except:
            self.log('Failure: Switch %s page is failed!' % string)
            return False

    def judge_equal(self,string1,string2,note1,pos1,pos2):
        if(string1==string2):
        #self.log('\'%s\' is equal in %s' % (note1,pos1))
            self.log('\nPASSED: \'%s\' is equal in %s and %s'%(note1,pos1,pos2))
            return True
        else:
            self.log('\nFAILURE: \'%s\' is different in %s and %s'%(note1,pos1,pos2))
            return False

    def checkequal_elements(self,last_build_1, statebar, string,last_build_2=None,):
        try:
            # assert
            self.assertIsNotNone(self.e_jobid_last, msg='The first job isn\'t exist in last 10 builds!')
            if self.driver.find_element_by_xpath(self.e_jobid_last) == '#1':
                if self.driver.find_element_by_xpath(self.e_last_build_state) == 'Building' or self.driver.find_element_by_xpath(self.e_last_build_state) == 'Waiting':
                    self.log('The first job is building on coverage_page!')
                else:
                    try:
                        self.assertTrue(self.find_element(self.driver, By.XPATH, last_build_1, 'last 10 builds '),msg='%s isn\'t exist in last 10 builds')
                        self.assertTrue(self.find_element(self.driver, By.XPATH, statebar, 'statebar '), msg='%s isn\'t exist in state bar')
                        lastbuild1 = self.driver.find_element(By.XPATH, last_build_1)
                        statebar1 = self.driver.find_element(By.XPATH, statebar)
                        assert self.judge_equal(lastbuild1.text,statebar1.text,string,'last 10 builds','state bar')
                        return True
                    except:
                        return False
            else:
                #self.driver.find_element_by_xpath(self.e_jobid_last).text == '#46'
                #self.log('sfsdf')
                try:
                    #self.log(self.driver.find_element_by_xpath(last_build_2).text)
                    if (self.driver.find_element_by_xpath(
                            self.e_last_build_state).text == 'BUILDING'
                            or self.driver.find_element_by_xpath(
                        self.e_last_build_state).text == 'WAITING'):
                        #self.log('ffff')
                        self.assertTrue(self.find_element(self.driver, By.XPATH, last_build_2,
                                                         '%s of the last job in last 10 builds' % string))

                        lastbuild1 = self.driver.find_element(By.XPATH, last_build_2)
                        #lastbuild1 = self.driver.find_element(By.XPATH, lastbuild2)
                    else:
                        #self.log('sssss')
                        self.assertTrue(self.find_element(self.driver, By.XPATH, last_build_1, '%s of the last job in last 10 builds'%string))
                        lastbuild1 = self.driver.find_element(By.XPATH, last_build_1)
                    self.assertTrue(self.find_element(self.driver, By.XPATH, statebar, '%s of the last job in state bar'%string))
                    self.log('last build %s is \'%s\' in last 10 builds' % (string, lastbuild1.text))
                    statebar1 = self.driver.find_element(By.XPATH, statebar)
                    self.log('statebar %s is \'%s\' in state bar' % (string, statebar1.text))
                    assert self.judge_equal(lastbuild1.text, statebar1.text, string, 'last 10 builds', 'state bar')
                    return True
                except:
                    return False
        except:
            return False






