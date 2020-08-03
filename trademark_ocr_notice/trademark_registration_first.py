import re
import hashlib
import pymongo
from cnocr import CnOcr


ocr = CnOcr()
from PIL import Image
# 爬虫Mongo 10.2.1.121 10.2.1.122 10.2.1.123   端口17017
DB = pymongo.MongoClient(host="10.2.1.121 ",port=17017)
transfer_notice_db = DB["trademark"]["trademark_registration_first"]



def ocr_img(img_path,imgName):
    img_dict = {
        "first_img": [r"E:\img\trademark_registration_first\ocr\first_img.jpg", (0, 0, 1110, 135)],
        "second_img": [r"E:\img\trademark_registration_first\ocr\second_img.jpg", (70, 132, 1110, 424)],
        "three_img": [r"E:\img\trademark_registration_first\ocr\three_img.jpg", (70, 424, 1110, 770)],
        "four_img": [r"E:\img\trademark_registration_first\ocr\four_img.jpg", (70, 770, 1110, 1120)],
        "five_img": [r"E:\img\trademark_registration_first\ocr\five_img.jpg", (70, 1120, 1110, 1480)],
    }

    img = Image.open(img_path)   # 读取图片
    # box = (0,0,1110,135)   # 设定要剪切的位置
    img_lt = []
    for k,v in img_dict.items():
        path = v[0]

        imgs = img.crop(v[1])
        if imgs.mode == "P":
            imgs = imgs.convert('RGB')
        imgs.save(path)
        img_lt.append(path)

    # result_lt = []
    count = 0
    res_dict = {}
    prefix = ""
    for _ in img_lt:
        res = ocr.ocr(_)
        result = ["".join(_) for _ in res]
        count += 1
        if count == 1:
            # 识别第一块并取出 期号，年，月，日，标题字段信息,一行写多个逻辑用分号（；）进行分割
            parents = re.findall(r"(\d+)", result[0])
            stage = parents[0]
            year = parents[1]
            month = parents[2] if len(parents[2]) == 2 else "0" + parents[2]
            day = parents[3] if len(parents[3]) == 2 else "0" + parents[3]
            prefix = stage + "_" + year + "-" + month + "-" + day

        elif count == 2:
            # 获取图片的公告类别
            res_dict["notice_category"] = result[0]

        elif count == 3:
            # 块，注册号 ,id ,商标，类别，转让人，受让人
            res_dict["block"] = "1"
            res_dict["registration_number"] = result[0].split(":")[1]
            _id = prefix + f"_{res_dict['registration_number']}"
            res_dict["_id"] = hashlib.md5( _id.encode('utf-8')).hexdigest()
            res_dict["trade"] = result[1][0:-2].split(":")[1]
            res_dict["category"] = result[2].split(":")[1][:-2]
            res_dict["imgName"] = imgName
            try:
                res_dict["Registrant"] = result[3].split(":")[1].strip("〉").strip("Z>")+ result[4]
            except:
                res_dict["Registrant"] = result[3].split(":")[1].strip("〉").strip("Z>")
            # transfer_notice_db.save(res_dict)
            print(res_dict)
        elif count == 4:
            # 块，注册号 ,id ,商标，类别，转让人，受让人
            res_dict["block"] = "2"
            res_dict["registration_number"] = result[0].split(":")[1].replace("<K<e","")
            _id = prefix + f"_{result[0].split(':')[1]}"
            res_dict["_id"] = hashlib.md5(_id.encode('utf-8')).hexdigest()
            tr = result[1].split(":")[1]
            res_dict["trade"] = tr.replace("、","") if "、" == tr[-1] else tr
            res_dict["category"] = result[2].split(":")[1]
            res_dict["imgName"] = imgName
            try:
                res_dict["Registrant"] = (result[3].split(":")[1] + result[4])
            except:
                res_dict["Registrant"] = result[3].split(":")[1]
                # transfer_notice_db.save(res_dict)
            print(res_dict)
        elif count == 5:
            # 块，注册号 ,id ,商标，类别，转让人，受让人
            res_dict["block"] = "3"
            res_dict["registration_number"] = result[0].split(":")[1].replace("人%s&","")
            _id = prefix + f"_{result[0].split(':')[1]}"
            res_dict["_id"] = hashlib.md5(_id.encode('utf-8')).hexdigest()
            res_dict["trade"] = result[1].split(":")[1].replace("Y入","")
            res_dict["category"] = result[2].split(":")[1][0:-2]
            res_dict["imgName"] = imgName
            try:
                res_dict["Registrant"] = result[3].split(":")[1] + result[4]
            except:
                res_dict["Registrant"] = result[3].split(":")[1]
            print(res_dict)

            # transfer_notice_db.save(res_dict)

    print(f"路径为：{img_path}的图片识别完毕")



# 遍历文件夹下面所有的图片实现批量识别图片
import os
file_lt = os.listdir(r'E:\img\trademark_registration_first')

for _ in file_lt:
    if _ == "ocr":
        continue
    else:
        img_path = r"E:\img\trademark_registration_first\{}".format(_)
        print(img_path)
        imgName = _.split(".")[0]
        ocr_img(img_path,imgName)
