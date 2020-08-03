import re
import os
import hashlib
import pymongo
from cnocr import CnOcr


ocr = CnOcr()
from PIL import Image
# 爬虫Mongo 10.2.1.121 10.2.1.122 10.2.1.123   端口17017
DB = pymongo.MongoClient(host="10.2.1.121 ",port=17017)
transfer_notice_db = DB["trademark"]["trademark_registration_second"]



def ocr_img(img_path,imgName):
    img_dict = {
        "first_img": [r"E:\img\trademark_registration_second\ocr\first_img.jpg", (0, 0, 1110, 135)],
        "second_img": [r"E:\img\trademark_registration_second\ocr\second_img.jpg", (70, 132, 1110, 424)],
        "three_img": [r"E:\img\trademark_registration_second\ocr\three_img.jpg", (70, 424, 1110, 1108)],
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
            parents = re.findall(r"(\d+)",result[0]);stage = parents[0];year = parents[1]
            month = parents[2] if len(parents[2]) == 2 else "0" + parents[2]
            day = parents[3] if len(parents[3]) == 2 else "0" + parents[3]
            prefix = stage + "_" + year + "-" + month + "-" + day

        elif count == 2:
            # 获取图片的公告类别
            res_dict["notice_category"] = result[0].strip("*/足").strip("ˇ7")

        elif count == 3:
            # 块，注册号 ,id ,商标，类别，审查/审查决定  初审公告日期
            res_dict["block"] = "1"
            res_dict["registration_number"] = result[1].split(":")[1]
            _id = prefix + f"_{res_dict['registration_number']}"
            res_dict["_id"] = hashlib.md5( _id.encode('utf-8')).hexdigest()
            res_dict["trade"] = result[2].split(":")[1]
            res_dict["category"] = result[3].split(":")[1][:-2]
            res_dict["imgName"] = imgName

            res_dict["Registrant"] = result[4].split(":")[1].strip("-2")
            res_dict["examination"] = result[5].split(":")[1]
            res_dict["preliminary_notice"] = result[6].split(":")[1].strip("`S")
            try:
                res_dict["commodity"] = result[7].split(":")[1] +";" + result[8]
            except:
                res_dict["commodity"] = result[7].split(":")[1]
            # transfer_notice_db.save(res_dict)
            print(res_dict)

    print(f"路径为：{img_path}的图片识别完毕")



# 遍历文件夹下面所有的图片实现批量识别图片
file_lt = os.listdir(r'E:\img\trademark_registration_second')

for _ in file_lt:
    if _ == "ocr":
        continue
    else:
        img_path = r"E:\img\trademark_registration_second\{}".format(_)
        print(img_path)
        imgName = _.split(".")[0]
        ocr_img(img_path,imgName)

