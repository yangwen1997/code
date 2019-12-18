from .api import api

DEFAULT_BLUEPRINT = [
    [api,"/api"]
]

# 封装函数，注册蓝本
def register_blueprint(app):
    for x in DEFAULT_BLUEPRINT:
        app.register_blueprint(x[0], url_prefix=x[1])
