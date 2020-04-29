#-*- coding: utf-8 -*-
import unittest,pytest
import lib_version4
import re,sys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep

uti = lib_version4.Utility_function()
num_mean ={"0":"UNKNOWN","1":"WAITING","2":"BUILDING","3":"COMPLETED","4":"FAILED","5":"CANCELED"}

class function_for_conformance():

    def get_mainpagecard(self, jobname):

        global status, commit, TotalBuildInfo
        Jobcards = uti.driver.find_elements_by_class_name("main-card")
        for job_card in Jobcards:
            if job_card.find_element_by_class_name("jobname").text == jobname:
                status = job_card.find_element_by_class_name("badge-warning").text
                commit = str(job_card.find_element_by_id("commit-id1-1").text).replace("COMMIT : ", "")
                TotalBuildInfo = job_card.find_element_by_class_name("build_statistic").find_element_by_class_name("total").text

    def judge_history(self):

        build_history = uti.lastbuild_exist("Conformance_Test")
        return build_history


    # def switch_to_jenkins(self,count_of_jobs):
    #     """获取jenkins中当前job标号，所用时间，开始时间，revision，job状态"""
    #     """需要分两种情况考虑，新部署的页面&已经有jobhistory的页面"""
    #     sleep(1)
    #     uti.driver.find_element_by_xpath('//*[@id="build_list"]/tr[1]/td[1]/a').click()
    #     uti.driver.find_element_by_xpath('//*[@class="item"][2]').click()
    #
    #     global jenkins_status,jenkins_id,jenkins_start_time,jenkins_duration_time,jenkins_commit
    #     jenkins_status_row = []
    #     jenkins_status = []
    #     jenkins_id = []
    #     jenkins_start_time = []
    #     jenkins_duration_time = []
    #     jenkins_commit_row = []
    #     jenkins_commit = []
    #
    #     for i in range(0,count_of_jobs):
    #         sleep(1)
    #         build_history_list = uti.driver.find_elements_by_class_name("single-line")
    #         if i < len(build_history_list):
    #             single_jenkins_job = build_history_list[i]
    #             jenkins_id.append(re.findall("#.+?",str(build_history_list[i].text))[0])
    #             jenkins_start_time.append(build_history_list[i].text)
    #             sleep(1)
    #             jenkins_status_row.append(uti.driver.find_element_by_xpath('//*[@class="build-status-link"]/img').get_attribute("alt"))
    #             single_jenkins_job.find_element_by_class_name("build-name").click()
    #             try:
    #                 duration_time_location = uti.driver.find_element_by_xpath('//*[@id="main-panel"]/div/div[2]/a').text
    #             except NoSuchElementException:
    #                 duration_time_location = uti.driver.find_element_by_xpath('//*[@id="main-panel"]/div/div[2]').text
    #             jenkins_duration_time.append(duration_time_location)
    #             jenkins_commit_row.append(uti.driver.find_element_by_xpath('//*[@id="main-panel"]//tr[3]/td[2]').text)
    #             uti.driver.back()
    #         else:
    #             pass
    #     uti.driver.back()
    #     uti.driver.back()
    #
    #     # 加工处理status的信息
    #     print(jenkins_status_row)
    #     for status in jenkins_status_row:
    #         if "Success" in status:
    #             jenkins_status.append("COMPLETED")
    #         if "Aborted" in status:
    #             jenkins_status.append("CANCELED")
    #         if "In progress" in status:
    #             jenkins_status.append("BUILDING")
    #         else:
    #             pass
    #
    #     # 加工处理commit的信息
    #     for single_commit in jenkins_commit_row:
    #         if "Revision" in str(single_commit):
    #             jenkins_commit.append(str(re.findall("[a-zA-Z0-9]*",str(single_commit))[3]))
    #         elif "Aborted" in str(single_commit):
    #             jenkins_commit.append("neterror")
    #         else:
    #             pass
    #
    #     print("jenkins_status",jenkins_status)
    #     print("jenkins_id",jenkins_id)
    #     print("jenkins_start_time",jenkins_start_time)
    #     print("jenkins_duration_time",jenkins_duration_time)
    #     print('jenkins_commit',jenkins_commit)
    #     # uti.driver.switch_to.window(now_window)
    #     assert len(build_history_list) == count_of_jobs

class Conformance(unittest.TestCase):
    """Check conformance-page"""

    @classmethod
    def setUpClass(cls):
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
        assert uti.switch_window(By.XPATH, "//div[@id='left_jobs']/div[2]/div[4]/div[2]", 'Conformance','Conformance Test - This is a Conformance Test Demo dashboard.')

        # 为判断首次deploy提供依据，当返回值为true，说明是不是首次deploy，不执行专门测试首次deploy的用例（即跳过它去执行其他的）
        global build_history
        build_history = function_for_conformance().judge_history()


        # 拿到last 10 builds中的后端数据
        global Ajax_list
        Ajax_list = uti.get_Ajax("your url")

    # @pytest.mark.skipif(build_history, reason="Run only in first deploy")
    # def test_first_deploy(self):
    #     """TODO:statusbar,chart,basic,output,buildlist  all of those should be emputy"""
    #     pass

    def test_allstatus_compare(self):

        mainpage_status = mainpage_conformance_card["status"]
        statusbar_status = uti.driver.find_element_by_class_name("STYLE8").text
        joblist_status_row = uti.driver.find_elements_by_class_name("badge")
        global joblist_status
        joblist_status = []
        for single_status_in_joblist in joblist_status_row:
            joblist_status.append(single_status_in_joblist.text)
        Ajax_joblist_status = uti.num_trans_status(Ajax_list)
        if len(joblist_status) == 1:
            if joblist_status[0] == 'BUILDING':
                uti.judge_equal_3(num_mean[Ajax_list['Status']],joblist_status[0],mainpage_status,"Job status ")
            else:
                uti.judge_equal_4(num_mean[Ajax_list['Status']],joblist_status[0],statusbar_status,mainpage_status,"Job status ")
        else:
            uti.judge_equal_4(num_mean[str(Ajax_list[0]['Status'])], joblist_status[0], statusbar_status, mainpage_status,"Job status ")
            self.assertEqual(Ajax_joblist_status,joblist_status,"joblist status and Ajax_joblist status exist difference(s) ")
        uti.log("================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)

    def test_commit_compare(self):
        mainpage_commit = mainpage_conformance_card["commit"]
        statusbar_commit_row = uti.driver.find_element_by_xpath('//*[@class="card mb-3 widget-content bg-midnight-bloom"]//*[@name="LastBuildCommit"]').text
        statusbar_commit = str(statusbar_commit_row).replace("Commit: ","")
        joblist_commit_row = uti.driver.find_elements_by_xpath('//*[@id="build_list"]//*[@class="widget-heading"]')
        joblist_commit = []
        for jobcommit in joblist_commit_row:
            joblist_commit.append(str(jobcommit.text).replace("Commit:","").replace(" ",""))

        if len(joblist_commit) == 1:
            if joblist_status[0] == 'BUILDING':
                self.assertTrue(uti.judge_equal_3(Ajax_list['CommitID'],joblist_commit[0],mainpage_commit,"Job commit "))
            else:
                self.assertTrue(uti.judge_equal_4(Ajax_list['CommitID'],joblist_commit[0],statusbar_commit,mainpage_commit,"Job commit "))
        else:
            Ajax_commit_list = []
            for One_Object in Ajax_list:
                Ajax_commit_list.append(One_Object['CommitID'])
            self.assertTrue(uti.judge_equal_4(Ajax_commit_list[0], joblist_commit[0], statusbar_commit,mainpage_commit,"Job commit "))
            self.assertEqual(Ajax_commit_list,joblist_commit,"joblist commit and Ajax_joblist commit exist difference(s) ")

    def test_basicoutput(self):
        """TODO:暂未决定要测试哪些功能点"""
        pass

        uti.log("================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)

    def test_fulllog(self):
        """TODO:1。full log按钮点击能否显示正确的新窗口；2.full log标题是否有，full log的x号是否有且点击跳转正确；3。up&down是否有且点击有正确效果；4.水平滚动条是否有且拖动是否有相应效果"""
        self.assertTrue(uti.click_element(By.ID,"open_btn",'//*[@id="close-button"]',"Full Log","Conformance_Test"))
        self.assertTrue(uti.js_top_down_btn("Conformance_Test"))
        self.assertTrue(uti.click_element(By.XPATH,'//*[@id="close-button"]','//*[@id="open-btn"]',"Button of close full log","Full log"))
        uti.log(
            "================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)

    def test_last_10_build_id(self):

        self.assertTrue(uti.judge_jobid("Conformance_test"))
        uti.log(
            "================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)

    def test_last_10_build_message(self):

        
        uti.log(
            "================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)

    def test_last_10_build_starttime(self):

        pass
        uti.log(
            "================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)

    def test_last_10_build_duration(self):

        pass
        uti.log(
            "================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)

    def test_last_10_build_operator(self):

        pass
        uti.log(
            "================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)

    def test_last_10_build_report(self):
        pass
        uti.log(
            "================== The case: %s status now is END =================== \n" % sys._getframe().f_code.co_name)



if __name__ == '__main__':
    unittest.main()
