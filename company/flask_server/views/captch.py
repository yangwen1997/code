from flask import Blueprint
from flask import current_app


import base64
import string
import random
from flask import Flask, request,json
import json
import pymysql
import hashlib
from PIL import Image, ImageFont, ImageDraw, ImageFilter

captch = Blueprint("captch",__name__)

def gene_text():
    """随机生成验证码"""
    source = list(string.ascii_letters + string.digits)
    captch_nummer = ""
    for index in range(0,4):
        captch_nummer += str(random.choice(source))
    return captch_nummer

@captch.route('/captch_touch',methods=["GET","POST"])
def captch_touch():
    # python生成验证码
    dict = {}

    try:
        result = gene_text()
        #  设置验证码的图片大小，创建图片并设置背景色为白色，创建字体为斜体，大小为25，创建画笔
        captch_result = result
        # 干扰线选取颜色
        Draw_color_lt = ["#BBFFFF", "#FFFAF0", "#FFF5EE", "#97FFFF", "#7FFF00", "#00BFFF",
                    "#98FB98", "#7FFF00", "#FFFF00", "#FFA500", "#FF69B4", "#EE82EE", "#FF6347", "#63B8FF"]
        # 字体随机选择颜色
        font_color_lt = ["#1C1C1C","#698B69","#483D8B","#8B6914","#8B3A3A","#CD0000","#00008B"]

        #  设置生成的图片的宽和高，设置背景色，设置字体和大小
        width, height = 150, 40
        image = Image.new("RGBA", (width, height), "#d9d6c3")
        font = ImageFont.truetype(font=r'D:\bmd\bmd_server\src\company\flask_server\captch\font\qihei55.ttf', size=25)

        # 创建画布
        draw = ImageDraw.Draw(image)

        # (width - font_width) / 2, 控制字体在图片中的X轴距离
        # (width - font_height) / 16 控制字体在图片中的Y轴距离
        # result 字体 fill 字体在图片中的颜色，这里从定义的色表中随机选取
        font_width, font_height = font.getsize(result)
        draw.text(((width - font_width) / 2, (width - font_height) / 16,), result, font=font,
                  fill=str(random.choice(font_color_lt)))

        #  循环10次添加10个干扰线，begin 干扰线的起点，end干扰线的终点
        #  draw.line 向画布中画干扰线 fill 干扰线的颜色，每次都随机选取
        for _ in range(0, 10):
            begin = (random.randint(0, width), random.randint(0, height))

            end = (random.randint(0, width), random.randint(0, height))

            draw.line([begin, end], fill=str(random.choice(Draw_color_lt)))
        # 保存图片
        image.save(r'D:\bmd\bmd_server\src\company\flask_server\captch\img\test.png')  # 保存验证码图片
        with open(r'D:\bmd\bmd_server\src\company\flask_server\captch\img\test.png', 'rb') as img_f:
            img_stream = img_f.read()
            img_stream = base64.b64encode(img_stream)
        dict["code"] = 200
        dict["captch_stream"] = "data:;base64," + str(img_stream).strip("b").replace("'","")
        dict["captch"] = result
        print(img_stream)
        return json.dumps(dict)
        # return img_stream

    except Exception as e:
        print(e)
    else:
        errdict = {}
        errdict["err_msg"] = "undefined"
        return errdict
