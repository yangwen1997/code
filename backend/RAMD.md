# author yangwenlong

backend : 爬虫管理平台Django后台系统

manage.py : DJango启动文件
apps:   项目应用
uwsgi  :    uwsgi配置文件

后端更新代码后需要关闭uwsgi重新启动，否则不生效
前端程序如果上传一个新的接口时，需要修改nginx的可配置的连接文件对接口进行拦截并重启nginx,否则不生效

ngingx 重启命令
    nginx -s reload
 uwsgi 启动命令
    uwsgi --ini uwsgi.ini
