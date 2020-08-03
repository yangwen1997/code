import re
import hashlib
import pymongo
from cnocr import CnOcr


ocr = CnOcr()
from PIL import Image

DB = pymongo.MongoClient(host="10.2.1.121 ",port=17017)
transfer_notice_db = DB["trademark"]["Trademark_trial"]

def ocr_img(img_path,imgName):
    img_dict = {
        "first_img": [r"E:\img\Trademark_trial\ocr\first_img.jpg", (0, 0, 1110, 120)],
        "second_img": [r"E:\img\Trademark_trial\ocr\second_img.jpg", (101, 120, 1083, 338)],
        "three_img": [r"E:\img\Trademark_trial\ocr\three_img.jpg", (103, 339, 1103, 423)],
        "four_img": [r"E:\img\Trademark_trial\ocr\four_img.jpg", (103, 795, 1097, 990)],
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
            res_dict["notice_category"] = result[0].strip("/玄")

        elif count == 3:
            # 块，注册号
            # res_dict["block"] = "1"
            res_dict["registration_number"] = re.findall(r'(\d+)',result[0])[0]
            _id = prefix + f"_{res_dict['registration_number'].strip('`')}"
            res_dict["_id"] = hashlib.md5(_id.encode('utf-8')).hexdigest()

        elif count == 4:
        #     # 块，注册号 ,id ,商标，类别，转让人，受让人

            if "址" in result[1] and "理机构" in result[2]:
                res_dict["registrant"] = result[0][3:]
                res_dict["addr"] = result[1][2:]
                res_dict["Agency"] = result[2][4:]
                try:
                    res_dict["ServiceItems"] = result[4].split(":")[1] + result[5]
                except:
                    res_dict["ServiceItems"] = result[4].split(":")[1]

            elif "址" in result[1] and "理机构" not in result[2]:
                res_dict["registrant"] = result[0][3:]
                res_dict["addr"] = result[1][2:] + result[2]
                res_dict["Agency"] = result[3][4:]
                try:
                    res_dict["ServiceItems"] = result[5].split(":")[1] + result[6]
                except:
                    res_dict["ServiceItems"] = result[5].split(":")[1]

            elif "址" not in result[1] and "理机构" in result[2]:
                res_dict["registrant"] = result[0][3:] + result[1]
                res_dict["addr"] = result[2][2:]
                res_dict["Agency"] = result[3][4:]


                try:
                    res_dict["ServiceItems"] = result[5].split(":")[1] + result[6]
                except:
                    res_dict["ServiceItems"] = result[5].split(":")[1]


            elif "址" not in result[1] and "理机构" not in result[2]:
                res_dict["registrant"] = result[0][3:] + result[1]
                res_dict["addr"] = result[2][2:] +  result[3]
                res_dict["Agency"] = result[4][4:]

                try:
                    res_dict["ServiceItems"] = result[6].split(":")[1] +  result[7]
                except:
                    res_dict["ServiceItems"] = result[6].split(":")[1]

        # elif count == 5:
        #     # 块，注册号 ,id ,商标，类别，转让人，受让人
        #     res_dict["block"] = "3"
        #     res_dict["registration_number"] = result[0].split(":")[1][:-1]
        #     _id = prefix + f"_{res_dict['registration_number'].strip('`')}"
        #     res_dict["_id"] = hashlib.md5(_id.encode('utf-8')).hexdigest()
        #     res_dict["trade"] = result[1].split(":")[1].strip("尽")
        #     res_dict["category"] = result[2].split(":")[1].strip("ˇ亏<")
        #
        #     res_dict["registrant"] = result[3].split(":")[1].strip("人/s&")
        #
        #     res_dict["Lost_card_number"] = result[4].split(":")[1]
        #
        #
        # elif count == 6:
        #     # 块，注册号 ,id ,商标，类别，转让人，受让人
        #     res_dict["block"] = "4"
        #     res_dict["registration_number"] = result[0].split(":")[1].strip("人")
        #     _id = prefix + f"_{res_dict['registration_number'].strip('`')}"
        #     res_dict["_id"] = hashlib.md5(_id.encode('utf-8')).hexdigest()
        #     res_dict["trade"] = result[1].split(":")[1].strip("`7'人")
        #     res_dict["category"] = result[2].split("类别")[1].strip(";>X为")
        #     res_dict["registrant"] = result[3].split(":")[1].strip("人/s&")
        #
        #     res_dict["Lost_card_number"] = result[4].split(":")[1].strip("<父")

        # res_dict["imgName"] = imgName

# 遍历文件夹下面所有的图片实现批量识别图片

import os
file_lt = os.listdir(r'E:\img\Trademark_trial')

for _ in file_lt:
    if _ == "ocr":
        continue
    else:
        img_path = r"E:\img\Trademark_trial\{}".format(_)
        print(img_path)
        imgName = _.split(".")[0]
        ocr_img(img_path,imgName)
