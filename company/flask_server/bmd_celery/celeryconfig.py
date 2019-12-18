# from bmd_celery.schedules import crontab
# from datetime import timedelta
# 配置中间人及结果存放redis地址
BROKER_URL = 'redis://127.0.0.1:6379/14'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/15'

CELERY_TIMEZONE='Asia/Shanghai'

imports = [
    "tasks",  # 导入py文件
]

# CELERYBEAT_SCHEDULE = {
#     'check_online_total': {
#         'task': 'tasks.check_online_total',
#         'schedule': crontab(minute='*/1'),   # 每1分钟执行一次
#         'args': ()             # 任务函数参数
#     },
#     # 'check_tel_total' : {
#     #     'task': 'tasks.check_tel_total',
#     #     'schedule': crontab(minute='*/1'),  # 每1分钟执行一次
#     #     'args': ()
#     # }
# }

# 日志
