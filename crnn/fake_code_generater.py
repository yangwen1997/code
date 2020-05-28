import sys
import os
import shutil
import random
import time
from captcha.image import ImageCaptcha
import string
import numpy as np

# 用于生成验证码的字符集
CHAR_SET = list(string.digits)+list(string.ascii_lowercase)
# 字符集的长度
CHAR_SET_LEN = len(CHAR_SET)
# 验证码的长度，每个验证码由4个数字组成
CAPTCHA_LEN = 4

# 验证码图片的存放路径
CAPTCHA_IMAGE_PATH = 'images/'

# 用于模型测试的验证码图片的个数，从生成的验证码图片中取出来放入测试集中
TEST_IMAGE_NUMBER = 100


# 生成验证码图片，4位的十进制数字可以有10000种验证码
def generate_captcha_image(charSet=CHAR_SET, charSetLen=CHAR_SET_LEN, captchaImgPath=CAPTCHA_IMAGE_PATH):

    for k in range(3000):
        a = np.random.randint(0, CHAR_SET_LEN)
        b = np.random.randint(0, CHAR_SET_LEN)
        c = np.random.randint(0, CHAR_SET_LEN)
        d = np.random.randint(0, CHAR_SET_LEN)
        captcha_text = charSet[a] + charSet[b] + charSet[c] + charSet[d]
        image = ImageCaptcha()
        image.write(captcha_text, captchaImgPath + captcha_text + '.png') # 图片格式改成其他可能会有问题
        k += 1
        sys.stdout.write("\rCreating %d" % (k))
        sys.stdout.flush()


# # 从验证码的图片集中取出一部分作为测试集，这些图片不参加训练，只用于模型的测试
# def prepare_test_set():
#     fileNameList = []
#     for filePath in os.listdir(CAPTCHA_IMAGE_PATH):
#         captcha_name = filePath.split('/')[-1]
#         fileNameList.append(captcha_name)
#     random.seed(time.time())
#     random.shuffle(fileNameList)
    # for i in range(TEST_IMAGE_NUMBER):
    #     name = fileNameList[i]
    #     shutil.move(CAPTCHA_IMAGE_PATH + name, TEST_IMAGE_PATH + name)


if __name__ == '__main__':
    generate_captcha_image(CHAR_SET, CHAR_SET_LEN, CAPTCHA_IMAGE_PATH)
    sys.stdout.write("\nFinished")
    sys.stdout.flush()
