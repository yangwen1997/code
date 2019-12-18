# author yangwenlong

from flask_server.common import com_reserve,Online_total,Tel_total,RED_CLI

from flask import current_app
class check_reserve(object):
    """
    检查数据是否推送类及数据是否进行过号码检测
    """
    def __init__(self):
        pass

    def check_online_total(self):
        """
        检测数据是否推送
        :return: sucess_count : 查询的数据总数
        :return: To_push : 已经推送的数量总数
        :return: Not_push : 未推送的数量总数
        :return: push_lt : 可以推送的数据ID列表
        """
        try:
            # 1. 查询数据总表中刚推进来的数据总量
            online_total_state = com_reserve.find({"push":{"$exists":False}, "tel_check":{"$exists":False}})
            sucess_count = 0
            To_push = 0
            Not_push = 0
            push_lt = []

            for _ in online_total_state:
                # 2. 当数据存在进行到推送状态表中进行查询,给数据添加指定的推送状态push,没有新数据直接结束
                if _:
                    id = _["_id"]
                    search_result = Online_total.find_one({"_id":id})
                    if search_result:
                        _["push"] = "1"
                        To_push += 1
                    else:
                        _["push"] = "0"
                        dict = {}
                        Not_push += 1
                        dict["ID"] = Not_push
                        dict["companyName"] = _["companyName"]
                        dict["companyTel"] = _["companyTel"]
                        dict["not_push"] = "未推送"
                        push_lt.append(dict)
                    com_reserve.save(_)
                else:
                    break
                sucess_count += 1

            return sucess_count,To_push,Not_push,push_lt
        except Exception as e:
            current_app.logger.info(e)

    def check_tel_total(self):
        """
        检查数据号码状态
        :return: sucessount : 检测过的数据总量
        :return: sucess_lt : 检测过的数据ID
        :return: totalCount : 未检测过的数据总量
        :return: total_lt : 未检测过的数据ID
        """
        try:
            sucessount = 0
            sucess_lt = []

            totalCount = 0
            total_lt = []
            # 1.查询出数据总表中没有被推送的数据
            Tel_total_result = com_reserve.find({"push":"0", "tel_check":{"$exists":False}})

            # 2. 检查数据总表中的最新的没有推送的数据
            for _ in Tel_total_result:
                # 2.如果没有直接结束,有进行操作
                if _:
                    id = _["_id"]
                    result = Tel_total.find_one({"_id":id})

                    # 3. 获取最新的未推送的数据查询号码状态,如果查到设置对应的号码状态,没有查到存入检测表缓存并回写数据待检测
                    if result:
                        tel_type = result["tel_type"]
                        _["tel_check"] = tel_type
                        com_reserve.save(_)
                        sucess_lt.append(id)
                    else:
                        # 4.如果数据没有被检测过回写字段tel_type 并存入redis 缓存表
                        _["tel_check"] = "待检测"
                        com_reserve.save(_)
                        dict_res = {}
                        dict_res["_id"] = id
                        dict_res["phone"] = _["companyTel"]
                        totalCount +=1
                        total_lt.append(id)
                    sucessount += 1
                else:
                    break


            return sucessount,sucess_lt,totalCount,total_lt
        except Exception as e:
            current_app.logger.info(e)


    def run(self):
        self.check_online_total()
        # self.check_tel_total()

    def test_add(self):
        current_app.logger.info("异步任务测试启动成功")
        tag = "测试任务"
        return tag



# 单文件测试启动
if __name__ == '__main__':
    start = check_reserve()
    start.run()
