import paramiko
import re
import requests
import hashlib
import time
import pymongo
import logging
import gc

MONGO_DB = pymongo.MongoClient(host='172.16.75.38',port=27017)
STATIC_IP = MONGO_DB["IP"]["STATIC_IP"]
HOST_INFO = MONGO_DB["IP"]["HOST_INFO"]


#设置日志记录器
logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%Y %H:%M:%S',
        filename='debug.log',
        filemode='w'
    )
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] %(filename)s[Line:%(lineno)d] [%(levelname)s] %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)


def conmond(shell,ssh):
    """
    执行shell命令
    :param shell:  shell 命令
    :param ssh: 创建的ssh客户端
    :return:
    """
    stdin, stdout, stderr = ssh.exec_command(str(shell))
    return str(stdout.read(),encoding='utf-8')


def redail(ssh,count):
    """拨号"""
    time.sleep(2)
    output_if = conmond('ip addr', ssh)
    ip = re.findall('inet (\d+.\d+.\d+.\d+) peer \d+.\d+.\d+.\d+/\d+ scope global ppp0', output_if)
    if len(ip) > 0 :
        ip = ip[0]
        output_state = conmond('curl -sL -x 127.0.0.1:2404 -w "%{http_code}" "www.baidu.com" -o /dev/null', ssh)
        if output_state == '200':
            logging.info('redail: 拨号成功')
            return ip
    else:
        count -= 1
        if count > 0 :
            redail(ssh,count)
        else:
            return False

def get_dial_ip(hostname,port:int):
    """
    :param hostname: 服务器主机
    :param port: 服务器ssh登录端口
    :param username: 用户名
    :param password: 密码
    :return:
    """
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 允许连接不在know_hosts文件中的主机
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=hostname, port=port, username="root", password="Vsw2vzIXxs")

    # 执行拨号脚本重新拨号
    # stdin, stdout, stderr = ssh.exec_command('python dial_2404.py')

    conmond('adsl-stop', ssh)
    conmond("ps -ef|grep /usr/sbin/pppd|grep -v grep|awk '{print $3,$2}'|xargs kill 9", ssh)
    conmond('pppoe-start', ssh)
    time.sleep(5)
    count = 3
    ip = redail(ssh,count)

    if ip:
        ssh.close()
        return ip
    else:
        return False

def ip_get():
    result = STATIC_IP.find({"flag":"0"})

    for _ in result:
        try:
            hostname = _["UUID_parmas"]
            host_info = HOST_INFO.find_one({"hostname":hostname})
            ip = get_dial_ip(hostname=host_info["host"],port=int(host_info["port"]))

            if ip:
                ip_parms = ip + ":" + "2404"
                # logging.info(ip_parms)
                item = {}
                item["_id"] = hashlib.md5(str(host_info['hostname']).encode('utf-8')).hexdigest()
                item["ip_parmas"] = ip_parms
                item["UUID_parmas"] = host_info['hostname']
                item["update_time"] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                if hostname == '323dgg1':
                    item["flag"] = "2"
                else:
                    item["flag"] = "1"
                STATIC_IP.save(item)
                logging.info("存入IP池成功:{}".format(ip_parms))
        except Exception as e:
            logging.info(e)

while 1:
    try:
        ip_get()
    except Exception as e:
        pass
