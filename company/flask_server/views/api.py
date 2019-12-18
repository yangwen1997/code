import sys
import json

from flask import request
sys.path.extend([r'D:\bmd\bmd_server\src\company\flask_server'])
# from flask_server.bmd_celery.tasks import check_online_total,check_tel_total
from flask import Blueprint
import os

api = Blueprint("api",__name__)

from flask_server.common import get_log
from flask_server.process_.Reserve_total import check_reserve
from flask_server.process_.result_push import Data_push
from werkzeug.utils import secure_filename
from flask_server.process_.excel_push import read_excel,tel_handler
from flask import current_app



@api.route('/check_data',methods=["GET","POST"])
def check_online_total():
    try:

        userid = request.form.get("userid")
        start = check_reserve()

        # 1. 检测数据是否推送
        sucess_count,To_push,Not_push,push_lt = start.check_online_total()

        dict = {}
        if sucess_count == 0:
            dict["code"] = 200
            dict["msg"] = "暂时没有需要查询推送的数据"
            dict["push_lt"] = []
        else:
        # log.info(f"数据总数{sucess_count}推送状态查询完成")
            dict["code"] = 200
            dict["msg"] = f'推送状态查询完成,数据总数{sucess_count}，已经推送的数据总共有{To_push},还未推送的数据有{Not_push}'
            dict["push_lt"] = push_lt
            dict["sucess_count"] = sucess_count
            dict["To_push"] = To_push
            dict["Not_push"] = Not_push

        return json.dumps(dict)
    except Exception as e:
        current_app.logger.info(e)

@api.route('/check_tel',methods=["GET","POST"])
def check_tel_total():
    try:
        userid = request.form.get('userid')
        print(userid)

        start = check_reserve()
        # 2. 检测数据号码是否是实号
        sucessount,sucess_lt,totalCount,total_lt = start.check_tel_total()

        dict = {}
        dict["msg"] = f'已经检测{sucessount}条数据，还有{totalCount}条数据需要进行空号清洗。'
        dict["sucessount"] = sucessount
        dict["sucess_lt"] = sucess_lt
        dict["totalCount"] = totalCount
        dict["total_lt"] = total_lt

        return json.dumps(dict)
    except Exception as e:
        print(e)

@api.route('/data_push',methods=["GET","POST"])
def data_push():
    try:
        print("进入函数")
        liquid_name = request.form.get("liquid_name")
        result_count = request.form.get("liquid_count")
        # "http://127.0.0.1:8082/api/data_push?liquid_name=知产&liquid_count=1000"


        if liquid_name and result_count:
            start = Data_push()
            result_count = str(result_count).replace("'","")
            dict = start.data_handle(liquid_name,result_count)
            # print(d)
            dict["code"] = 200
            return json.dumps(dict)

        else:
            dict = {}
            dict["code"] = 503
            dict["errmsg"] = "参数错误"
        return json.dumps(dict)
    except Exception as e:
        current_app.logger.info(e)

@api.route("/file_update",methods=["GET","POST"],)
def file_update():
    """
    上传文件
    :return:
    """
    try:
        print("进入上传函数")
        # file = request.files.get('files')
        file = request.files.getlist('files')
        userid = request.form.get('userid')
        trade = request.form.get('trade')
        base_path = (os.path.abspath(os.path.dirname(__file__))).replace(r'views',"files")

        dict = {}
        if userid and file and trade:
            user_path = base_path + '\{}'.format(userid)
            if not os.path.exists(user_path):
                os.mkdir(user_path)
            for item in file:

                filename = user_path + r'\{}'.format(item.filename)
                if os.path.exists(filename):
                    os.remove(filename)
                item.save(filename)
            total,sucess,err = read_excel(user_id=userid,trade=trade)
            sucess_count = tel_handler()
            dict["code"] = 200
            dict["msg"] = '用户：{}上传的总数据为-{}，公司去重后成功存入的数据-{}，失败的数据-{},' \
                          '手机去重后的功存入的数据-{}'.format(userid,total,sucess,err,sucess_count)
            return json.dumps(dict)
        else:
            print("aaaa")
            return "error"
    except Exception as e:
        current_app.logger.info(e)


@api.route('/test',methods=["GET","POST"])
def tests():
    # from company.manage import app
    # current_app.logger.info("测试日志")
    s = check_reserve()
    s.test_add()
    return "sucess"
