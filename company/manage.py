from flask_server import create_app
from flask_script import Manager
from flask_wtf.csrf import CSRFProtect
from flask_cors import *

import logging
import time

app = create_app()
CORS(app, supports_credentials=True)

# manager = Manager(app)
# 设置flaks中的日志文件可以写入指定位置，并以utf-8的方式记录
log_dir_name = r'D:\bmd\bmd_server\src\company\flask_server\log\白名单推送.log'
handler = logging.FileHandler(log_dir_name,encoding='utf-8')

# 日志格式
logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)

app.logger.addHandler(handler)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8082)
    # manager.run()

