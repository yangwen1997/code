import hashlib
from common import com_reserve,DATA_result,target_db
import urllib
import re

from flask import current_app
class Data_push(object):

    """
    数据处理推送至顶企客
    """
    def __init__(self):
        """
        :return self.liquid_names : 液态在iboss中对应的唯一编码
        """
        self.liquid_names = {
            "项目": "BUS_YT_XM",
            "工商": "BUS_YT_CY",
            "资质": "BUS_YT_ZZ",
            "互联网": "BUS_YT_HLW",
            "财税": "BUS_YT_CS",
            "会计": "BUS_YT_KJ",
            "金融发展": "BUS_YT_JRFZ",
            "法律": "BUS_YT_FL",
            "培训（大卓商学院）": "BUS_YT_DZSXY",
            "综合": "BUS_YT_ZH",
            "知产": "BUS_YT_ZSCQ",
            "品牌": "BUS_YT_PP",
            "人事外包": "BUS_YT_RSWB",
            "装饰": "BUS_YT_ZS",
            "融资": "BUS_YT_DK",
            "商标版权": "BUS_YT_SBBQ",
            "专利项目": "BUS_YT_ZLXM",
            "巨方地产(禁用)": "BUS_YT_JFDC",
            "认证": "BUS_YT_TXRZ",
            "创新": "BUS_YT_CX",
            "网点交易": "BUS_YT_WDJY"
        }

    def data_save(self,sucess_data,data,code_name,liquid_name):
        """
        :param sucess_data: 保存数据的空字典
        :param data: 需要解析该条数据信息
        :param code_name: 液态iboss编码
        :param liquid_name: 推送的液态名称
        :return: sucess_data ：保存成功的数据
        """
        try:
            sucess_data["_id"] = hashlib.md5(str(data["companyTel"] + liquid_name).encode(encoding='utf-8')).hexdigest()
            sucess_data["companyName"] = data["companyName"]
            sucess_data["companyTel"] = data["companyTel"]
            sucess_data["outName"] = ""

            # 省份进行判断,市进行判断
            if re.search("北京",data["companyProvince"]) :
                sucess_data["companyCity"] = "北京"
                sucess_data["companyProvince"] = "北京市"
            elif re.search("重庆",data["companyProvince"]):
                sucess_data["companyCity"] = "重庆"
                sucess_data["companyProvince"] = "重庆市"
            elif re.search("上海",data["companyProvince"]):
                sucess_data["companyCity"] = "上海"
                sucess_data["companyProvince"] = "上海市"
            else:
                if data["companyProvince"]:
                    if re.search("省",data["companyProvince"]):
                        sucess_data["companyProvince"] = data["companyProvince"]
                    else:
                        sucess_data["companyProvince"] = data["companyProvince"] + "省"
                if data["companyCity"]:
                    if re.search("市",data["companyCity"]):
                        sucess_data["companyCity"] = data["companyCity"].replace("市","")
                    else:
                        sucess_data["companyCity"] = data["companyCity"]

            sucess_data["companyAddr"] = data["registerAddress"]
            sucess_data["name"] = liquid_name
            sucess_data["code"] = code_name
            sucess_data["busCode"] = ""
            sucess_data["webUrl"] = "https://www.qichacha.com/search?key=" + urllib.parse.quote(sucess_data["companyName"])
            sucess_data["resourceRemark"] = "城市：{},法人：{},注册时间：{}，注册资本：{}，经营范围：{}".format(data["companyCity"],
                                                                                         data["legalMan"],data["registerTime"],
                                                                                         data["registerMoney"],data["businessScope"])
            sucess_data.update({
                "ibossNum": None,
                "orgId": None,
                "deptId": None,
                "centreId": None,
            })
            sucess_data["isDir"] = 0
            sucess_data["isShare"] = 0

            #推送至目标库后修改数据的push值回写到数据总表
            target_db.save(sucess_data)
            data["push"] = "2"
            com_reserve.update({"_id":data["_id"]},data)

            return sucess_data
        except Exception as e:
            current_app.logger.info(e)

    def data_mark_none(self,count=None,liquid_name_lt=None,result_num=None,data=None,liquid_name=None):
        """
        数据的推送规则处理
        :param result_num: 液态数据，多条
        :param count: 推送数量
        :param data: 单条数据
        :param liquid_name_lt: 规则
        :param liquid_name: 要推送的液态名

        :return:dict_lt ： 推送成功保存起来的数据列表
        :return:sucess_count ： 推送成功的剩余数量
        """
        try:

            if liquid_name_lt:
                # 1. 通用判断
                pass
            else:
                # 2. 工商和法律的初次判断，只存在result_num，以及count,liquid_name
                sucess_count = count
                dict_lt = []
                for _ in result_num:
                    sucess_data = {}
                    code_name = self.liquid_names[liquid_name]
                    suces_result = self.data_save(sucess_data=sucess_data, data=_, code_name=code_name,liquid_name=liquid_name)
                    dict_lt.append(suces_result)
                    sucess_count -= 1

                    if sucess_count <= 0:
                        break

                return dict_lt,sucess_count
        except Exception as e:
            current_app.logger.info(e)

    def data_second_iduge(self,count,liquid_name):
        """
        工商和法律的数据推送判断逻辑
        :param count: 推送的数据总数
        :param liquid_name: 液态名
        :return:
        """
        result_num = com_reserve.find({"push": "0", "tel_check": "实号", "mark": ""}).count()
        dict_result = {}
        if result_num > 0:
            result_num = com_reserve.find({"push": "0", "tel_check": "实号", "mark": ""})
            sucess_lt, sucess_count = self.data_mark_none(result_num=result_num, count=count, liquid_name=liquid_name)
            if sucess_count <= 0:
                dict_result["SucessResult"] = sucess_lt
                dict_result["msg"] = "数据补充{}条".format((count - sucess_count))

            else:
                # 数据不够指定推送的数据时
                result_num = com_reserve.find({"push": "0", "tel_check": "实号"})
                dict_lt, sucess_count = self.data_mark_none(result_num=result_num, count=sucess_count,
                                                            liquid_name=liquid_name)

                sucess_lt += dict_lt
                dict_result["SucessResult"] = sucess_lt
                dict_result["msg"] = "数据补充{}条".format((count - sucess_count))
                if sucess_count > 0:
                    dict_result["err_num"] = "数据剩余{}条未推送，暂时没有该液态的资源数据".format(sucess_count)
        else:
            result_num = com_reserve.find({"push": "0", "tel_check": "实号"})
            sucess_lt, sucess_count = self.data_mark_none(result_num=result_num, count=count,
                                                          liquid_name=liquid_name)
            dict_result["SucessResult"] = sucess_lt
            dict_result["msg"] = "数据补充{}条".format((count - sucess_count))
            if sucess_count > 0:
                dict_result["Not_push_msg"] = "数据剩余{}条未推送，暂时没有该液态的资源数据".format(sucess_count)

        return dict_result

    def data_first_iduge(self,count,liquid_name):
        """
        工商/法律 液态的数据推送处理逻辑
        :param data: 数据总数
        :param count: 推送的数据量
        :return:
        """

        class_count = com_reserve.find({"push": "0", "tel_check": "实号", "mark":str(liquid_name)}).count()
        if class_count > 0:
            # 1. mark存在时直接查询推送
            if class_count - count > 0:
                result_num = com_reserve.find({"push": "0", "tel_check": "实号", "mark":str(liquid_name)}).limit(count)
            else:
                result_num = com_reserve.find({"push": "0", "tel_check": "实号", "mark": str(liquid_name)})
            sucess_lt, sucess_count = self.data_mark_none(result_num=result_num, count=count, liquid_name=liquid_name)
            dict_result = {}
            if sucess_count <= 0:
                # 2.如果mark为该液态的数据直接存在时
                dict_result["SucessResult"] = sucess_lt
                dict_result["msg"] = "数据补充{}条".format((count - sucess_count))
                dict_result["Not_push_msg"] = "数据剩余{}条未推送".format(sucess_count)
            else:
                # 3.如果mark为该液态的数据不够推送的数据时
                result_num = com_reserve.find({"push": "0", "tel_check": "实号"})
                dict_lt,sucess_count = self.data_mark_none(result_num=result_num, count=sucess_count, liquid_name=liquid_name)

                # 4.两次获取的数据进行相加合并计算出推送的数据总量及剩余的数量
                sucess_lt += dict_lt
                dict_result["SucessResult"] = sucess_lt
                dict_result["msg"] = "数据补充{}条".format((count - sucess_count))
                if sucess_count > 0:
                    dict_result["err_num"] = "数据剩余{}条未推送，暂时没有该液态的资源数据".format(sucess_count)

            return dict_result
        else:
            # mark 不存在时先推送mark 为 "",数据不够时再进行推送其他数据
            dict_result = self.data_second_iduge(count, liquid_name)
            return dict_result

    def data_allot(self,data_count,count):
        """
        计算推送数据的资源比列
        :param data_count: 需要推送的总数
        :param count: 多少种类规则

        :return:arevage 根据给定的资源的多少类平均每类需要取出的数量
        :return:residue 推送数据中缺失的数据条数
        """
        try:
            # 1. 先根据资源的等级计算出平均的一个比例
            arevage = int(abs(data_count/count))

            # 2.根据平均值的绝对值计算缺少的数据
            residue = data_count - (int(arevage*count))

            return arevage,residue
        except Exception as E:
            current_app.logger.info(E)

    def get_count_and_result(self,arevage,liquid_name=None,grade=None):
        """
        根据指定的规则获取对应的数据
        :param grade : 规则
        :param arevage :  比例

        :return: rema_count : 剩余数量
        :return: data_sucess : 取出的结果
        """
        try:

            if liquid_name:
                data_count = com_reserve.find({"push": "0", "mark":str(liquid_name)}).count()
                if (data_count-arevage) >= 0:
                    rema_count = 0
                else:
                    rema_count = arevage - data_count
            else:
                data_count = com_reserve.find({"push": "0", "mark": {"$in": grade}}).count()
                if (data_count-arevage) >= 0:
                    rema_count = 0
                else:
                    rema_count = arevage - data_count


            return rema_count
        except Exception as e:
             current_app.logger.info(e)

    def three_sucess_data_handler(self,three_grade,liquid_name,sucess_count):
        """

        :param three_grade: 规则
        :param sucess_count: 未推送的数量
        :param liquid_name: 液态名
        :return:
        """
        try:
            three_result = com_reserve.find({"push": "0", "tel_check": "实号", "mark": ""})
            dict_lt = []
            for _ in three_result:
                tag = 0
                sucess_data = {}
                for y in three_grade:
                    if re.search(y, _["companyName"]):
                        tag = 1
                        break
                if tag == 1:
                    code = self.liquid_names[liquid_name]
                    sucess_data = self.data_save(sucess_data=sucess_data, data=_, code_name=code,
                                                 liquid_name=liquid_name)
                    dict_lt.append(sucess_data)
                    sucess_count -= 1
                if sucess_count <= 0:
                    break
            return dict_lt,sucess_count

        except Exception as e:
            current_app.logger.info(e)


    def zc_data(self,liquid_name,count,arevage,residue=0,first_grade=None,second_grade=None,three_grade=None):
        """
        数据处理规则,目前知产规则最多
        :param  liquid_name : 推送的液态名
        :param  count ： 推送的总数
        :param  arevage ： 平均每级资源的比列
        :param  residue ： 缺失值，默认为0
        :param  first_grade ： 一级规则
        :param  second_grade ： 二级规则
        :param  three_grade ： 三级规则
        :return:
        """
        try:
            push_count = int(count)
            if liquid_name:

                # 1. 判断mark未液态名的数据是否够直接取完所有的推送数据
                rema_count = self.get_count_and_result(arevage=arevage, liquid_name=liquid_name)
                if rema_count == 0:
                    result = com_reserve.find({"push": "0","tel_check" : "实号", "mark":str(liquid_name)}).limit(arevage)

                else:
                    result = com_reserve.find({"push": "0","tel_check" : "实号", "mark": str(liquid_name)})
                    residue_count = residue + rema_count
                    arev, residue = self.data_allot(data_count=residue_count, count=3)
                    arevage += arev

                sucesslt,sucess_count = self.data_mark_none(count=push_count,result_num=result,liquid_name=liquid_name)

                #2. 判断是否有一级规则
                if first_grade:
                    rema_count = self.get_count_and_result(arevage=arevage,grade=first_grade)
                    if rema_count == 0:
                        first_result = com_reserve.find({"push": "0", "tel_check" : "实号","mark": {"$in":first_grade}}).limit(arevage)
                    else:
                        first_result = com_reserve.find({"push": "0", "tel_check" : "实号","mark": {"$in": first_grade}})
                        residue_count = residue + rema_count
                        arev, residue = self.data_allot(data_count=residue_count, count=2)
                        arevage += arev
                    dict_lt,sucess_count = self.data_mark_none(count=sucess_count,result_num=first_result,liquid_name=liquid_name)
                    sucesslt += dict_lt

                # 2. 判断是否有二级规则
                if second_grade:
                    rema_count = self.get_count_and_result(arevage=arevage,grade=second_grade)
                    if rema_count == 0:
                        second_result = com_reserve.find({"push": "0", "tel_check" : "实号", "mark": {"$in":second_grade}}).limit(arevage)
                    else:
                        second_result = com_reserve.find({"push": "0", "tel_check" : "实号", "mark": {"$in": second_grade}})
                        residue_count = residue + rema_count
                        arev, residue = self.data_allot(data_count=residue_count, count=1)
                        arevage += arev
                        arevage += residue
                    dict_lt, sucess_count = self.data_mark_none(count=sucess_count, result_num=second_result,liquid_name=liquid_name)
                    sucesslt += dict_lt

                # 2. 判断是否有三级规则
                if three_grade:
                    three_count = com_reserve.find({"push": "0", "tel_check": "实号", "mark": ""}).count()
                    if (three_count - arevage) >= 0:
                        dict_lt,sucess_count = self.three_sucess_data_handler(three_grade=three_grade,sucess_count=sucess_count,liquid_name=liquid_name)
                    else:
                        three_result = com_reserve.find({"push": "0", "tel_check": "实号", "mark": ""})
                        dict_lt = []
                        for _ in three_result:
                            tag = 0
                            sucess_data = {}
                            for y in three_grade:
                                if re.search(y, _["companyName"]):
                                    tag = 1
                                    break
                            if tag == 1:
                                code = self.liquid_names[liquid_name]
                                sucess_data = self.data_save(sucess_data=sucess_data, data=_, code_name=code,
                                                             liquid_name=liquid_name)
                                dict_lt.append(sucess_data)
                                sucess_count -= 1
                            if sucess_count <= 0:
                                break
                    sucesslt += dict_lt

                # 2. 所有的数据平均分配完毕后是否有剩余未推送的数据,有的话从新获取
                if sucess_count >0:

                    if com_reserve.find({"push":"0","tel_check":"实号","mark":liquid_name}).count() > sucess_count:
                        result = com_reserve.find({"push": "0", "tel_check": "实号", "mark": str(liquid_name)}).limit(sucess_count)
                        dict_lt, sucess_count = self.data_mark_none(count=sucess_count, result_num=result,liquid_name=liquid_name)
                        sucesslt += dict_lt

                    if three_grade and sucess_count>0:
                        three_count = com_reserve.find({"push": "0", "tel_check": "实号", "mark": ""}).count()
                        if (three_count - sucess_count) >= 0:
                            dict_lt,sucess_count = self.three_sucess_data_handler(three_grade=three_grade,liquid_name=liquid_name,sucess_count=sucess_count)
                            sucesslt += dict_lt

                    if second_grade and sucess_count>0:
                        second_count = com_reserve.find({"push": "0", "tel_check": "实号", "mark":{"$in":second_grade}}).count()
                        if (second_count - sucess_count) > 0:
                            second_result = com_reserve.find({"push": "0", "tel_check": "实号", "mark": {"$in": second_grade}}).limit(sucess_count)
                            dict_lt, sucess_count = self.data_mark_none(count=sucess_count, result_num=second_result,liquid_name=liquid_name)
                            sucesslt += dict_lt

                    if first_grade and sucess_count>0:
                        first_count = com_reserve.find({"push": "0", "tel_check": "实号", "mark": {"$in": first_grade}}).count()
                        if (first_count - sucess_count) > 0:
                            second_result = com_reserve.find({"push": "0", "tel_check": "实号", "mark": {"$in": first_grade}}).limit(sucess_count)
                            dict_lt, sucess_count = self.data_mark_none(count=first_count, result_num=second_result,liquid_name=liquid_name)
                            sucesslt += dict_lt
                    else:
                        if sucess_count > 0:
                            res_count = com_reserve.find({"push": "0", "mark":str(liquid_name)}).count()
                            if (res_count - sucess_count) > 0:
                                result = com_reserve.find({"push": "0", "tel_check": "实号", "mark":str(liquid_name)}).limit(sucess_count)
                                dict_lt, sucess_count = self.data_mark_none(count=res_count, result_num=result,liquid_name=liquid_name)
                                sucesslt += dict_lt

                dict_result = {}
                dict_result["SucessResult"] = sucesslt
                dict_result["msg"] = "数据补充{}条".format((count - sucess_count))
                if sucess_count > 0:
                    dict_result["Not_push_msg"] = "数据剩余{}条未推送，暂时没有该液态的资源数据".format(sucess_count)
                return dict_result

            # 根据判断规则取出对应的数据，并切把不足的数据
        except Exception as e:
            current_app.logger.info(e)


    def data_handle(self,liquid_name,result_count):
        """
        从 reserve 取出状态为0并且tel_check为10号的数据进行清洗并推送
        :return:
        :param liquid_name : 要推送的液态
        :param result_count :  要推送的数量
        """
        liquid_name = str(liquid_name)
        count = int(result_count)
        result = com_reserve.find({"push": "0", "tel_check": "实号"})
        # dict_result = {}
        if liquid_name == "工商":
            dict_result = self.data_first_iduge(count,liquid_name)
            dict_result["liquid_name"] = liquid_name
            return dict_result
        elif liquid_name == "融资":
            # 融资液态数据推送的是个人数据

            # dict_result["code"] = 201
            return "rz"
        elif liquid_name == "知产":
            arevage,residue = self.data_allot(data_count=count,count=4)
            first_grade = ["有商标", "有专利", "有软件著作权", "有作者著作权"]
            second_grade = ["科技类", "信息技术类"]
            three_grade = ["技术", "科技"]
            dict_result = self.zc_data(liquid_name=liquid_name,count=count,arevage=arevage,residue=residue,
                         first_grade=first_grade,second_grade=second_grade,three_grade=three_grade)

            dict_result["liquid_name"] = liquid_name
            return dict_result
        elif liquid_name == "资质":
            arevage, residue = self.data_allot(data_count=count, count=3)
            first_grade = ["建筑类","建筑类型"]
            three_grade = ["建筑", "装修","装饰","工程"]
            dict_result = self.zc_data(liquid_name=liquid_name, count=count, arevage=arevage, residue=residue,
                                       first_grade=first_grade,three_grade=three_grade)
            return dict_result

        elif liquid_name == "法律":
            dict_result = self.data_first_iduge(count, liquid_name)
            dict_result["liquid_name"] = liquid_name
            return dict_result

        elif liquid_name == "综合":
            arevage, residue = self.data_allot(data_count=count, count=3)
            first_grade = ["科技类", "信息技术类"]
            three_grade = ["技术", "科技"]
            dict_result = self.zc_data(liquid_name=liquid_name, count=count, arevage=arevage, residue=residue,
                                       first_grade=first_grade,three_grade=three_grade)
            return dict_result

        elif liquid_name == "互联网":
            arevage, residue = self.data_allot(data_count=count, count=3)
            first_grade = ["科技类", "信息技术类"]
            three_grade = ["技术", "科技"]
            dict_result = self.zc_data(liquid_name=liquid_name, count=count, arevage=arevage, residue=residue,
                                       first_grade=first_grade,three_grade=three_grade)
            return dict_result

        # elif liquid_name == "人事外包":
        #     pass


if __name__ == '__main__':
    start = Data_push()
    liquid_name = "资质"
    result_count = 1000

    start.data_handle(liquid_name,result_count)
    # start.data_allot(939,4)
