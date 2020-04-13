#-*- coding: utf-8 -*-
import unittest
import sys
import lib_version2
import test_login_passed_v2
import re
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep

uti = lib_version2.Utility_function()

class Mainpage(unittest.TestCase):
    """Check home-page"""

    @classmethod
    def setUpClass(cls):
        uti.loginconfig()
        sleep(1)
        test_login_passed_v2.Login().fun_login(test_login_passed_v2.Parameter.name1_admin,test_login_passed_v2.Parameter.name1_password)

    @classmethod
    def tearDownClass(cls):
        uti.driver.quit()

    def test_account(self):
        """Test if the account information is correct"""
        sleep(1)
        uti.find_element(By.ID, "UserMe", "UserName", "mainpage")
        RealName = uti.username
        sleep(0.5)
        PageDisplayName = uti.driver.find_element_by_id('UserMe').text
        Account_status = uti.judge_equal(RealName,PageDisplayName,"Account name","LoginPage","MainPage")
        uti.log(
            "\n---------------------------------The case: %s status now is END " % sys._getframe().f_code.co_name)
        self.assertTrue(Account_status)

    def test_account_logout(self):
        click_logout = uti.click_element(By.CLASS_NAME, "logout", "//*[@id='test1']", "Log out", "MainPage")
        self.assertTrue(click_logout)
        uti.driver.back()
        uti.log(
            "\n---------------------------------The case: %s status now is END " % sys._getframe().f_code.co_name)

    def test_alltest_button(self):
        uti.driver.find_element(By.CSS_SELECTOR,"#tab-0 > span").is_displayed()
        RealName = "ALL TEST"
        sleep(0.5)
        PageDisplaybutton = uti.driver.find_element_by_css_selector("#tab-0 > span").text
        uti.judge_equal(RealName, PageDisplaybutton, "button", "ALL TEST", "MainPage")
        uti.log(
            "\n---------------------------------The case: %s status now is END " % sys._getframe().f_code.co_name)
        self.assertTrue(uti.driver.find_element(By.CSS_SELECTOR,"#tab-0 > span").is_displayed())

    def test_footer(self):
        dividing_line_status = uti.driver.find_element(By.CLASS_NAME,"hr").is_displayed()
        if dividing_line_status:
            uti.log("\nPASSED: Dividing line dispaly normally")
        else:
            uti.log("\nFAILURE: Dividing line dispaly abnormal")
        self.assertTrue(uti.driver.find_element(By.CLASS_NAME,"hr").is_displayed())
        footer_status = uti.driver.find_element(By.CLASS_NAME, "logo").is_displayed()
        if footer_status:
            uti.log("\nPASSED: Footer dispaly normally")
        else:
            uti.log("\nFAILURE: Footer line dispaly abnormal")
        self.assertTrue(uti.driver.find_element(By.CLASS_NAME, "logo").is_displayed())
        uti.log(
            "\n---------------------------------The case: %s status now is END " % sys._getframe().f_code.co_name)

    def test_click_Cidana_jpg(self):
        """Test click on the cidana icon in the title bar and it should have the correct response"""

        cidana_jpg = uti.driver.find_element(By.ID,"titleBackHomePage").is_displayed()
        if cidana_jpg is True:
            mainpage_window = uti.driver.current_url
            uti.driver.find_element_by_id("titleBackHomePage").click()
            page_url_now = uti.driver.current_url
            sleep(1)
            uti.log("\nPASSED: Click on the title image to return to the address： %s"%page_url_now)
            uti.config()
            sleep(1)
        else:
            uti.log("\nFAILURE: The cidana picture in the title is abnormal")

        self.assertTrue(cidana_jpg)
        uti.log(
            "\n---------------------------------The case: %s status now is END " % sys._getframe().f_code.co_name)

    def test_mainpage_title(self):
        title_testframework = uti.find_element(By.CLASS_NAME,"testframework","PageTitle","Mainpage")
        self.assertTrue(title_testframework)
        uti.log(
            "\n---------------------------------The case: %s status now is END " % sys._getframe().f_code.co_name)

    def test_job_page_redirect(self):
        """Test if the go button of each job can jump to the destination URL"""

        #先取到mainpage里的jobname
        Job_mainpage = []
        jobsname_mainpage = uti.driver.find_elements_by_class_name('jobname')
        for j in jobsname_mainpage:
            Job_mainpage.append(j.text)

        Num_Job_mainpage = len(Job_mainpage)

        #从跳转的网页获取信息，test名称，对应的url
        JobUrl = []
        Original_title = []
        Jobtitle = []
        MainWindow = uti.driver.current_window_handle
        jobsgoelement = uti.driver.find_elements_by_class_name('btn-success1')
        for goelement in jobsgoelement:
            sleep(1)
            goelement.click()
            sleep(1)
            uti.driver.switch_to.window(MainWindow)
        for handle in uti.driver.window_handles:
            uti.driver.switch_to.window(handle)
            Original_title.append(uti.driver.title)
            JobUrl.append(uti.driver.current_url)
        uti.driver.switch_to.window(MainWindow)

        for ele in Original_title:
            jobtitle = ele.split(" -")[0].replace(" ","_").upper()
            if '' == ele:
                jobtitle = "xxx"
            Jobtitle.append(jobtitle)

        #除去mainpage的标题和url
        Jobtitle.remove("TEST_FRAMEWORK")
        JobUrl.remove("http://ctpqa.cidanash.com:8083/")
        Num_Jobttitle = len(Jobtitle)
        Authority_of_ThisAccount = dict(zip(Job_mainpage,JobUrl))

        Total_Authority = {"xxx（title）": 'xxx（url）',
                           "xxx（title）": 'xxx（url）',
                           "xxx（title）": 'xxx（url）',
                           "xxx（title）": 'xxx（url）'}

        for job in Job_mainpage:
            if job in Jobtitle:
                uti.log("PASSED: Jump to %s successfully,URL is %s" % (job, Authority_of_ThisAccount[job]))
                if Authority_of_ThisAccount[job] == Total_Authority[job]:
                    uti.log("PASSED: The URL of the current jump is consistent with the URL of the target job")
                else:
                    uti.log("Failure: The URL of the current jump is not consistent with the URL of the target job")
                self.assertEqual(Authority_of_ThisAccount[job], Total_Authority[job])
            else:
                uti.log("Failure: Jump to %s page faild" % job)
        # mainpage的Job数应与跳转的Job数相等（除去mainpage本身）
        self.assertEqual(Num_Job_mainpage, Num_Jobttitle)
        print("\n")
        uti.log(
            "\n---------------------------------The case: %s status now is END " % sys._getframe().f_code.co_name)

    def test_job_state(self):

        num_mean ={"0":"UNKNOWN","1":"???FAILED","2":"BUILDING","3":"COMPLETED","4":"???CANCEL"}

        #Information preprocessing
        page_source = uti.driver.page_source
        jobs_info_total = re.findall('>\[.+',page_source)
        # job_info_total里的每一个列表元素都是一个job的全部信息
        job_info_total = re.findall('.+?\}',str(jobs_info_total))
        print(job_info_total)

        Jobcards = uti.driver.find_elements_by_class_name("main-card")
        self.assertEqual(len(Jobcards),len(job_info_total))
        j = True

        for job_card in Jobcards:

            ignore_card = job_card.find_element_by_class_name("jobname").text
            if "AWCYTESTDEMO" in str(ignore_card).upper():
                pass
            else:
                #job名称的校验
                try:
                    jobname = job_card.find_element_by_class_name("jobname").text
                    if str(jobname).lower() in str(jobs_info_total).lower():
                        uti.log("PASSED: %s in view permissions"%jobname)
                    else:
                        uti.log("FAILURE : %s isn't in view permissions"%jobname)
                    self.assertIn(jobname,str(jobs_info_total).upper(),msg="%s isn't in view permissions"%jobname)
                    print("--",jobname,"--")
                except NoSuchElementException as error:
                    uti.log("FAILURE : %s :No element with class name 'jobname' was obtained  or  no items with current view permissions were detected"%error)
                    j = False

                #job commit的校验
                try:
                    # commit_with_symbol = job_card.find_element_by_id("commit-id1-1").text
                    # commit = str(commit_with_symbol).replace("commit : ","")
                    commit = str(job_card.find_element_by_id("commit-id1-1").text).replace("COMMIT : ","")
                    print(commit)
                    for real_job in job_info_total:
                        if str(jobname).lower() in str(real_job).lower():
                            real_commit = re.findall('Commit.+?\,',real_job)
                            if commit.lower() in str(real_commit).lower():
                                uti.log("PASSED: %s  commit : %s verify PASS"%(jobname,commit))
                            else:
                                uti.log("FAILURE: %s  commit : %s verify FAIL"%(jobname,commit))
                            self.assertIn(str(commit).lower(),str(real_commit).lower())
                            print("-- commit: ",commit)
                except NoSuchElementException as error:
                    uti.log("%s : In %s, An exception occurred in the commit (lookup method: id: 'commit-id 1-1'); the commit of the current project was not checked"%(error,jobname.text))
                    j = False

                #jobstatus的校验
                try:
                    status = job_card.find_element_by_class_name("badge-warning").text
                    for real_job in job_info_total:
                        if str(jobname).lower() in str(real_job).lower():
                            real_status_str = re.findall('Status.+?\,', real_job)
                            real_status_number = re.sub("\D","",str(real_status_str))
                            real_status = num_mean[real_status_number]
                            if status.lower() in real_status.lower():
                                uti.log("PASSED: %s  status : %s verify PASS"%(jobname,status))
                            else:
                                uti.log("FAILURE: %s  status : %s verify FAIL"%(jobname,status))
                            self.assertIn(str(status).lower(),str(real_status).lower())
                            print("-- status: ",status)
                    print(jobname, " Status is： ", str(status))
                except NoSuchElementException as error:
                    uti.log("%s : In %s,  Status exception (lookup: classname: 'badge-warning'); status of current item was not checked"%(error,jobname.text))
                    j = False

                try:
                    TotalBuildInfo = job_card.find_element_by_class_name("build_statistic")
                    TotalBuildInfo_text = TotalBuildInfo.text.replace("\n", " ")
                    for real_job in job_info_total:
                        if str(jobname).lower() in str(real_job).lower():
                            real_totalinfo_str = re.findall('total.+?\}', real_job)
                            real_totalinfo_number = re.sub("\D","",str(real_totalinfo_str))
                            page_totalinfo_number = re.sub("\D","",str(TotalBuildInfo_text))
                            if real_totalinfo_number == page_totalinfo_number:
                                uti.log("PASSED: %s  totalinfo : %s verify PASS" % (jobname, TotalBuildInfo_text))
                            else:
                                uti.log("FAILURE: %s  totalinfo : %s verify FAIL" % (jobname, TotalBuildInfo_text))
                            self.assertEqual(real_totalinfo_number,page_totalinfo_number)
                            print("-- totalinfo: ",TotalBuildInfo_text)
                except NoSuchElementException as error:
                    uti.log("%s : In %s, Total BuildInfo exception (Find by: classname: 'build statistic'); TotalBuildInfo for the current project was not detected "%(error,jobname.text))
                    j = False


                print("\n")
        self.assertTrue(j)

if __name__ == '__main__':
    unittest.main()




