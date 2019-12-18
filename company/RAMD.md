#author yangwenlong



flask_company       :   flask 后台服务
    common          :   企业公共文件配置
    config          :   配置文件
    views           :   蓝图路由函数文件夹
    bmd_celery      :   celery异步任务
    process_            :   逻辑代码文件夹
        Reserve         :   数据总表查询文件
        check_tel       :   号码检测文件
        excel_push      ：  excel上传，公司/手机号去重
        result_push     :   按照液态推送数据

创建虚拟环境 : mkvirtualenv my_env
进入虚拟环境 : workon my_env
退出虚拟环境 : deactivate
列出虚拟环境 : lsvirtualenv


版本redis=2.10.6
    celery=3.1.25 
