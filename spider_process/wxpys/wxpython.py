# encoding='utf-8'


#微信机器人自动发送消息
from wxpy import *
import time
# 初始化机器人，扫码登陆


bot = Bot()
my_friend = bot.friends().search('张半仙', city="成都")[0]
# 定时企业微信发送消息
# import requests,json
#
# wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=29aab440-4cdc-41a3-be3f-cf0ee97bc6f3"
#
# dsj_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4ed90a0b-dc9c-4323-b132-005038d7d3fd"
#
# send_message = "记得发日报，小心明天扣钱"
# send_message = "sucess"

# def send_msg():
#     #json格式化发送的数据信息
#
#     data = json.dumps({
#         "msgtype":"text",
#         "text":{
#             "content":send_message, # 发送的消息内容
#             "mentioned_list":["@all"] #圈出所有人
#         }
#     })
#
#     r = requests.post(wx_url,data,auth=('Content-Type', 'application/json'))
#     resp = requests.post(dsj_url,data,auth=('Content-Type', 'application/json'))
#     print(r.json)

def work():

    # 搜索名称含有 "毛桃子" 的好友

    # 发送文本给好友
    my_friend.send('记得发日报，小心明天扣钱')
    # send_msg()
#
# if __name__ == '__main__':
#     work()

import time
import datetime

# print(datetime.date.today())
def get_current_week():
    date = datetime.datetime.now()
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }
    day = date.weekday()

    return week_day_dict[day]


while 1:
    date = get_current_week()
    datelt = ['星期一','星期二','星期三','星期四','星期五']
    if date in datelt:
        hour = time.strftime("%H",time.localtime())
        min = time.strftime("%M",time.localtime())
        if int(hour) == 20 and int(min) == 10:
            work()
            time.sleep(15)
        else:
            pass
    else:
        pass