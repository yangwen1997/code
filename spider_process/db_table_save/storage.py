import pymysql

conn = pymysql.connect(host="172.16.75.38",port=3306,user="yang",password="dgg102888",database="db_manage")
cursor = conn.cursor()

sql_data = {"title": "大数据信息表","ch_table": "dm层-新BI系统-每日电话信息聚合表","en_table":"dm_new_bi_performance_vis_aggr_daily","dates":r"""{"info":[
{"field": "user_id","dataType": "mysql","fieldType":"bigint","length":"20","notes":"客户ID"},
{"field": "login_name", "dataType": "mysql", "fieldType": "varchar", "length": "20", "notes": "客户编号"},
{"field": "real_name", "dataType": "mysql", "fieldType": "varchar", "length": "20", "notes": "客户姓名"},
{"field": "aggr_day", "dataType": "mysql", "fieldType": "int", "length": "11", "notes": "客户年龄"},
{"field": "aggr_month", "dataType": "mysql", "fieldType": "varchar", "length": "20", "notes": "客户性别"},

{"field": "cus_area", "dataType": "mysql", "fieldType": "varchar", "length": "64", "notes": "客户所在区域"},
{"field": "cus_type", "dataType": "mysql", "fieldType": "varchar", "length": "20", "notes": "客户类型：个人/企业"},
{"field": "cus_create_time", "dataType": "mysql", "fieldType": "varchar", "length": "20", "notes": "客户创建时间"},
{"field": "cus_id_card", "dataType": "mysql", "fieldType": "varchar", "length": "20", "notes": "客户身份证号"},
{"field": "cus_tel", "dataType": "mysql", "fieldType": "varchar", "length": "20", "notes": "客户电话"},
{"field": "cus_contact_way", "dataType": "mysql", "fieldType": "varchar", "length": "20", "notes": "客户联系方式：MB/QQ/QT/TEL/WX"},
{"field": "cus_comp_name", "dataType": "mysql", "fieldType": "varchar", "length": "64", "notes": "客户公司名称"},
{"field": "cus_comp_login_time", "dataType": "mysql", "fieldType": "varchar", "length": "20", "notes": "客户公司注册时间"},
{"field": "cus_comp_login_capital", "dataType": "mysql", "fieldType": "decimal", "length": "20", "notes": "客户公司注册金额"},
{"field": "cus_trade", "dataType": "mysql", "fieldType": "varchar", "length": "20", "notes": "客户所属行业"},
{"field": "cus_comp_status", "dataType": "mysql", "fieldType": "varchar", "length": "20", "notes": "客户公司状态：正常/注销"},
{"field": "cus_origin", "dataType": "mysql", "fieldType": "varchar", "length": "20", "notes": "客户来源"},
{"field": "cus_education", "dataType": "mysql", "fieldType": "varchar", "length": "20", "notes": "客户教育水平"},
{"field": "last_bus_id", "dataType": "mysql", "fieldType": "varchar", "length": "20", "notes": "最新商机ID"},
{"field": "sign_status", "dataType": "mysql", "fieldType": "int", "length": "11", "notes": "客户签单状态：0-未签单/1-已签单"},
{"field": "last_sign_time", "dataType": "mysql", "fieldType": "varchar", "length": "20", "notes": "最新签单时间"},
{"field": "last_sign_type_code", "dataType": "mysql", "fieldType": "varchar", "length": "20", "notes": "最新签单业态"},
{"field": "order_count", "dataType": "mysql", "fieldType": "int", "length": "11", "notes": "订单数量"},
{"field": "order_type", "dataType": "mysql", "fieldType": "int", "length": "11", "notes": "已签订单类型：0-无/1-线下/2-网签/3-线下+网签"},
{"field": "is_refer_twice", "dataType": "mysql", "fieldType": "int", "length": "11", "notes": "是否二次咨询：1-是0-不是 --两条以上商机"},
{"field": "is_sign_bill", "dataType": "mysql", "fieldType": "int", "length": "11", "notes": "是否签单：1-是0-不是"},
{"field": "sign_bill_bu", "dataType": "mysql", "fieldType": "varchar", "length": "64", "notes": "签单事业部 --多个"},
{"field": "sign_bill_pro", "dataType": "mysql", "fieldType": "varchar", "length": "64", "notes": "业态名称 --多个"},
{"field": "payment_way", "dataType": "mysql", "fieldType": "varchar", "length": "64", "notes": "付款方式：支付宝/微信/..."},
{"field": "payment_amount", "dataType": "mysql", "fieldType": "decimal", "length": "20", "notes": "签单核款金额 --多个订单总金额"},
{"field": "is_apply_ip", "dataType": "mysql", "fieldType": "int", "length": "11", "notes": "是否申请过知识产权：1-是0-不是2-未知"},
{"field": "first_refer_city", "dataType": "mysql", "fieldType": "varchar", "length": "64", "notes": "首次咨询所在城市"},
{"field": "refered_bu", "dataType": "mysql", "fieldType": "varchar", "length": "128", "notes": "咨询过的事业部"},
{"field": "last_refer_time", "dataType": "mysql", "fieldType": "varchar", "length": "64", "notes": "最新咨询时间"},
{"field": "business_count", "dataType": "mysql", "fieldType": "int", "length": "11", "notes": "累计新建商机量"},
{"field": "tel_status", "dataType": "mysql", "fieldType": "varchar", "length": "20", "notes": "电话状态：已接通/未接通"},
{"field": "connect_count_60day", "dataType": "mysql", "fieldType": "int", "length": "11", "notes": "最近60天接通电话次数"},
{"field": "tel_count_60day", "dataType": "mysql", "fieldType": "int", "length": "11", "notes": "最近60天通话次数"},
{"field": "tel_30s_count", "dataType": "mysql", "fieldType": "int", "length": "11", "notes": "累计30秒的通话次数"},
{"field": "max_tel_seconds", "dataType": "mysql", "fieldType": "int", "length": "11", "notes": "最长通话时长"},
{"field": "max_tel_time", "dataType": "mysql", "fieldType": "varchar", "length": "64", "notes": "最长通话时长所在日期"},
{"field": "last_contact_time", "dataType": "mysql", "fieldType": "varchar", "length": "20", "notes": "最近一次联系时间"},
{"field": "is_visit", "dataType": "mysql", "fieldType": "int", "length": "11", "notes": "是否上门：1-是0-不是"},
{"field": "visit_count", "dataType": "mysql", "fieldType": "int", "length": "11", "notes": "上门次数"},
{"field": "last_visit_time", "dataType": "mysql", "fieldType": "varchar", "length": "64", "notes": "最近上门时间"},
{"field": "is_complain", "dataType": "mysql", "fieldType": "int", "length": "11", "notes": "是否投诉"},
{"field": "last_complain_time", "dataType": "mysql", "fieldType": "varchar", "length": "64", "notes": "最近投诉时间"},
{"field": "is_grumble", "dataType": "mysql", "fieldType": "int", "length": "11", "notes": "是否抱怨"},
{"field": "last_grumble_time", "dataType": "mysql", "fieldType": "varchar", "length": "64", "notes": "最近抱怨时间"},
]}"""}

dates = sql_data["dates"]
sql = "INSERT INTO db_info(title,ch_table,en_table,dates) VALUES ('{}','{}','{}','{}')".format(str(sql_data["title"]),str(sql_data["ch_table"]),str(sql_data["en_table"]),dates)


try:
   # 执行sql语句
   cursor.execute(sql)
   # print(cursor.fetchone())
   # 提交到数据库执行
   conn.commit()
   print("存入数据库成功")
except Exception as e:

    print(e)
    # conn.rollback()

# 关闭数据库连接
cursor.close()
conn.close()



# bi_all_table_mapping
#bi_form_detail
#bi_form_measure_mapping
#bi_measure_dimension_mapping
#bi_topic_detail
#dept_mapping
#dgg_wrk_user_conf
#dm_bi_dzb_custom_performance_all
#dm_bi_dzh_resources_operation