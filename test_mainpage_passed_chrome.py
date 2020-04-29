#-*- coding: utf-8 -*-
import unittest
import sys
import lib_version3
import re
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep

uti = lib_version3.Utility_function()

# def judge_first_deploy():
#     global first_deploy_return
#     Jobcards = uti.driver.find_elements_by_class_name("main-card")
#     i = 0
#     for job_card in Jobcards:
#         if job_card.find_element_by_class_name("badge-warning").text == "UNKNOWN":
#             pass
#         else:
#             i += 1
#     if i == 0:
#         first_deploy_return = False
#     else:
#         first_deploy_return = True

class function_for_mainpage():

    def re_findall(real_job):

        page_total_info_str = re.findall('total.+?\,', real_job)
        page_total_info_number = int(re.sub("\D", "", str(page_total_info_str)))
        page_passed_info_str = re.findall('finishs.+?\,', real_job)
        page_passed_info_number = int(re.sub("\D", "", str(page_passed_info_str)))
        page_fails_info_str = re.findall('fails.+?\,', real_job)
        page_fails_info_number = int(re.sub("\D", "", str(page_fails_info_str)))
        page_cancels_info_str = re.findall('cancels.+?\}', real_job)
        page_cancels_info_number = int(str(re.sub("\D", "", str(page_cancels_info_str))))
        sum_number = page_passed_info_number + page_fails_info_number + page_cancels_info_number
        return page_total_info_number,sum_number

    def totalinfo_compare_logprint(A,B,jobname,status):

        if A == B:
            uti.log(
                "PASSED: %s  total jobs number %s is equal with other sumnumber : %s (When status is %s)" % (
                    jobname, A, B, str(status)))
        else:
            uti.log(
                "FAILURE: %s  total jobs number %s is not equal with other sumnumber : %s (When status is %s)" % (
                    jobname, A, B, str(status)))


class Mainpage(unittest.TestCase):
    """Check home-page"""

    @classmethod
    def setUpClass(cls):
        uti.driver.implicitly_wait(10)
        uti.config()
        sleep(1)
        assert uti.find_element(By.CLASS_NAME, "logout", "logout", "mainpage")


    @classmethod
    def tearDownClass(cls):
        uti.driver.quit()

    # @pytest.mark.skipif(first_deploy_return,reason="Run only in first deploy")
    # def test_first_deploy_3jobs(self):
    #     """skip when condition is ture"""
    #     Jobcards = uti.driver.find_elements_by_class_name("main-card")
    #     for job_card in Jobcards:
    #         self.assertEqual(job_card.find_element_by_class_name("badge-warning").text,"UNKNOWN")
    #         self.assertEqual(len(str(job_card.find_element_by_id("commit-id1-1").text)),0)
    #         self.assertEqual(re.sub("\D", "", str(job_card.find_element_by_class_name("build_statistic").text).replace("\n", " ")),0000)
    #         self.assertEqual()
    #
    # @pytest.mark.skipif(first_deploy_return, reason="Run only in first deploy")
    # def test_first_deploy_awcy(self):
    #     """skip when condition is ture"""
    #     Jobcards = uti.driver.find_elements_by_class_name("main-card")
    #     for job_card in Jobcards:
    #         awcy_card = job_card.find_element_by_class_name("jobname").text
    #         if "REGRESSION_REPORT" in str(awcy_card).upper():
    #             page_description = job_card.find_element_by_id("info1")
    #             for real_job in job_info_total:
    #                 if str(awcy_card).lower() in str(real_job).lower():
    #                     real_description_row1 = re.findall('Desc":.+?\"', real_job)
    #                     real_description_row2 = str(real_description_row1[0]).replace('Desc":"', "")
    #                     real_description = str(re.findall('.+[^"]', real_description_row2))
    #                     if page_description == real_description:
    #                         uti.log("PASSED: %s  description : %s verify PASS" % (awcy_card, page_description))
    #                     else:
    #                         uti.log("FAILURE: %s  description : %s verify FAIL" % (awcy_card, page_description))
    #                     self.assertEqual(page_description, real_description)

    def test_account(self):
        """Test if the account information is correct"""
        sleep(1)
        uti.find_element(By.ID, "UserMe", "UserName", "mainpage")
        RealName = uti.username
        sleep(0.5)
        PageDisplayName = uti.driver.find_element_by_id('UserMe').text
        Account_status = uti.judge_equal(RealName,PageDisplayName,"Account name","LoginPage","MainPage")
        uti.log("================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)
        self.assertTrue(Account_status)

    def test_account_logout(self):
        click_logout = uti.click_element(By.CLASS_NAME, "logout", "//*[@id='test1']", "Log out", "MainPage")
        self.assertTrue(click_logout)
        sleep(3)
        uti.config()
        uti.log("================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)


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
        uti.log("================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)

    def test_click_Cidana_jpg(self):
        """Test click on the cidana icon in the title bar and it should have the correct response"""

        cidana_jpg = uti.driver.find_element(By.ID,"titleBackHomePage").is_displayed()
        if cidana_jpg is True:
            mainpage_window = uti.driver.current_url
            uti.driver.find_element_by_id("titleBackHomePage").click()
            page_url_now = uti.driver.current_url
            if mainpage_window == page_url_now:
                uti.log("\nPASSED: Click on the title image didn't redirect to a new window")
            else:
                uti.log("\nPASSED: Click on the title image to return to the address： %s"%page_url_now)
                uti.config()
                sleep(1)
        else:
            uti.log("\nFAILURE: The cidana picture in the title is abnormal")

        self.assertTrue(cidana_jpg)
        uti.log("================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)

    def test_mainpage_title(self):
        title_testframework = uti.find_element(By.CLASS_NAME,"testframework","PageTitle","Mainpage")
        self.assertTrue(title_testframework)
        uti.log("================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)

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
                jobtitle = "AWCYTESTDEMO"
            Jobtitle.append(jobtitle)

        #除去mainpage的标题和url
        Jobtitle.remove("TEST_FRAMEWORK")
        JobUrl.remove("http://ctpqa.cidanash.com:8083/")
        Num_Jobttitle = len(Jobtitle)
        Authority_of_ThisAccount = dict(zip(Jobtitle,JobUrl))

        Total_Authority = {"REGRESSION_REPORT": 'http://ctpqa.cidanash.com:8083/awcy_regress.php',
                           'CONFORMANCE_TEST': 'http://ctpqa.cidanash.com:8083/Jenkins_Job4.php?id=2',
                           'COVERAGE_TEST': 'http://ctpqa.cidanash.com:8083/Jenkins_Job3.php?id=3',
                           'PERFORMANCE_TEST': 'http://ctpqa.cidanash.com:8083/Jenkins_Job2.php?id=4'}

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
        uti.log("\n================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)

    def test_job_state(self):

        num_mean ={"0":"UNKNOWN","1":"WAITING","2":"BUILDING","3":"COMPLETED","4":"FAILED","5":"CANCELED"}

        #Information preprocessing
        global job_info_total
        page_source = uti.driver.page_source
        with open(r'F:\123.txt','w') as ps:
            ps.write(page_source)
            ps.close()
        jobs_info_total = re.findall('>\[.+',page_source)
        # job_info_total里的每一个列表元素都是一个job的全部信息
        job_info_total = re.findall('.+?\}',str(jobs_info_total))

        Jobcards = uti.driver.find_elements_by_class_name("main-card")
        self.assertEqual(len(Jobcards),len(job_info_total))
        j = True

        for job_card in Jobcards:
            ignore_card = job_card.find_element_by_class_name("jobname").text
            if "REGRESSION_REPORT" in str(ignore_card).upper():
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

                # jobstatus的校验
                try:
                    status = job_card.find_element_by_class_name("badge-warning").text
                    for real_job in job_info_total:
                        if str(jobname).lower() in str(real_job).lower():
                            real_status_str = re.findall('Status.+?\,', real_job)
                            real_status_number = re.sub("\D", "", str(real_status_str))
                            real_status = num_mean[real_status_number]
                            if status.lower() in real_status.lower():
                                uti.log("PASSED: %s  status : %s verify PASS" % (jobname, status))
                            else:
                                uti.log("FAILURE: %s  status : %s verify FAIL" % (jobname, status))
                            self.assertIn(str(status).lower(), str(real_status).lower())
                            print("-- status: ", status)
                    print(jobname, " Status is： ", str(status))
                except NoSuchElementException as error:
                    uti.log(
                        "%s : In %s,  Status exception (lookup: classname: 'badge-warning'); status of current item was not checked" % (
                        error, jobname.text))
                    j = False


                try:
                    TotalBuildInfo = job_card.find_element_by_class_name("build_statistic")
                    TotalBuildInfo_text = TotalBuildInfo.text.replace("\n", " ")
                    for real_job in job_info_total:
                        if str(jobname).lower() in str(real_job).lower():
                            real_totalinfo_str = re.findall('total.+?\}', real_job)
                            real_totalinfo_number = re.sub("\D", "", str(real_totalinfo_str))
                            page_totalinfo_number = re.sub("\D", "", str(TotalBuildInfo_text))
                            if real_totalinfo_number == page_totalinfo_number:
                                uti.log("PASSED: %s  totalinfo : %s verify PASS" % (jobname, TotalBuildInfo_text))
                            else:
                                uti.log("FAILURE: %s  totalinfo : %s verify FAIL" % (jobname, TotalBuildInfo_text))
                            self.assertEqual(real_totalinfo_number, page_totalinfo_number)

                            # 判断总和是否正确
                            page_total_info_number,sum_number = function_for_mainpage.re_findall(real_job)
                            if "BUILDING" in str(status).upper():
                                function_for_mainpage.totalinfo_compare_logprint(page_total_info_number - 1,sum_number,jobname,status)
                                self.assertEqual(page_total_info_number - 1, sum_number)
                            elif status == "UNKNOWN":
                                function_for_mainpage.totalinfo_compare_logprint(page_total_info_number, sum_number,jobname, status)
                                self.assertEqual(page_total_info_number,sum_number)
                                self.assertEqual(page_total_info_number,0,"Total info error in first deploy")
                            else:
                                function_for_mainpage.totalinfo_compare_logprint(page_total_info_number,sum_number,jobname,status)
                                self.assertEqual(page_total_info_number, sum_number)

                            print("-- totalinfo: ", TotalBuildInfo_text)
                except NoSuchElementException as error:
                    uti.log("%s : In %s, Total BuildInfo exception (Find by: classname: 'build statistic'); TotalBuildInfo for the current project was not detected "%(error,jobname.text))
                    j = False

                # job commit的校验
                try:
                    commit = str(job_card.find_element_by_id("commit-id1-1").text).replace("COMMIT : ", "")
                    for real_job in job_info_total:
                        if str(jobname).lower() in str(real_job).lower():
                            real_commit = re.findall('Commit.+?\,', real_job)
                            # When there is no commit, take the length of the string for comparison
                            if  status == "UNKNOWN":
                                uti.log("PASSED: %s  no commit when status is %s" % (jobname, status))
                            elif page_total_info_number == 1 and (status == "BUILDING" or "WAITING"):
                                uti.log("PASSED: %s  no commit when status is %s" % (jobname, status))
                            else:
                                if commit.lower() in str(real_commit).lower():
                                    uti.log("PASSED: %s  commit : %s verify PASS" % (jobname, commit))
                                else:
                                    uti.log("FAILURE: %s  commit : %s verify FAIL" % (jobname, commit))
                                self.assertIn(str(commit).lower(), str(real_commit).lower())
                            print("-- commit: ", commit)
                except NoSuchElementException as error:
                    uti.log(
                        "%s : In %s, An exception occurred in the commit (lookup method: id: 'commit-id 1-1'); the commit of the current project was not checked" % (
                            error, jobname.text))
                    j = False

                # jobdescription的校验
                try:
                    page_description_with_linebreak = job_card.find_element_by_id("info1").text
                    page_description = str(page_description_with_linebreak).replace("\n","")
                    for real_job in job_info_total:
                        if str(jobname).lower() in str(real_job).lower():
                            real_description_row1 = re.findall('Desc":.+?\",',real_job)
                            real_description_row2 = str(real_description_row1[0]).replace('Desc":"',"")
                            real_description = re.findall('.+[^",]',real_description_row2.replace('<br \\\\="">',""))
                            print("in page",page_description)
                            print("in real",str(real_description[0]))
                            if page_description == str(real_description[0]):
                                uti.log("PASSED: %s  description : %s verify PASS" % (jobname,page_description))
                            else:
                                uti.log("FAILURE: %s  description : %s verify FAIL" % (jobname, page_description))
                            self.assertEqual(page_description,str(real_description[0]))
                except NoSuchElementException as error:
                    uti.log("%s : In %s, Description exception (Find by: id: 'info1'); Description for the current project was not detected " % (error, jobname.text))
                    j = False

                print("\n")
        self.assertTrue(j)
        uti.log(
            "================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)

if __name__ == '__main__':
    unittest.main()




