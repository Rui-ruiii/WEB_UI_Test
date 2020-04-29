import logging,requests,re
from time import sleep
import unittest,configparser
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Utility_function(unittest.TestCase):
    #读取配置文件
    cf = configparser.ConfigParser()
    cf.read(".\config.ini")
    # s=cf.items("Default")
    url = cf.get("Default", "url")
    username = cf.get("LoginData", "username")
    userpw = cf.get("LoginData", "userpw")
    #driver=webdriver.Edge()
    driver=cf.get("Default","driver")
    #browser={"chrome":'webdriver.ChromeOptions()'}
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # driver= webdriver.Chrome(chrome_options=chrome_options)
    if driver == 'edgebeta':
        driver = webdriver.EdgeBeta()
    elif driver == 'firefox':
        driver= webdriver.Firefox()
    elif driver == 'edge':
        driver = webdriver.Edge()
    elif driver == 'opera':
        driver = webdriver.Opera()
    else:
        driver=webdriver.Chrome()

    def loginconfig(self):
        sleep(3)
        driver = self.driver
        driver.get(self.url)
        sleep(0.5)
        alert = EC.alert_is_present()(driver)
        #self.log(alert)
        #sleep(2)
        if alert:
            self.log('\n-- ！！--Warning-- A popup appears: %s ' % alert.text)
            alert.accept()
            sleep(1)
        else:
            sleep(1)
            pass
        return True

    def config(self):
        e_logout_btn = "//a[@class='logout']"
        driver = self.driver
        self.assertTrue(self.loginconfig())
        #input username
        self.assertTrue(self.find_element(By.ID, 'username', 'username textbox', 'Login'),
                        msg='\nFAILURE: usernamebox isn\'t exist on login page!')
        self.driver.find_element_by_id("username").send_keys(self.username)
        # input password
        self.assertTrue(self.find_element(By.ID, 'password', 'password textbox', 'Login'),
                        msg='\nFAILURE: passwordbox isn\'t exist on login page!')
        self.driver.find_element_by_id("password").send_keys(self.userpw)
        #click login button
        assert self.click_element(By.XPATH, '//div/p[4]/*', e_logout_btn, 'login button', 'Login')
        self.log('\nPASSED: login success')
        return True

    def log(self,message):
        # 创建info级别的记录器
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            logger.setLevel(logging.INFO)

        # 创建日志处理程序，并将log命名为log.txt,logging.info表示log中打印信息的级别为info（只有级别高于info才会写进文档。）
        #     handler_info = logging.FileHandler('log.txt', 'w')
        #     handler_info.setLevel(logging.INFO)

        # console中输出日志信息
            handler_info = logging.StreamHandler()
            handler_info.setLevel(logging.INFO)

        # 日志格式
        #     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        #     handler_info.setFormatter(formatter)

        # 将日志处理程序加入到记录器
            logger.addHandler(handler_info)
        logger.info(message)
        #logger.handlers.clear()
        return logger

    def find_element(self,how, what,element_desc,page_name):
        try:
            assert self.driver.find_element(how, what)
            self.log('\nPASSED: \'%s\' is exist on %s Page' % (element_desc,page_name))
            return True
        except:
            # else:
            self.log('\nFAILURE: \'%s\' isn\'t exist on %s Page!'% (element_desc,page_name))
            return False

    def lastbuild_exist(self,pagename):
        try:
            #self.log('ss')
            e_jobid_last = "//tbody[@id='build_list']/tr[1]/td[1]/a/b"
            job_last=self.driver.find_elements_by_xpath(e_jobid_last)
            #self.log(len(job_last))
            #assert
            assert len(job_last)==1
            return True
            #self.log()
            # self.log('gg')
        except:
            #self.log('dddd')
            self.log('The first build isn\'t exist in last 10 builds on %s page!' % pagename)
            return False

    def js_top_down_btn(self,pagename):
        #TODO{LUCKY} DOING.....
        #sleep(10)
        # js='var fullLogContent = document.getElementById("test").scrollTop;' \
        #    'var hwJenkinsheight = document.getElementById("jenkins_full_log").scrollHeight;' \
        #    'alert(hwJenkinsheight)'
        # self.driver.execute_script(js)
        # sleep(10)
        # return 1
        assert self.lastbuild_exist(pagename)
        js1 = 'var fullLogContent = document.getElementById("test").scrollTop;return fullLogContent'
        scrollbar_height=self.driver.execute_script(js1)
        self.log('Scrollbar height of fulllog page is %s on %s page'%(scrollbar_height,pagename))
        sleep(3)
        js2 = 'var hwJenkinsLogWnd = document.getElementById("jenkins_full_log").scrollHeight;return hwJenkinsLogWnd '
        jenkinslog_height=self.driver.execute_script(js2)
        self.log('jenkinslog height of fulllog page is %s on %s page'%(jenkinslog_height,pagename))
        if scrollbar_height==0:
            return 1
        elif scrollbar_height==jenkinslog_height:
            return 2
        else:
            return 3

    def click_element(self, how, button, element, button_desc, page_name):
        # button is the item element,element is used to verify
        driver = self.driver
        try:
            assert self.find_element(how, button, button_desc, page_name)
            driver.find_element(how, button).click()
            self.driver.implicitly_wait(10)
            if button_desc=='full log top button' or button_desc=='full log down button':
                #TODO:{LUCKY}doing.....
                s=self.js_top_down_btn(page_name)
                self.log(self.driver.find_element_by_id('buildButton').text)
                #self.log(s)
                if button_desc == 'full log top button':
                    assert s==1
                elif button_desc == 'full log top button' or self.driver.find_element_by_id('buildButton').text=='BUILDING':
                    assert s==2
            else:
                self.driver.implicitly_wait(10)
                assert driver.find_element(By.XPATH, element).is_displayed()
            self.log('\nPASSED: click \'%s\' successed on %s page!' % (button_desc, page_name))
            return True
        except:
            self.log('\nFailure: click \'%s\' failed on %s page!' % (button_desc, page_name))
            return False

    def switch_window(self, by, button, string, title):
        try:
            driver = self.driver
            before_handle = driver.current_window_handle
            self.log("before switch handle: %s" % before_handle)
            before_title = driver.title
            self.log("before switch title: %s" % before_title)
            # time.sleep(3)
            driver.find_element(by, button).click()
            #self.click_element(by,button,)
            all_handle = driver.window_handles
            self.log("All handles: %s" % all_handle)
            for i in all_handle:
                if i != before_handle:
                    driver.switch_to.window(i)
                    after_handle = driver.current_window_handle
                    after_title = driver.title
                    if after_title == title:
                        break
            assert after_title==title
            self.log("After switch handle: %s" % after_handle)
            self.log("After switch title: %s" % after_title)
            self.log('\nPASSED: Switch %s page successfully!' % string)
            return True
        except:
            self.log('\nFAILURE: Switch %s page is failed!' % string)
            return False

    #judge order of jobid in last 10 builds
    def judge_jobid(self,pagename):
        assert self.lastbuild_exist(pagename)
        job_id_all = "//td[@class='text-center text-muted']/a/b"
        job_id_last = "//tbody[@id='build_list']/tr[1]/td[1]/a/b"
        jobids = self.driver.find_elements(By.XPATH, job_id_all)
        jobid_last = self.driver.find_element_by_xpath(job_id_last)
        #assert jobid_last.is_displayed()
        jobid_last = int(jobid_last.text.replace('#', ''))
        for jobid in jobids:
            jobid = int(jobid.text.replace('#', ''))
            if jobid == jobid_last:
                jobid_last = jobid_last - 1
            else:
                self.log('\nFAILURE:jobid (#%s) is wrong order on %s page' % (jobid, pagename))
                return False
        self.log('\nPASSED: job\'s order is right on %s page' % pagename)
        return True

    def judge_equal(self,string1,string2,note1,pos1,pos2):
        if(string1==string2):
            self.log('\nPASSED:\n \'%s\' is equal in %s and %s'%(note1,pos1,pos2))
            return True
        else:
            self.log('\nFAILURE:\n \'%s\' is different in %s and %s'%(note1,pos1,pos2))
            return False

    def checkequal_elements(self, last_build_1, statebar, string, last_jobid, page, last_build_2):
        assert self.lastbuild_exist(page)
        state = "//tbody[@id='build_list']/tr[1]/td[3]/div"
        try:
            if self.driver.find_element_by_xpath(last_jobid).text == '#1':
                # self.log('ssss')
                if self.driver.find_element_by_xpath(
                        state).text == 'BUILDING' or self.driver.find_element_by_xpath(
                    state).text == 'WAITING ...':
                    self.log('The first job is building on %s!' % page)
                else:
                    assert self.find_element(By.XPATH, last_build_1,
                                             '%s of the last job in last 10 builds' % string, page)
                    lastbuild1 = self.driver.find_element(By.XPATH, last_build_1)
            else:
                if (self.driver.find_element_by_xpath(
                        state).text == 'BUILDING'
                        or self.driver.find_element_by_xpath(
                            state).text == 'WAITING ...'):
                    # self.log('ffff')
                    assert self.find_element(By.XPATH, last_build_2,
                                             '%s of the last job in last 10 builds' % string, page)
                    lastbuild1 = self.driver.find_element(By.XPATH, last_build_2)
                else:
                    assert self.find_element(By.XPATH, last_build_1,
                                             '%s of the last job in last 10 builds' % string,
                                             page)
                    lastbuild1 = self.driver.find_element(By.XPATH, last_build_1)
            assert self.find_element(By.XPATH, statebar, '%s of the last job in state bar' % string, page)
            self.log('last build %s is \'%s\' on %s page' % (string, lastbuild1.text.strip(), page))
            statebar1 = self.driver.find_element(By.XPATH, statebar)
            self.log('statebar %s is \'%s\' on %s page' % (string, statebar1.text.strip(), page))
            assert self.judge_equal(lastbuild1.text.strip(), statebar1.text.strip(), string,'last 10 builds', 'state bar')
            return True
        except:
            return False

    #check report exist when status is completed.
    def checkexist_report(self,pagename):
        assert self.lastbuild_exist(pagename)
        jobid_all=self.driver.find_elements_by_xpath("//td[@class='text-center text-muted']/a/b")
        #self.log(jobid_all)
        state_all=self.driver.find_elements_by_xpath("//td[ @class ='text-center'][1]/div")
        report_all=self.driver.find_elements_by_xpath("//td[ @class ='text-center'][2]")
        i=0
        try:
            # self.log(len(jobid_all))
            for jobid in jobid_all:
                # self.log(jobid)
                # self.log(i)
                # self.log(state_all[i].text)
                # i=i+1
                #self.log(states_all[i].text)
                if state_all[i].text == 'COMPLETED':
                    # self.log('ttt')
                    if report_all[i].text == '':
                        self.log('\nFAILURE: The %s state is completed,but report isn\'t exist on %s page' % (
                        jobid.text, pagename))
                        return False
                else:
                    # self.log('ff')
                    if report_all[i].text != '':
                        self.log('\nFAILURE: The %s state is %s,but report is exist on %s page' % (
                        jobid.text, state_all[i].text, pagename))
                        return False
                i=i+1
            # self.log('dddd')
            self.log(
                 '\nPASSED: All exist state of job report is right on %s page' % pagename)
            return True
        except:
            return False

    def get_Ajax(self,base_url):
        """base_url is the request url,change it you could get last10builds,or statusbar,or any other ajax part you need"""

        try:
            cookielist = self.driver.get_cookies()
            for cookiedict in cookielist:
                if cookiedict['name'] == 'CiSession':
                    cookievalue = cookiedict['value']
                else:
                    pass
            cookie = "testcookie=yes;CiSession=" + cookievalue
            header = {
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
                'Cookie': cookie,
                        }

            response = requests.get(base_url,headers=header)
            Ajax_list = response.json()
            return Ajax_list

        except requests.ConnectionError as e:
            self.log("--ERROR--:",e.args)

    def judge_equal_3(self,parm1,parm2,parm3,desc):
        """Compare the three parameter values"""
        if (parm1 == parm2 == parm3):
            self.log('\nPASSED: \'%s\' is equal in %s , %s and %s '%(desc,parm1,parm2,parm3))
            return True
        else:
            self.log('\nFAILURE: \'%s\' is different in %s, %s and %s '%(desc,parm1,parm2,parm3))
            return False

    def judge_equal_4(self,parm1,parm2,parm3,parm4,desc):
        """Compare the four parameter values"""
        if (parm1 == parm2 == parm3 == parm4):
            self.log('\nPASSED: \'%s\' is equal in %s , %s ,%s and %s '%(desc,parm1,parm2,parm3,parm4))
            return True
        else:
            self.log('\nFAILURE: \'%s\' is different in %s , %s ,%s and %s '%(desc,parm1,parm2,parm3,parm4))
            return False

    def num_trans_status(self,Ajax_list):
        """Switch between numbers and states"""
        Ajax_list_status = []
        for One_Object in Ajax_list:
            if One_Object['Status'] == 0:
                Ajax_list_status.append("UNKNOWN")
            if One_Object['Status'] == 1:
                Ajax_list_status.append("WAITING")
            if One_Object['Status'] == 2:
                Ajax_list_status.append("BUILDING")
            if One_Object['Status'] == 3:
                Ajax_list_status.append("COMPLETED")
            if One_Object['Status'] == 4:
                Ajax_list_status.append("FAILED")
            if One_Object['Status'] == 5:
                Ajax_list_status.append("CANCELED")
        return Ajax_list_status

    def get_Page_10builds_info(self):
        """get 10builds info in page"""
        joblist_starttime = []
        joblist_duration = []
        joblist_by = []
        joblist_starttime_duration_by_row = self.driver.find_elements_by_class_name("opacity-7")
        for single in joblist_starttime_duration_by_row:
            starttime = re.findall("\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d", str(single.text))
            if len(starttime):
                joblist_starttime.append(starttime[0])
            duration_row = re.findall("Duration.+", str(single.text))
            if len(duration_row):
                duration = str(duration_row[0]).replace("Duration : ", "")
                joblist_duration.append(duration)
            operator = re.findall("By.+", str(single.text))
            if len(operator):
                joblist_by.append(str(operator[0]).replace("By : ", ""))

        joblist_commit = []
        joblist_commit_row = self.driver.find_elements_by_xpath('//*[@id="build_list"]//*[@class="widget-heading"]')
        for jobcommit in joblist_commit_row:
            joblist_commit.append(str(jobcommit.text).replace("Commit:", "").replace(" ", ""))

        joblist_message_row = self.driver.find_elements_by_class_name("widget-heading-m")
        joblist_message = []
        for job_message in joblist_message_row:
            joblist_message.append(job_message.text)

        global joblist_status
        joblist_status = []
        joblist_status_row = self.driver.find_elements_by_class_name("badge")
        for single_status_in_joblist in joblist_status_row:
            joblist_status.append(single_status_in_joblist.text)

        joblist_id = []
        joblist_id_row = self.driver.find_elements_by_xpath('//*[@id="build_list"]//td[1]/a')
        for id in joblist_id_row:
            joblist_id.append(id.text)

        return joblist_id, joblist_commit, joblist_message, joblist_starttime, joblist_duration, joblist_by, joblist_status

    def get_Ajax_10build_info(self,Ajax_list):
        """get 10builds info in ajax"""
        Ajax_starttime = []
        Ajax_duration = []
        Ajax_by = []
        Ajax_id = []
        Ajax_commit = []
        Ajax_message = []
        Ajax_status = []
        for One_Object in Ajax_list:
            Ajax_id.append("#"+ str(One_Object['JenkinsBuildNo']))
            Ajax_commit.append(One_Object['CommitID'])
            Ajax_message.append(str("Message:" + One_Object['CommitMsg']).replace("\n", "").replace("\r", ""))
            Ajax_status.append(One_Object['Status'])
            Ajax_starttime.append(One_Object['StartTime'])
            Ajax_duration.append(One_Object['Duration'])
            Ajax_by.append(One_Object['Operator'])

        return Ajax_id, Ajax_commit, Ajax_message, Ajax_starttime, Ajax_duration, Ajax_by, Ajax_status
