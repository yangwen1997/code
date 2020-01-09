from .api import api
from .captch import captch
from .Tel import tel

# 导入模块路由
DEFAULT_BLUEPRINT = [
    [api,"/api"],
    [captch,"/captch"],
    [tel,"/tel"],
]

# 封装函数，注册蓝本
def register_blueprint(app):
    for x in DEFAULT_BLUEPRINT:
        app.register_blueprint(x[0], url_prefix=x[1])
