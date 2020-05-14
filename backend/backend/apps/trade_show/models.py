# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TrademarkAgencyInfo(models.Model):
    agent_num = models.CharField(unique=True, max_length=255)
    agent_name = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_agency_info'


class TrademarkBaseInfo(models.Model):
    """商标基本信息"""
    regist_num_and_class = models.CharField(max_length=255)
    regist_num = models.CharField(max_length=64)
    international_class = models.CharField(max_length=64, blank=True, null=True)
    regist_time = models.CharField(max_length=255, blank=True, null=True)
    trademark_name = models.CharField(max_length=255, blank=True, null=True)
    trademark_type = models.CharField(max_length=255, blank=True, null=True)
    agent_num = models.CharField(max_length=255, blank=True, null=True)
    preliminary_notice_num = models.CharField(max_length=255, blank=True, null=True)
    preliminary_notice_time = models.CharField(max_length=255, blank=True, null=True)
    regist_notice_num = models.CharField(max_length=255, blank=True, null=True)
    regist_notice_time = models.CharField(max_length=255, blank=True, null=True)
    special_period_start_time = models.CharField(max_length=255, blank=True, null=True)
    special_period_end_time = models.CharField(max_length=255, blank=True, null=True)
    special_period_effective_time = models.CharField(max_length=255, blank=True, null=True)
    design_description = models.TextField(blank=True, null=True)
    color_description = models.TextField(blank=True, null=True)
    give_up_special_authority_description = models.TextField(blank=True, null=True)
    is_three_dimensional = models.CharField(max_length=255, blank=True, null=True)
    is_co_regist = models.CharField(max_length=255, blank=True, null=True)
    form = models.CharField(max_length=255, blank=True, null=True)
    geographical_indication_info = models.CharField(max_length=255, blank=True, null=True)
    color_indication = models.CharField(max_length=255, blank=True, null=True)
    is_well_known = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_base_info'


class TrademarkBaseInfo1(models.Model):
    """商标基本信息"""
    regist_num_and_class = models.CharField(max_length=255)
    regist_num = models.CharField(max_length=64)
    international_class = models.CharField(max_length=64, blank=True, null=True)
    regist_time = models.CharField(max_length=255, blank=True, null=True)
    trademark_name = models.CharField(max_length=255, blank=True, null=True)
    trademark_type = models.CharField(max_length=255, blank=True, null=True)
    agent_num = models.CharField(max_length=255, blank=True, null=True)
    preliminary_notice_num = models.CharField(max_length=255, blank=True, null=True)
    preliminary_notice_time = models.CharField(max_length=255, blank=True, null=True)
    regist_notice_num = models.CharField(max_length=255, blank=True, null=True)
    regist_notice_time = models.CharField(max_length=255, blank=True, null=True)
    special_period_start_time = models.CharField(max_length=255, blank=True, null=True)
    special_period_end_time = models.CharField(max_length=255, blank=True, null=True)
    special_period_effective_time = models.CharField(max_length=255, blank=True, null=True)
    design_description = models.TextField(blank=True, null=True)
    color_description = models.TextField(blank=True, null=True)
    give_up_special_authority_description = models.TextField(blank=True, null=True)
    is_three_dimensional = models.CharField(max_length=255, blank=True, null=True)
    is_co_regist = models.CharField(max_length=255, blank=True, null=True)
    form = models.CharField(max_length=255, blank=True, null=True)
    geographical_indication_info = models.CharField(max_length=255, blank=True, null=True)
    color_indication = models.CharField(max_length=255, blank=True, null=True)
    is_well_known = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_base_info_1'


class TrademarkBaseInfo2(models.Model):
    """商标基本信息"""
    regist_num_and_class = models.CharField(max_length=255)
    regist_num = models.CharField(max_length=64)
    international_class = models.CharField(max_length=64, blank=True, null=True)
    regist_time = models.CharField(max_length=255, blank=True, null=True)
    trademark_name = models.CharField(max_length=255, blank=True, null=True)
    trademark_type = models.CharField(max_length=255, blank=True, null=True)
    agent_num = models.CharField(max_length=255, blank=True, null=True)
    preliminary_notice_num = models.CharField(max_length=255, blank=True, null=True)
    preliminary_notice_time = models.CharField(max_length=255, blank=True, null=True)
    regist_notice_num = models.CharField(max_length=255, blank=True, null=True)
    regist_notice_time = models.CharField(max_length=255, blank=True, null=True)
    special_period_start_time = models.CharField(max_length=255, blank=True, null=True)
    special_period_end_time = models.CharField(max_length=255, blank=True, null=True)
    special_period_effective_time = models.CharField(max_length=255, blank=True, null=True)
    design_description = models.TextField(blank=True, null=True)
    color_description = models.TextField(blank=True, null=True)
    give_up_special_authority_description = models.TextField(blank=True, null=True)
    is_three_dimensional = models.CharField(max_length=255, blank=True, null=True)
    is_co_regist = models.CharField(max_length=255, blank=True, null=True)
    form = models.CharField(max_length=255, blank=True, null=True)
    geographical_indication_info = models.CharField(max_length=255, blank=True, null=True)
    color_indication = models.CharField(max_length=255, blank=True, null=True)
    is_well_known = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_base_info_2'


class TrademarkCoOwnerInfo(models.Model):
    regist_num = models.CharField(max_length=64)
    co_owner_chinese_name = models.TextField(blank=True, null=True)
    co_owner_english_name = models.TextField(blank=True, null=True)
    co_owner_chinese_address = models.TextField(blank=True, null=True)
    co_owner_english_address = models.TextField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_co_owner_info'


class TrademarkCommodityServerInfo(models.Model):
    regist_num_and_class = models.CharField(max_length=255)
    regist_num = models.CharField(max_length=64)
    international_class = models.CharField(max_length=64, blank=True, null=True)
    similar_group = models.CharField(max_length=64, blank=True, null=True)
    commodity_num = models.CharField(max_length=64, blank=True, null=True)
    commodity_chinese_name = models.CharField(max_length=255, blank=True, null=True)
    commodity_state = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_commodity_server_info'


class TrademarkCommodityServerInfo1(models.Model):
    regist_num_and_class = models.CharField(max_length=255)
    regist_num = models.CharField(max_length=64)
    international_class = models.CharField(max_length=64, blank=True, null=True)
    similar_group = models.CharField(max_length=64, blank=True, null=True)
    commodity_num = models.CharField(max_length=64, blank=True, null=True)
    commodity_chinese_name = models.CharField(max_length=255, blank=True, null=True)
    commodity_state = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_commodity_server_info_1'


class TrademarkCommodityServerInfo10(models.Model):
    regist_num_and_class = models.CharField(max_length=255)
    regist_num = models.CharField(max_length=64)
    international_class = models.CharField(max_length=64, blank=True, null=True)
    similar_group = models.CharField(max_length=64, blank=True, null=True)
    commodity_num = models.CharField(max_length=64, blank=True, null=True)
    commodity_chinese_name = models.CharField(max_length=255, blank=True, null=True)
    commodity_state = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_commodity_server_info_10'


class TrademarkCommodityServerInfo11(models.Model):
    regist_num_and_class = models.CharField(max_length=255)
    regist_num = models.CharField(max_length=64)
    international_class = models.CharField(max_length=64, blank=True, null=True)
    similar_group = models.CharField(max_length=64, blank=True, null=True)
    commodity_num = models.CharField(max_length=64, blank=True, null=True)
    commodity_chinese_name = models.CharField(max_length=255, blank=True, null=True)
    commodity_state = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_commodity_server_info_11'


class TrademarkCommodityServerInfo12(models.Model):
    regist_num_and_class = models.CharField(max_length=255)
    regist_num = models.CharField(max_length=64)
    international_class = models.CharField(max_length=64, blank=True, null=True)
    similar_group = models.CharField(max_length=64, blank=True, null=True)
    commodity_num = models.CharField(max_length=64, blank=True, null=True)
    commodity_chinese_name = models.CharField(max_length=255, blank=True, null=True)
    commodity_state = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_commodity_server_info_12'


class TrademarkCommodityServerInfo13(models.Model):
    regist_num_and_class = models.CharField(max_length=255)
    regist_num = models.CharField(max_length=64)
    international_class = models.CharField(max_length=64, blank=True, null=True)
    similar_group = models.CharField(max_length=64, blank=True, null=True)
    commodity_num = models.CharField(max_length=64, blank=True, null=True)
    commodity_chinese_name = models.CharField(max_length=255, blank=True, null=True)
    commodity_state = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_commodity_server_info_13'


class TrademarkCommodityServerInfo14(models.Model):
    regist_num_and_class = models.CharField(max_length=255)
    regist_num = models.CharField(max_length=64)
    international_class = models.CharField(max_length=64, blank=True, null=True)
    similar_group = models.CharField(max_length=64, blank=True, null=True)
    commodity_num = models.CharField(max_length=64, blank=True, null=True)
    commodity_chinese_name = models.CharField(max_length=255, blank=True, null=True)
    commodity_state = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_commodity_server_info_14'


class TrademarkCommodityServerInfo2(models.Model):
    regist_num_and_class = models.CharField(max_length=255)
    regist_num = models.CharField(max_length=64)
    international_class = models.CharField(max_length=64, blank=True, null=True)
    similar_group = models.CharField(max_length=64, blank=True, null=True)
    commodity_num = models.CharField(max_length=64, blank=True, null=True)
    commodity_chinese_name = models.CharField(max_length=255, blank=True, null=True)
    commodity_state = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_commodity_server_info_2'


class TrademarkCommodityServerInfo3(models.Model):
    regist_num_and_class = models.CharField(max_length=255)
    regist_num = models.CharField(max_length=64)
    international_class = models.CharField(max_length=64, blank=True, null=True)
    similar_group = models.CharField(max_length=64, blank=True, null=True)
    commodity_num = models.CharField(max_length=64, blank=True, null=True)
    commodity_chinese_name = models.CharField(max_length=255, blank=True, null=True)
    commodity_state = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_commodity_server_info_3'


class TrademarkCommodityServerInfo4(models.Model):
    regist_num_and_class = models.CharField(max_length=255)
    regist_num = models.CharField(max_length=64)
    international_class = models.CharField(max_length=64, blank=True, null=True)
    similar_group = models.CharField(max_length=64, blank=True, null=True)
    commodity_num = models.CharField(max_length=64, blank=True, null=True)
    commodity_chinese_name = models.CharField(max_length=255, blank=True, null=True)
    commodity_state = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_commodity_server_info_4'


class TrademarkCommodityServerInfo5(models.Model):
    regist_num_and_class = models.CharField(max_length=255)
    regist_num = models.CharField(max_length=64)
    international_class = models.CharField(max_length=64, blank=True, null=True)
    similar_group = models.CharField(max_length=64, blank=True, null=True)
    commodity_num = models.CharField(max_length=64, blank=True, null=True)
    commodity_chinese_name = models.CharField(max_length=255, blank=True, null=True)
    commodity_state = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_commodity_server_info_5'


class TrademarkCommodityServerInfo6(models.Model):
    regist_num_and_class = models.CharField(max_length=255)
    regist_num = models.CharField(max_length=64)
    international_class = models.CharField(max_length=64, blank=True, null=True)
    similar_group = models.CharField(max_length=64, blank=True, null=True)
    commodity_num = models.CharField(max_length=64, blank=True, null=True)
    commodity_chinese_name = models.CharField(max_length=255, blank=True, null=True)
    commodity_state = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_commodity_server_info_6'


class TrademarkCommodityServerInfo7(models.Model):
    regist_num_and_class = models.CharField(max_length=255)
    regist_num = models.CharField(max_length=64)
    international_class = models.CharField(max_length=64, blank=True, null=True)
    similar_group = models.CharField(max_length=64, blank=True, null=True)
    commodity_num = models.CharField(max_length=64, blank=True, null=True)
    commodity_chinese_name = models.CharField(max_length=255, blank=True, null=True)
    commodity_state = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_commodity_server_info_7'


class TrademarkCommodityServerInfo8(models.Model):
    regist_num_and_class = models.CharField(max_length=255)
    regist_num = models.CharField(max_length=64)
    international_class = models.CharField(max_length=64, blank=True, null=True)
    similar_group = models.CharField(max_length=64, blank=True, null=True)
    commodity_num = models.CharField(max_length=64, blank=True, null=True)
    commodity_chinese_name = models.CharField(max_length=255, blank=True, null=True)
    commodity_state = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_commodity_server_info_8'


class TrademarkCommodityServerInfo9(models.Model):
    regist_num_and_class = models.CharField(max_length=255)
    regist_num = models.CharField(max_length=64)
    international_class = models.CharField(max_length=64, blank=True, null=True)
    similar_group = models.CharField(max_length=64, blank=True, null=True)
    commodity_num = models.CharField(max_length=64, blank=True, null=True)
    commodity_chinese_name = models.CharField(max_length=255, blank=True, null=True)
    commodity_state = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_commodity_server_info_9'


class TrademarkImageInfo(models.Model):
    image_id = models.CharField(max_length=64)
    regist_num = models.CharField(max_length=64, blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_image_info'


class TrademarkInternationalBaseInfo(models.Model):
    regist_num = models.CharField(unique=True, max_length=64)
    international_regist_num = models.CharField(max_length=64, blank=True, null=True)
    international_regist_time = models.CharField(max_length=255, blank=True, null=True)
    international_publish_time = models.CharField(max_length=255, blank=True, null=True)
    international_regist_language = models.CharField(max_length=255, blank=True, null=True)
    international_regist_type = models.CharField(max_length=255, blank=True, null=True)
    international_notice_num = models.CharField(max_length=255, blank=True, null=True)
    international_notice_time = models.CharField(max_length=255, blank=True, null=True)
    international_later_time = models.CharField(max_length=255, blank=True, null=True)
    international_basic_regist_time = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_international_base_info'


class TrademarkPriorityInfo(models.Model):
    regist_num_and_class = models.CharField(max_length=255, blank=True, null=True)
    regist_num = models.CharField(max_length=64, blank=True, null=True)
    international_class = models.CharField(max_length=64, blank=True, null=True)
    priority_num = models.CharField(max_length=255, blank=True, null=True)
    priority_type = models.CharField(max_length=255, blank=True, null=True)
    priority_date = models.CharField(max_length=255, blank=True, null=True)
    priority_commodity = models.TextField(blank=True, null=True)
    priority_country = models.CharField(max_length=255, blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_priority_info'


class TrademarkRegistrantInfo(models.Model):
    regist_num_and_class = models.CharField(max_length=255, blank=True, null=True)
    regist_num = models.CharField(max_length=64)
    international_class = models.CharField(max_length=64, blank=True, null=True)
    registrant_chinese_name = models.CharField(max_length=255, blank=True, null=True)
    registrant_foreign_name = models.CharField(max_length=255, blank=True, null=True)
    registrant_chinese_address = models.TextField(blank=True, null=True)
    registrant_foreign_address = models.TextField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_registrant_info'


class TrademarkRegistrantInfo1(models.Model):
    regist_num_and_class = models.CharField(max_length=255, blank=True, null=True)
    regist_num = models.CharField(max_length=64)
    international_class = models.CharField(max_length=64, blank=True, null=True)
    registrant_chinese_name = models.CharField(max_length=255, blank=True, null=True)
    registrant_foreign_name = models.CharField(max_length=255, blank=True, null=True)
    registrant_chinese_address = models.TextField(blank=True, null=True)
    registrant_foreign_address = models.TextField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_registrant_info_1'


class TrademarkRegistrantInfo2(models.Model):
    regist_num_and_class = models.CharField(max_length=255, blank=True, null=True)
    regist_num = models.CharField(max_length=64)
    international_class = models.CharField(max_length=64, blank=True, null=True)
    registrant_chinese_name = models.CharField(max_length=255, blank=True, null=True)
    registrant_foreign_name = models.CharField(max_length=255, blank=True, null=True)
    registrant_chinese_address = models.TextField(blank=True, null=True)
    registrant_foreign_address = models.TextField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'trademark_registrant_info_2'
