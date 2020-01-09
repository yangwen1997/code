# from flask_server.common import com_reserve
# #
# #
# # # RESULT = com_reserve.find({}).skip(752)
# RESULT = com_reserve.find({})
# # # RESULT = com_reserve.find({"push": "0","tel_check" : "实号", "mark":"知产"}).limit(250)
# # # RESULT = com_reserve.find({}).limit(100).skip(100)
# COUNT = 0
# for _ in RESULT:
# #     # _["mark"] = "资质"
# #     # _["push"] = "0"
# #     # del _["push"]
#     _["tel_check"] = "实号"
#     id = _["_id"]
#     com_reserve.update({"_id":id},_)
# #     COUNT += 1
# print(COUNT)


# import pymongo
#
# DB = pymongo.MongoClient("mongodb://rwuser:48bb67d7996f327b@10.2.1.216:57017,10.2.1.217:57017,10.2.1.218:57017")
# xs_com_reserve = DB['BMD']["Reserve_total"]
#
# DBB = pymongo.MongoClient(host="127.0.0.1",port=27017)
# com_reserve = DBB['BMD']["Reserve_total"]
#
# result = xs_com_reserve.find({})
# com_reserve.insert(result)


# import requests
# import json
# s = requests.session()
# s.headers.update({
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
# })
#
# url = "http://172.16.74.178:8082/captch/captch_touch"
# res = s.post(url)
# # print(json.loads(res.text()))
# print(res.text)


# from PIL import Image
#
# image = Image.open(r'G:\VUE\vue_learn\vueL\src\assets\img\加载.gif')
# w,h = image.size
# scale = 2
# NEW = image.resize((int(w/scale),int(h/scale)), Image.ANTIALIAS)
# NEW.save(r'G:\VUE\vue_learn\vueL\src\assets\img\a.gif')
# NEW.close()


# file_text = r'D:\bmd\bmd_server\src\company\flask_server\files\102888\TEL\102888.txt'
# with open(file_text,"r",encoding='utf-8') as fp:
#     linse = fp.readlines()
#     print(len(linse))

# import requests
# s = requests.session()
# s.headers.update({
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
# })
#
# data = {
#     "userid":"102888",
# }
# file = {"files":open(file_text,"rb")}
# res = s.post("http://127.0.0.1:8082/tel/checkTel",data,files=file)
# res.encoding = "utf-8"
# print(res.text)

# import hashlib
# import time
# from common import sendID
#
# # dict = {}
# # dict["sendid"] = "0300"
# # dict["user"] = "102888"
# # dict["_id"] = hashlib.md5(str(dict["sendid"]).encode('utf-8')).hexdigest()
# # dict["time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
# # dict["local_time"] = str(int(time.time() * 1000))
# # sendID.insert(dict)
#
# # result = sendID.find()
# # lt = []
# # for i in result:
# #     a = (i["_id"],i["local_time"])
# #     lt.append(a)
# # print(lt)
# # def takeSecond(elm):
# #     return elm[1]
# # lt.sort(key=takeSecond)
# # print(lt)
# # print(lt[-1][0])
#
# import requests
# s = requests.session()
#
# a = s.get('http://127.0.0.1:8083/a/')
# a.encoding = 'utf-8'
# print(a.json())
import requests
s = requests.session()

file_path = r"D:\bmd\bmd_server\src\company\flask_server\files\102888\TEL\待检测号码.txt"
file = {"files": open(file_path, "rb")}
rep = s.get("http://127.0.0.1:8082/tel/test",files=file)
print(rep.text)
