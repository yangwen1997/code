from rest_framework import serializers

class TreadeBaseINFO(serializers.Serializer):
    """基本信息序列器"""
    regist_num_and_class = serializers.CharField(max_length=255)
    regist_num = serializers.CharField(max_length=64)
    international_class = serializers.CharField(max_length=64)
    regist_time = serializers.CharField(max_length=255)
    trademark_name = serializers.CharField(max_length=255)
    trademark_type = serializers.CharField(max_length=255)
    agent_num = serializers.CharField(max_length=255)
    preliminary_notice_num = serializers.CharField(max_length=255)
    preliminary_notice_time = serializers.CharField(max_length=255)
    regist_notice_num = serializers.CharField(max_length=255)
    regist_notice_time = serializers.CharField(max_length=255)
    special_period_start_time = serializers.CharField(max_length=255)
    special_period_end_time = serializers.CharField(max_length=255)
    special_period_effective_time = serializers.CharField(max_length=255)
    design_description = serializers.CharField()
    color_description = serializers.CharField()
    give_up_special_authority_description = serializers.CharField()
    is_three_dimensional = serializers.CharField(max_length=255)
    is_co_regist = serializers.CharField(max_length=255)
    form = serializers.CharField(max_length=255)
    geographical_indication_info = serializers.CharField(max_length=255)
    color_indication = serializers.CharField(max_length=255)
    is_well_known = serializers.CharField(max_length=255)
    update_time = serializers.CharField()


class TrademarkCommodityServerInfoContent(serializers.Serializer):
    """商标小项序列器"""
    regist_num_and_class = serializers.CharField(max_length=255)
    regist_num = serializers.CharField(max_length=64)
    international_class = serializers.CharField(max_length=64)
    similar_group = serializers.CharField(max_length=64)
    commodity_num = serializers.CharField(max_length=64)
    commodity_chinese_name = serializers.CharField(max_length=255)
    commodity_state = serializers.CharField(max_length=255)
    update_time = serializers.CharField()
