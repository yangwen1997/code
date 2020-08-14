'''
@author yangwenlong
@iter 商标局数据解析
'''
import re
from sbj.common import scjd_DB ,yyjd_DB ,sbps_DB,red_cli

class sbj_xpath(object):

    def __init__(self):
        # self.dict redis缓存字典 ，self.xpath_dict 解析字典
        self.dict = {
            "商标注册审查决定文书":(scjd_DB,"scjd_redis"),
            "商标异议决定文书":(yyjd_DB,"yyjd_redis"),
            "商标评审裁定/决定文书":(sbps_DB,"sbps_redis"),
        }

        self.xpath_dict = {
            "商标注册审查决定文书": [scjd_DB,'申请人：(.*?)</font>',
                           '>委托代理人：(.*?)</font>',"scjd_redis"
                           ],
            "商标异议决定文书": [yyjd_DB,'200%;">异议人：(.*?)<br>',
                         '<br>委托代理人：(.*?)<br>',
                         '<br>被异议人：(.*?)<br>',"yyjd_redis"
                         ],
            "商标评审裁定/决定文书": [sbps_DB, '>申请人：(.*?)<br>',
                            '委托代理人：(.*?)<br>',
                            '被申请人：(.*?)<br>',"凑数","sbps_redis"
                            ],

        }

    def xpath_html(self,htmlinfo,regex):
        """

        :param htmlinfo: DOM文档
        :param regex: 匹配规则
        :return:
        """

        import re
        resp = re.findall(regex, htmlinfo)
        if len(resp) > 1:
            return resp
        else:
            return "".join(resp)

    def to_redis(self,cateName):
        """取数据存入redis
        redisName :  redis的名字
        """
        DB,redisName = self.dict[cateName]

        result = DB.find({"flag":"1"})

        print("开始导入数据库数据到redis进行缓存，不再打印节省资源")
        [ red_cli.sadd(redisName,str(_)) for _ in result]
        count = red_cli.scard(redisName)
        print(f"总计：存入{redisName}缓存数据库中{count}条数据")

    def proce_main(self,cateName):
        """
        进程开始
        :return:
        """
        try:
            #  mongodb, xpath, redis名称，总数
            MONGO_DB = self.xpath_dict[cateName][0]
            datelt = self.xpath_dict[cateName]
            del datelt[0]
            redisName = datelt.pop(-1)
            count = red_cli.scard(redisName)

            # 批量处理数据
            while count:
                result = red_cli.srandmember(redisName)
                item = eval(result)

                item["trademarkType"] = "商标" + item["datename"].split("商标")[1].replace("\xa0", "") if "商标" in item["datename"] else ""
                item["trademarkNum"] = "".join(re.findall(r'(\d+)', item["datename"]))
                if len(datelt) == 2:
                    # 商标注册审查决定文书
                    item["applicant"],item["agent"] = self.xpath_html(item["tag_text"],datelt[0]), self.xpath_html(item["tag_text"],datelt[1])
                elif len(datelt) == 3:
                    # 商标异议决定书
                    item["Objector"], item["Objected"] = self.xpath_html(item["tag_text"], datelt[0]),self.xpath_html(item["tag_text"], datelt[2])

                    resp_agent = self.xpath_html(item["tag_text"], datelt[1])

                    item["agent"] = resp_agent[0] if isinstance(resp_agent,list) and len(resp_agent)>=1 else resp_agent
                    item["agent_second"] = resp_agent[1] if isinstance(resp_agent,list) and len(resp_agent)>1 else ""

                elif len(datelt) == 4:
                    #商标评审文书

                    item["applicant"], item["the_respondent"] = self.xpath_html(item["tag_text"], datelt[0]),\
                                                                               self.xpath_html(item["tag_text"], datelt[2])

                    resp_agent = self.xpath_html(item["tag_text"], datelt[1])
                    item["agent"] = resp_agent[0] if isinstance(resp_agent,list) and len(resp_agent) >= 1 else resp_agent
                    item["agent_second"] = resp_agent[1] if isinstance(resp_agent,list) and len(resp_agent) > 1 else ""


                item["flag"] = "2"
                MONGO_DB.save(item)
                print(f"数据{item['_id']}解析完毕回写数据库修改状态flag :2")
                red_cli.srem(redisName,result)

                count -= 1
        except:
            print("程序异常，请检查")
            exit()


def work():
    start = sbj_xpath()
    start.proce_main("商标评审裁定/决定文书")

import threading
for i in range(10):
    t = threading.Thread(target=work)
    t.start()
    print("please wait!")