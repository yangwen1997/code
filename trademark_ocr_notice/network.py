import json
import requests
import time
from hashlib import sha1
from time import sleep
import hmac
import base64
from PIL import Image
from cnocr import CnOcr
from zheye import zheye
ocr = CnOcr()
z = zheye()
class Zhihu(object):

    def __init__(self):
        self.session=requests.session()
        self.headers={
            # 'authority':'www.zhihu.com',
            'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
        }
        self.session.headers.update(self.headers)
        self.picture=None
        self.signature=None
        self.picture_url=None

    def getcapture(self):
        # 获取验证码方法，有时候不用获取验证码就可以直接登录
        # lang=en是英文字母 验证码
        # message=self.session.get(url='https://www.zhihu.com/api/v3/oauth/captcha?lang=en').json()       # get 检测是否需要验证码
        message=self.session.get(url='https://www.zhihu.com/api/v3/oauth/captcha?lang=cn').json()       # get 检测是否需要验证码
        print(message)
        if message['show_captcha'] == False:
            self.picture=''
        else:
            # self.picture_url = self.session.put(url='https://www.zhihu.com/api/v3/oauth/captcha?lang=en').json()    # put 获取验证码
            self.picture_url = self.session.put(url='https://www.zhihu.com/api/v3/oauth/captcha?lang=cn').json()    # put 获取验证码
            # 采用base64格式将验证码通过图片格式显示出来
            with open(r'E:\code\chineseocr-app\trademark_ocr_notice\captcha.png','wb') as f:
                f.write(base64.b64decode(self.picture_url['img_base64']))
            positions = z.Recognize(r'E:\code\chineseocr-app\trademark_ocr_notice\captcha.png')
            # imgs=Image.open(r'E:\code\chineseocr-app\trademark_ocr_notice\captcha.png')
            # image.show()
            # if imgs.mode == "P":
            #     imgs = imgs.convert('RGB')
            #     imgs.save(r'E:\code\chineseocr-app\trademark_ocr_notice\captcha.png')
            # res = ocr.ocr(r'E:\code\chineseocr-app\trademark_ocr_notice\captcha.png')
            # self.picture = res
            # self.picture=input('请输入验证码')
            # json.dumps({'img_size': [200, 44],
            #             'input_points': [i[0],i[1] for i in positions]})
            pos = []
            for i in positions:
                i = list(i)
                pos.append(i)
            self.picture = json.dumps({'img_size': [200, 44],"input_points":pos})

            message1=self.session.post(url='https://www.zhihu.com/api/v3/oauth/captcha?lang=en',data={'input_text':self.picture}).json()    # post 验证码
            print(message1)

    def get_signature(self):
        # 知乎登陆的主要问题在于找到signature了这是重点。
        a=hmac.new('d1b964811afb40118a12068ff74a12f4'.encode('utf-8'),digestmod=sha1)
        a.update('password'.encode('utf-8'))
        a.update(b'c3cef7c66a1843f8b3a9e6a1e3160e20')
        a.update(b'com.zhihu.web')
        a.update(str(int(time.time()*1000)).encode())
        self.signature=a.hexdigest()

    def Login_phone(self):
        # 登录
        data={
            'client_id':'c3cef7c66a1843f8b3a9e6a1e3160e20',#'c3cef7c66a1843f8b3a9e6a1e3160e20',
            'grant_type':'password',
            'timestamp':str(int(time.time()*1000)),
            'source':'com.zhihu.web',
            'signature':self.signature,
            'username':'3045871342@qq.com',
            'password':'dgg962540',
            'captcha':self.picture,
            'lang':'en',
            # 'ref_source':'homepage',
            # 'utm_source':''
        }

        headers = {
                    # 'scheme':'https',
                    # 'accept':'*/*',
                    # 'accept-encoding':'gzip, deflate, br',
                    # 'accept-language':'zh-CN,zh;q=0.8',
                    # 'cache-control':'no-cache',
                    # 'content-length':'412',
                    # 'origin':'https://www.zhihu.com',
                   'content-type':'application/x-www-form-urlencoded',
                   # 'referer':'https://www.zhihu.com/signin?next=%2F',
                   'x-zse-83':'3_2.0',
                   }
        message=self.session.post(url='https://www.zhihu.com/api/v3/oauth/sign_in', headers=headers, data=data)
        message.encoding='utf-8'
        print(message.text)
        print(json.loads(message.text)['error']['message'])

    def target_url(self,url):
        text=self.session.get(url)
        return text.text


if __name__ == "__main__":
    zhihu=Zhihu()
    zhihu.getcapture()      # 验证码
    zhihu.get_signature()   # signature
    zhihu.Login_phone()     # 登录
