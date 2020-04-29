# -*- coding: utf-8 -*-
import unittest, pytest
import lib_version4
import re, sys
from selenium.webdriver.common.by import By
from time import sleep

uti = lib_version4.Utility_function()

class function_for_conformance():

    def get_mainpagecard(self, jobname):

        global status, commit, TotalBuildInfo
        Jobcards = uti.driver.find_elements_by_class_name("main-card")
        for job_card in Jobcards:
            if job_card.find_element_by_class_name("jobname").text == jobname:
                status = job_card.find_element_by_class_name("badge-warning").text
                commit = str(job_card.find_element_by_id("commit-id1-1").text).replace("COMMIT : ", "")
                TotalBuildInfo = job_card.find_element_by_class_name("build_statistic").find_element_by_class_name(
                    "total").text

    def judge_history(self):

        build_history = uti.lastbuild_exist("Conformance_Test")
        return build_history


class Conformance(unittest.TestCase):
    """Check conformance-page"""

    @classmethod
    def setUpClass(cls):
        sleep(2)
        uti.driver.implicitly_wait(10)
        uti.config()
        sleep(1)
        assert uti.find_element(By.CLASS_NAME, "logout", "logout", "mainpage")

        # 获取到mainpage中用来对比的信息
        function_for_conformance().get_mainpagecard("CONFORMANCE_TEST")
        print(status, "--", commit, "--", TotalBuildInfo)
        TotalBuildInfo_num = re.sub("\D", "", str(TotalBuildInfo))
        mainpage_obj = ["status", "commit", "total"]
        mainpage_obj_data = []
        for ele in status, commit, TotalBuildInfo_num:
            mainpage_obj_data.append(ele)
        global mainpage_conformance_card
        mainpage_conformance_card = dict(zip(mainpage_obj, mainpage_obj_data))

        # 跳转到Conformance页面
        assert uti.switch_window(By.XPATH, "//div[@id='left_jobs']/div[2]/div[4]/div[2]", 'Conformance',
                                 'Conformance Test - This is a Conformance Test Demo dashboard.')

        # 为判断首次deploy提供依据，当返回值为true，说明是不是首次deploy，不执行专门测试首次deploy的用例（即跳过它去执行其他的）
        global build_history
        build_history = function_for_conformance().judge_history()

        # 拿到last 10 builds中的后端数据
        global Ajax_list
        Ajax_list = uti.get_Ajax("http://ctpqa.cidanash.com:8083/ajax-getBuilds.php?count=10&job=2")

        global joblist_id, joblist_commit, joblist_message, joblist_starttime, joblist_duration, joblist_by, joblist_status
        joblist_id, joblist_commit, joblist_message, joblist_starttime, joblist_duration, joblist_by, joblist_status = uti.get_Page_10builds_info()

        global Ajax_id, Ajax_commit, Ajax_message, Ajax_starttime, Ajax_duration, Ajax_by, Ajax_status
        Ajax_id, Ajax_commit, Ajax_message, Ajax_starttime, Ajax_duration, Ajax_by, Ajax_status = uti.get_Ajax_10build_info(Ajax_list)


    def test_allstatus_compare(self):

        mainpage_status = mainpage_conformance_card["status"]
        statusbar_status = uti.driver.find_element_by_class_name("STYLE8").text
        Ajax_joblist_status = uti.num_trans_status(Ajax_list)
        if len(joblist_status) == 1:
            if joblist_status[0] == 'BUILDING':
                uti.judge_equal_3(Ajax_joblist_status[0], joblist_status[0], mainpage_status, "Job status ")
            else:
                uti.judge_equal_4(Ajax_joblist_status[0], joblist_status[0], statusbar_status, mainpage_status,"Job status ")
        else:
            uti.judge_equal_4(Ajax_joblist_status[0], joblist_status[0], statusbar_status,mainpage_status, "Job status ")
            self.assertEqual(Ajax_joblist_status, joblist_status,"joblist status and Ajax_joblist status exist difference(s) ")
            self.assertEqual(len(joblist_status),len(Ajax_status),"The number of joblist_status and Ajax_status is not Equal")
        uti.log("\n================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)

    def test_commit_compare(self):
        mainpage_commit = mainpage_conformance_card["commit"]
        statusbar_commit_row = uti.driver.find_element_by_xpath(
            '//*[@class="card mb-3 widget-content bg-midnight-bloom"]//*[@name="LastBuildCommit"]').text
        statusbar_commit = str(statusbar_commit_row).replace("Commit: ", "")

        if len(joblist_commit) == 1:
            if joblist_status[0] == 'BUILDING':
                self.assertTrue(uti.judge_equal_3(Ajax_commit[0], joblist_commit[0], mainpage_commit, "Job commit "))
            else:
                self.assertTrue(uti.judge_equal_4(Ajax_commit[0], joblist_commit[0], statusbar_commit, mainpage_commit,"Job commit "))
        else:
            self.assertTrue(uti.judge_equal_4(Ajax_commit[0], joblist_commit[0], statusbar_commit, mainpage_commit,"Job commit "),"The commit in ajax,joblist,statusbar,mainpage is not equal")
            self.assertEqual(Ajax_commit, joblist_commit,"joblist commit and Ajax_joblist commit exist difference(s) ")
        self.assertEqual(len(joblist_commit), len(Ajax_commit),"The number of joblist_commit and Ajax_commit is not Equal")
        uti.log("\n================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)

    def test_basicoutput(self):
        """TODO:暂未决定要测试哪些功能点"""
        pass

        uti.log("\n================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)

    def test_fulllog(self):
        """TODO:1。full log按钮点击能否显示正确的新窗口；2.full log标题是否有，full log的x号是否有且点击跳转正确；3。up&down是否有且点击有正确效果；4.水平滚动条是否有且拖动是否有相应效果"""
        self.assertTrue(uti.click_element(By.ID, "open_btn", '//*[@id="close-button"]', "Full Log", "Conformance_Test"))
        self.assertTrue(uti.js_top_down_btn("Conformance_Test"))
        self.assertTrue(uti.click_element(By.ID, "close-button", '//*[@id="open-btn"]', "Button of close full log","Full log"))

        uti.log("\n================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)

    def test_last_10_build_id(self):

        self.assertTrue(uti.judge_jobid("Conformance_test"))
        self.assertEqual(joblist_id,Ajax_id,"joblist id not equal to ajax id")
        self.assertEqual(len(joblist_id), len(Ajax_id),"The number of joblist_id and Ajax_id is not Equal")
        uti.log("\n================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)

    def test_last_10_build_message(self):

        self.assertEqual(joblist_message, Ajax_message)
        self.assertEqual(len(joblist_message), len(Ajax_message), "The number of joblist_message and Ajax_message is not Equal")
        uti.log("\n================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)

    def test_last_10_build_starttime(self):

        self.assertEqual(joblist_starttime,Ajax_starttime,"joblist starttime not equal to ajax starttime")
        self.assertEqual(len(joblist_starttime), len(Ajax_starttime),"The number of joblist_starttime and Ajax_starttime is not Equal")
        uti.log("\n================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)

    def test_last_10_build_duration(self):

        self.assertEqual(joblist_duration, Ajax_duration, "joblist duration not equal to ajax duration")
        self.assertEqual(len(joblist_duration), len(Ajax_duration),"The number of joblist_duration and Ajax_duration is not Equal")
        uti.log("\n================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)

    def test_last_10_build_operator(self):

        self.assertEqual(joblist_by,Ajax_by,"joblist operator not equal to ajax operator")
        self.assertEqual(len(joblist_by), len(Ajax_by),"The number of joblist_operator and Ajax_operator is not Equal")
        uti.log("\n================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)

    def test_last_10_build_report(self):
        uti.log("\n================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)


if __name__ == '__main__':
    unittest.main()