import hashlib
import time
from common import RED_CLI,Tel_total,com_reserve,sendID
from flask import current_app
import requests
import os

# 执行异步函数
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(1)

class CheckTel(object):

    def __init__(self,userid):
        # self.userid = userid
        self.userid = "102888"
        self.s = requests.session()
        self.s.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
            }
        )

    def check_before(self):
        """从未检测表中取出数据存入待检测txt文档中,准备检测"""

        # 1. 从库里面查询出所有没有检测的数据
        count = com_reserve.find({"tel_check":"待检测"}).count()
        dict = {}
        if count > 2000:
            if count > 3000:
                result = com_reserve.find({"tel_check":"待检测"}).limit(3000)
            else:
                result = com_reserve.find({"tel_check": "待检测"}).limit(3000)

            TxtPath = r'D:\bmd\bmd_server\src\company\flask_server\files\{}\TEL\待检测号码.txt'.format(self.userid)
            if os.path.exists(TxtPath):
                os.remove(TxtPath)
            else:
                pass

            for _ in result:
                phone = _["companyTel"]
                with open(TxtPath, "a", encoding='utf-8') as fp:
                    fp.write(phone + '\n')
            dict["msg"] = "生成文本sucess。。。"
        else:
            dict["msg"] = "可检测数据不足3000条"
        return dict


    def tel_check_save(self,result,cuurent_time):

        # 2.循环列表解析数据更新
        count = 0
        for lt in result:
            item = {}
            item["_id"] = hashlib.md5(str(lt["tel"]).encode('utf-8')).hexdigest()
            item["tel"] = lt["tel"]
            item["out_name"] = ""
            item["tel_type"] = lt["name"]
            item["detect_time"] = cuurent_time
            try:
                # 更新空号池
                Tel_total.save(item)
            except Exception as e:
                current_app.log.info(e)

            # 更新数据总表中该条号码的状态
            try:
                checkResult = com_reserve.find_one({"companyTel":lt["tel"]})
                checkResult["tel_check"] = lt["name"]
                com_reserve.save(checkResult)

            except Exception as e:
                current_app.log.info(e)
            count += 1
            print("号码状态更新成功")
            print(count)

    def check_after(self):
        """对检测后的号码进行更新到号码状态总表中去"""

        result = []
        cuurent_time = str(time.strftime("%Y-%m-%d", time.localtime()))

        # 1. 读取文本数据统一添加到列表中
        realPath = r'D:\bmd\bmd_server\src\company\flask_server\files\{}\TEL\活跃号.txt'.format(self.userid)
        with open(realPath,"r",encoding='utf-8') as fp:
            resp = fp.read()
            res = resp.replace('\ufeff',"").split("\n")
            for _ in res:
                succeed_check = {}
                if _:
                    succeed_check["name"] = "实号"
                    succeed_check["tel"] = _
                    result.append(succeed_check)

        # emptyPath = r'D:\bmd\bmd_server\src\company\flask_server\files\{}\TEL\空号.txt'.format(self.userid)
        # with open(emptyPath,"r",encoding='utf-8') as fp:
        #     resp = fp.read()
        #     res = resp.replace('\ufeff', "").split("\n")
        #     for _ in res:
        #         empty_check = {}
        #         if _:
        #             empty_check["name"] = "空号"
        #             empty_check["tel"] = _
        #             result.append(empty_check)
        #
        # silencePath = r'D:\bmd\bmd_server\src\company\flask_server\files\{}\TEL\沉默号.txt'.format(self.userid)
        # with open(silencePath, "r", encoding='utf-8') as fp:
        #
        #     resp = fp.read()
        #     res = resp.replace('\ufeff', "").split("\n")
        #     for _ in res:
        #         silence_check = {}
        #         if _:
        #             silence_check["name"] = "沉默号"
        #             silence_check["tel"] = _
        #             result.append(silence_check)
        #
        # riskPath = r'D:\bmd\bmd_server\src\company\flask_server\files\{}\TEL\风险号.txt'.format(self.userid)
        # with open(riskPath, "r", encoding='utf-8') as fp:
        #     resp = fp.read()
        #     res = resp.replace('\ufeff', "").split("\n")
        #     for _ in res:
        #         risk_check = {}
        #         if _:
        #             risk_check["name"] = "风险号"
        #             risk_check["tel"] = _
        #             result.append(risk_check)
        executor.submit(self.tel_check_save(result,cuurent_time))
        # self.tel_check_save(result,cuurent_time)

        return result


    def updefile(self):
        """
        请求上传接口进行文件上传
        :return:
        """

        try:
            TxtPath = r'D:\bmd\bmd_server\src\company\flask_server\files\{}\TEL\待检测号码.txt'.format(self.userid)
            # with open(text_path,)
            data = {
                "account":"18502882837",
                "pass":"dgg962540",
            }
            file = {"file": open(TxtPath, "rb")}
            resp = self.s.post('https://xcjk.mobwin.me/api/Upload.ashx',data=data,files=file)
            # resp = self.s.post('http://127.0.0.1:8082/tel/test',files=file)
            print(resp.text)
            # print(resp.text)
            res = resp.json()
            sendid = res["DATA"]["sendID"]
            print(sendid)
            dict = {}
            dict["user"] = self.userid
            dict["_id"] = hashlib.md5(str(sendid).encode("utf-8")).hexdigest()
            dict["sendID"] = sendid
            dict["time"] = str(int(time.time() * 1000))
            dict["local_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            sendID.insert(dict)
            return sendid
        except Exception as e:
            current_app.log.info(e)
            return False


    def search_api(self,sendIDS):
        """
        查询接口API
        :param
        :return:
        """
        dict = {}
        try:
            user_result = sendID.find_one({"user": self.userid,"sendID":sendIDS})
            if user_result["sendID"]:
                url = 'http://101.132.111.135:1688/api/Query.ashx'
                data = {
                    "account": "18502882837",
                    "pass": "dgg962540",
                    "sendID": sendIDS,
                }
                resp = self.s.post('http://101.132.111.135:1688/api/Query.ashx', data=data)
                result = resp.json()
                if result["DATA"]["status"] == "2":
                    dict["code"] = 200
                    dict["活跃号数量"] = result["DATA"]["number2"]
                    dict["空号数量"] = result["DATA"]["number3"]
                    dict["沉默号数量"] = result["DATA"]["number4"]
                    dict["风险号数量"] = result["DATA"]["number5"]
                else:
                    dict["code"] = 203
                    dict["msg"] = "暂未检测完成，建议稍后尝试"
            else:
                items = {}
                items["user"] = self.userid
                items["_id"] = hashlib.md5(str(sendIDS).encode("utf-8")).hexdigest()
                items["sendID"] = sendIDS
                items["time"] = str(int(time.time() * 1000))
                items["local_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                sendID.insert(items)

            return dict


        except Exception as e:
            current_app.log.info("清洗时错误")

    def down_api(self,sendIDS):
        """
        请求接口下载压缩包.zip格式
        :param sendIDS:
        :return:
        """
        try:
            data = {
                "account": "18502882837",
                "pass": "dgg962540",
                "sendID": sendIDS,
                "type":1,
            }
            resp = self.s.post('http://101.132.111.135:1688/api/Download.ashx', data=data)
            file_path = r'D:\bmd\bmd_server\src\company\flask_server\files\{}\TEL\result.zip'.format(self.userid)
            with open(file_path,'wb') as fp:
                fp.write(resp.content)
                return True
        except:
            return False




if __name__ == '__main__':
   start =  CheckTel("102888")
   start.updefile()
