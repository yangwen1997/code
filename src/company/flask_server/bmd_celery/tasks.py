from celery import Celery
import sys
sys.path.extend([r'D:\bmd\bmd_server\src\company'])


from flask_server.process_.Reserve_total import check_reserve
app = Celery('tasks')
app.config_from_object('celeryconfig')
@app.task
def check_online_total(*args):
    """
    发布任务检测数据是否推送
    :param args:
    :return:
    """
    start = check_reserve()
    TAG = start.check_online_total()
    if TAG == "数据状态检测完成":
        return TAG

@app.task
def check_tel_total(*args):
    """
    发布任务检测数据号码是否需要检测
    :param args:
    :return:
    """
    start = check_reserve()
    TAG = start.check_tel_total()
    if TAG == "号码检测完成":
        return TAG

@app.task
def test(*args):

    start = check_reserve()
    result = start.test_add()

    return result
