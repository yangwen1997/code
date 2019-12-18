from flask import Flask
from flask_server.views import register_blueprint
from flask_server.config import BaseConfig
# 创建工厂函数


def create_app():

    # 创建应用实列对象
    app = Flask(__name__)

    # 初始化配置，配置的一些数据库这里咱不配置
    app.config.from_object(BaseConfig)
    app.config['UPLOAD_FOLDER'] = r'./files'
    # 配置扩展,暂无配置

    # 注册蓝本
    register_blueprint(app)


    return app

