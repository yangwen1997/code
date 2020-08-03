import re
import hashlib
import pymongo
from cnocr import CnOcr


ocr = CnOcr()
from PIL import Image

DB = pymongo.MongoClient(host="10.2.1.121 ",port=17017)
transfer_notice_db = DB["trademark"]["renewal_notice"]


def ocr_img(img_path,imgName):
    img_dict = {
        "first_img": [r"E:\img\renewal_notice\ocr\first_img.jpg", (0, 0, 1110, 135)],
        "second_img": [r"E:\img\renewal_notice\ocr\second_img.jpg", (101, 137, 1083, 440)],
        "three_img": [r"E:\img\renewal_notice\ocr\three_img.jpg", (103, 420, 1103, 687)],
        "four_img": [r"E:\img\renewal_notice\ocr\four_img.jpg", (103, 687, 1097, 958)],
        "five_img": [r"E:\img\renewal_notice\ocr\five_img.jpg", (100, 958, 1094, 1225)],
        "six_img": [r"E:\img\renewal_notice\ocr\six_img.jpg", (100, 1225, 1094, 1490)],
    }

    img = Image.open(img_path)  # 读取图片
    img_lt = []

    for k, v in img_dict.items():
        path = v[0]

        imgs = img.crop(v[1])
        if imgs.mode == "P":
            imgs = imgs.convert('RGB')
        imgs.save(path)
        img_lt.append(path)

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
            res_dict["notice_category"] = result[0].strip("`")

        elif count == 3:
            # 块，注册号 ,id ,商标，类别，转让人，受让人
            res_dict["block"] = "1"
            res_dict["registration_number"] = result[0].split(":")[1].strip("`")
            _id = prefix + f"_{res_dict['registration_number'].strip('`')}"
            res_dict["_id"] = hashlib.md5( _id.encode('utf-8')).hexdigest()
            res_dict["trade"] = result[1].split(":")[1]
            res_dict["category"] = result[2].split(":")[1].strip("/这")

            try:
                res_dict["Registrant"] = result[3].split(":")[1].strip("这") + result[4]
            except:
                res_dict["Registrant"] = result[3].split(":")[1].strip("这")

        elif count == 4:
            # 块，注册号 ,id ,商标，类别，转让人，受让人
            res_dict["block"] = "2"
            res_dict["registration_number"] = result[0].split(":")[1].strip("Z")
            _id = prefix + f"_{res_dict['registration_number'].strip('`')}"
            res_dict["_id"] = hashlib.md5(_id.encode('utf-8')).hexdigest()
            res_dict["trade"] = result[1].split(":")[1].strip("ˇ,")
            res_dict["category"] = result[2].split(":")[1].strip("ˇ'")

            try:
                res_dict["Registrant"] = result[3].split(":")[1] + result[4]
            except:
                res_dict["Registrant"] = result[3].split(":")[1]

        elif count == 5:
            # 块，注册号 ,id ,商标，类别，转让人，受让人
            res_dict["block"] = "3"
            res_dict["registration_number"] = result[0].split(":")[1]
            _id = prefix + f"_{res_dict['registration_number'].strip('`')}"
            res_dict["_id"] = hashlib.md5(_id.encode('utf-8')).hexdigest()
            res_dict["trade"] = result[1].split(":")[1].strip("K")
            res_dict["category"] = result[2].split(":")[1].strip("/穴")

            try:
                res_dict["Registrant"] = result[3].split(":")[1] + result[4].strip("芦人%7")
            except:
                res_dict["Registrant"] = result[3].split(":")[1]

            res_dict["imgName"] = imgName

        elif count == 6:
            # 块，注册号 ,id ,商标，类别，转让人，受让人
            res_dict["block"] = "4"
            res_dict["registration_number"] = result[0].split(":")[1].strip("yZ《7")
            _id = prefix + f"_{res_dict['registration_number'].strip('`')}"
            res_dict["_id"] = hashlib.md5(_id.encode('utf-8')).hexdigest()
            res_dict["trade"] = result[1].split(":")[1].strip(">Zl")
            res_dict["category"] = result[2].split(":")[1].strip("/-2")

            try:
                res_dict["Registrant"] = result[3].split(":")[1].strip("(") + result[4]
            except:
                res_dict["Registrant"] = result[3].split(":")[1].strip("(")

            res_dict["imgName"] = imgName

    print(f"路径为：{img_path}的图片识别完毕")


import os
file_lt = os.listdir(r'E:\img\renewal_notice')

for _ in file_lt:
    if _ == "ocr":
        continue
    else:
        img_path = r"E:\img\renewal_notice\{}".format(_)
        print(img_path)
        imgName = _.split(".")[0]
        ocr_img(img_path,imgName)
