#encoding=utf-8

class DBrouter(object):
    """数据库路由、读写配置"""

    def db_for_read(self, model, **hints):
        """
            设置从哪个表读取数据
        """
        if model._meta.app_label == 'sdxydb':
            return "sdxydb"
        return None

    def db_for_write(self, model, **hints):
        """
            设置写入数据到哪个表
        """
        if model._meta.app_label == 'sdxydb':
            return "sdxydb"
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        指定迁移数据库时与项目中的数据库地址一致
        :param db:
        :param app_label:
        :param model_name:
        :param hints:
        :return:
        """
        if app_label == 'sdxydb':
            return db == 'sdxydb'
        else:
            return None

