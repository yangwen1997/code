'''
@author : yangwenlong
@file : img_patterns
@intr : 图片规则匹配
@time : 2020/8/10
'''

import os,shutil,pymongo

MONGO = pymongo.MongoClient(host="172.16.74.249",port=27017)

def main():
    """程序入口"""
    base_path = r"D:\Img"
    # base_path = r"E:\code\spider_manage\backend\backend\apps"
    filesLt = os.listdir(base_path)

    for _ in filesLt:

        # 根据期数 拼接数据库地址 数据库对象 图片文件夹地址
        SB_DB = "GongGao" + str(_)
        imgs_path = base_path + r"\{}".format(str(_))
        imgs_files = os.listdir(imgs_path)
        MONGO_DB = MONGO["ShangB"][SB_DB]

        # 循环每张图片进行反查
        for img in imgs_files:
            regNum = img.split("_")[1]

            if "." in img:
                annTypeCode = img.split("_")[-1].strip(".jpg")
                result = MONGO_DB.find_one({"regNum":regNum,"annTypeCode" : annTypeCode})
                tradecategory = result["annType"]

                # 根据类型拼接路径
                end_path = imgs_path + r"\{}".format(str(tradecategory)).replace("/","_")
                if os.path.exists(end_path):
                    pass
                else:
                    os.mkdir(end_path)

                img_ord_path = imgs_path + r"\{}".format(img)
                img_new_path = end_path + r"\{}".format(img)
                shutil.move(img_ord_path,img_new_path)

                print(f"图片{img}移动至{img_new_path}")


    print(filesLt)

if __name__ == '__main__':
    main()