import hashlib
import time
from common import RED_CLI,Tel_total,com_reserve
class CheckTel(object):

    def __init__(self):
        pass

    def check_before(self):
        """从未检测表中取出数据存入待检测txt文档中,准备检测"""

        # 1. 从库里面查询出所有没有检测的数据
        count = com_reserve.find({"tel_check":"待检测"}).count()
        if count > 3000:
            if count > 10000:
                result = com_reserve.find({"tel_check":"待检测"}).limit(10000)
            else:
                result = com_reserve.find({"tel_check": "待检测"})

            for _ in result:
                phone = _["companyTel"]
                with open(r'D:\bmd\bmd_server\src\company\check_tel_phone\待检测号码.txt', "a", encoding='utf-8') as fp:
                    fp.write(phone + '\n')
            print("数据写入文本成功")

    def check_after(self):
        """对检测后的号码进行更新到号码状态总表中去"""

        result = []
        succeed_check = {}
        empty_check = {}
        silence_check = {}
        risk_check = {}
        cuurent_time = str(time.strftime("%Y-%m-%d", time.localtime()))

        # 1. 读取文本数据统一添加到列表中
        with open(r'D:\bmd\bmd_server\src\company\check_tel_phone\实号.txt',"r",encoding='utf-8') as fp:
            succeed_check["phone"] = fp.readlines()
        succeed_check["name"] = "实号"
        result.append(succeed_check)

        with open(r'D:\bmd\bmd_server\src\company\check_tel_phone\空号.txt',"r",encoding='utf-8') as fp:
            empty_check["phone"] = fp.readlines()
        empty_check["name"] = "空号"
        result.append(empty_check)

        with open(r'D:\bmd\bmd_server\src\company\check_tel_phone\沉默号.txt', "r", encoding='utf-8') as fp:
            silence_check["phone"] = fp.readlines()
        silence_check["name"] = "沉默号"
        result.append(silence_check)

        with open(r'D:\bmd\bmd_server\src\company\check_tel_phone\风险号.txt', "r", encoding='utf-8') as fp:
            risk_check["phone"] = fp.readlines()
        risk_check["name"] = "风险号"
        result.append(risk_check)

        # 2.循环列表解析数据更新
        for lt in result:
            result_dict = {}

            phone_name = lt["name"]
            for _ in lt["phone"]:
                result_dict["name"] = phone_name
                result_dict["phone"] = _.replace("\n","")
                result_dict["out_name"] =  ""
                result_dict["_id"] = hashlib.md5(result_dict["phone"].encode(encoding='utf-8')).hexdigest()
                result_dict["detect_time"] = cuurent_time
                print(result_dict)

                # 3. 将结果更新到号码状态总表中
                # Tel_total.save(result_dict)


    def check_tel(self):
        pass

if __name__ == '__main__':
   start =  CheckTel()
   start.check_before()
