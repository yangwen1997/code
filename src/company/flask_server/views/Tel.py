import os
import sys
import json
from flask import Blueprint,current_app,request,send_from_directory,send_file
from process_.check_tel import CheckTel
from common import com_reserve
import requests

tel = Blueprint('Tel',__name__)

# 空号检测


@tel.route('/checkTel',methods=["GET","POST"])
def checkTel():
    """
    空号检测，通用上传文件
    :return:dict :json 数据
    :return:dict[""code] :状态码
    :return:dict["msg"] : 消息
    :return:dict["TextMsg"] : txt消息
    """
    dict = {}
    try:
        dict["code"] = 200
        userid = request.form.get("userid")
        file = request.files.get("files")
        if userid and file:

            userid_path = r'D:\bmd\bmd_server\src\company\flask_server\files\{}'.format(userid)
            if os.path.exists(userid_path):
                tel_file_path = userid_path + '\TEL'
                if os.path.exists(tel_file_path):
                    pass
                else:
                    os.mkdir(tel_file_path)
            else:
                tel_file_path = userid_path + '\TEL'
                os.makedirs(tel_file_path)
            tel_file_txt = tel_file_path + r'\{}.txt'.format(userid)
            if os.path.exists(tel_file_txt):
                os.remove(tel_file_txt)
            file.save(tel_file_txt)
            with open(tel_file_txt)as fp:
                linse = fp.readlines()
                if len(linse) < 3000:
                    dict["TextMsg"] = "只支持3000条以上的批量清洗,当前文本中传入的手机号为{}条".format(len(linse))
            Start = CheckTel(userid)
            # Start.check_tel()
        else:
            dict["msg"] = "请传入正确的文件或者用户"
    except Exception as e:
        dict["code"] = 403
        dict["msg"] = "error"
        current_app.log.info(e)
    return json.dumps(dict)


@tel.route('/download',methods=["GET","POST"])
def download():
    try:
        return send_file(r'D:\bmd\bmd_server\src\company\flask_server\files\102888\TEL\102888.txt',mimetype='text/csv',
                         attachment_filename="down.txt",as_attachment=True)

    except Exception as E:
        current_app.log.info("下载失败")

@tel.route('/createTxt',methods=["GET","POST"])
def create_txt():
    """
    生成文本信息
    :return:
    """
    try:
        userid = request.form.get("userid")
        STA = CheckTel(userid)
        dict = STA.check_before()
        dict["code"] = 200
        return json.dumps(dict)
    except Exception as e:
        dict = {}
        dict["code"] = 505
        dict["msg"] = "出现异常"
        current_app.log.info(e)

@tel.route('/searchCount',methods=["GET","POST"])
def search_count():
    """
    查询没有清洗的数据总数
    :return:
    """
    dict = {}
    try:
        count = com_reserve.find({"push":"0","tel_check":"待检测"}).count()
        dict["code"] = 200
        dict["msg"] = f"可以清洗的数据总数有{count}条"
    except Exception as e:
        dict["code"] = 505
        dict["msg"] = "查询数据异常"
        current_app.log.info(e)

    return json.dumps(dict)

@tel.route('/update_api',methods=["GET","POST"])
def upapi():
    """
    请求付费的上传接口
    :return:
    """
    dict = {}
    try:
        userid = request.form.get("userid")
        STR = CheckTel(userid)
        SENDID = STR.updefile()
        if SENDID:
            dict["code"] = 200
            dict["msg"] = "sucess"
            dict["sendID"] = SENDID
        else:
            dict["code"] = 201
            dict["msg"] = "接口请求失败"
        return json.dumps(dict)

    except Exception as e:
        current_app.log.info(e)

@tel.route('/search_api',methods=["GET","POST"])
def search_api():
    """
    查询接口
    :return:
    """
    try:
        userid = request.form.get("userid")
        sendid = request.form.get("sendid")
        STR = CheckTel(userid)
        dicts = STR.search_api(sendid)
        dict = {}
        dict["real"] = dicts["活跃号数量"]
        dict["empty"] = dicts["空号数量"]
        dict["silence"] = dicts["沉默号数量"]
        dict["risk"] = dicts["风险号数量"]

        return json.dumps(dict)
    except Exception as e:
        current_app.log.info(e)

@tel.route('/down_api',methods=["GET","POST"])
def down_api():
    """
    发送请求下载压缩包
    :return:
    """
    try:
        userid = request.form.get("userid")
        sendid = request.form.get("sendid")

        STR = CheckTel(userid)
        TAG = STR.down_api(sendid)
        TAG = True
        if TAG:
            STR.check_after()
            count = com_reserve.find({"push":"0","tel_check":"实号"}).count()
            dict = {}
            dict["code"] = 200
            dict["msg"] = f"可以推送的数据总数有{count}条"
            return json.dumps(dict)
    except Exception as e:
        current_app(e)
