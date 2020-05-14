from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import TrademarkBaseInfo,TrademarkBaseInfo1,TrademarkBaseInfo2,\
    TrademarkRegistrantInfo,TrademarkAgencyInfo,TrademarkCommodityServerInfo,TrademarkPriorityInfo,\
    TrademarkCoOwnerInfo,TrademarkImageInfo
from .Serializer import TrademarkCommodityServerInfoContent,TreadeBaseINFO



class trade_search_name(APIView):

    def post(self,request):
        item = {}
        item["code"] = 200
        treadeName = request.POST.get("treadeName",None)
        if treadeName:
            try:
                # BaseInfo = TrademarkBaseInfo.objects.using("trade").filter(trademark_name__contains=treadeName)
                BaseInfo = TrademarkBaseInfo.objects.using("trade").filter(trademark_name=treadeName)

                LT = []
                for _ in BaseInfo:
                    items = TreadeBaseINFO(_)
                    print(items.data)
                    LT.append(items.data)

                item["data"] = LT

            except Exception as e:
                print(e)
        else:
            item["err_msg"] = "暂无商标信息"
        return Response(item)


class tradeInfo_API(APIView):
    """商标查询API"""
    def get(self,request):
        item = {}
        item["code"] = 200
        treadeName = request.GET.get("treadeName", None)
        if treadeName:
            try:
                BaseInfo = TrademarkBaseInfo.objects.using("trade").filter(trademark_name=treadeName).first()

                # 商标注册人与基本信息表关联字段信息regist_num_and_class
                baseregist_num_and_class = BaseInfo.regist_num_and_class
                baseRegistrantInfo = TrademarkRegistrantInfo.objects.using("trade").filter(regist_num_and_class=baseregist_num_and_class).first()

                # 注册商标优先权信息表
                PriorityInfo = TrademarkPriorityInfo.objects.using("trade").filter(regist_num_and_class=baseregist_num_and_class).first()


                # 共有人信息表及申请号关联字段
                baseregist_num = BaseInfo.regist_num
                CoOwnerInfo = TrademarkCoOwnerInfo.objects.using("trade").filter(regist_num=baseregist_num).first()

                # 商标图片信息表
                ImageInfo = TrademarkImageInfo.objects.using("trade").filter(regist_num=baseregist_num).first()

                # 商标小项信息表
                CommodityServerInfo = TrademarkCommodityServerInfo.objects.using("trade").filter(regist_num_and_class=baseregist_num_and_class).values()
                # CommodityServerInfo = TrademarkCommodityServerInfo.objects.using("trade").filter(regist_num_and_class=baseregist_num_and_class).first()
                # a = TrademarkCommodityServerInfoContent(CommodityServerInfo)
                CommodityLT = []
                for _ in CommodityServerInfo:
                    TrademarkCommodityServerInfoContent
                    items = {}
                    items["类似群"] = _["similar_group"]
                    items["商品中文名称"] = _["commodity_chinese_name"]
                    items["商品序号"] = _["commodity_num"]
                    items["商品状态"] = _["commodity_state"]
                    CommodityLT.append(items)

                #代理人与基本信息表关联字段信息
                agency_info = BaseInfo.agent_num
                AgencyInfo = TrademarkAgencyInfo.objects.using("trade").filter(agent_num=agency_info).first()

                item["商标名称"] = BaseInfo.trademark_name
                item["申请号"] = BaseInfo.regist_num
                item["申请日期"] = BaseInfo.regist_time
                item["初审公告期号"] = BaseInfo.preliminary_notice_num
                item["初审公告日期"] = BaseInfo.preliminary_notice_time
                item["注册公告期号"] = BaseInfo.regist_notice_num
                item["注册公告日期"] = BaseInfo.regist_notice_time
                item["专用有效期"] = BaseInfo.special_period_effective_time
                item["代理人编码"] = BaseInfo.agent_num

                item["国际分类"] = BaseInfo.international_class
                item["商标类型"] = BaseInfo.trademark_type
                item["专用期开始日期"] = BaseInfo.special_period_start_time
                item["专用期结束日期"] = BaseInfo.special_period_end_time
                item["商标设计说明"] = BaseInfo.design_description
                item["商标颜色说明"] = BaseInfo.color_description
                item["放弃专用权说明"] = BaseInfo.give_up_special_authority_description
                item["是否立体商标"] = BaseInfo.is_three_dimensional
                item["是否共有申请"] = BaseInfo.is_co_regist
                item["商标形态"] = BaseInfo.form
                item["地理标志信息"] = BaseInfo.geographical_indication_info
                item["颜色标志"] = BaseInfo.color_indication
                item["是否驰名商标"] = BaseInfo.is_well_known




                item["代理人名称"] = AgencyInfo.agent_name

                item["申请人名称"] = baseRegistrantInfo.registrant_chinese_name if baseRegistrantInfo else ""
                item["申请人英文名称"] = baseRegistrantInfo.registrant_foreign_name  if baseRegistrantInfo else ""
                item["申请人地址"] = baseRegistrantInfo.registrant_chinese_address  if baseRegistrantInfo else ""
                item["申请人英文地址"] = baseRegistrantInfo.registrant_foreign_address  if baseRegistrantInfo else ""
                item["商品服务项目"] = CommodityLT

                item["优先权日期"] = PriorityInfo.priority_date if PriorityInfo else ""
                item["优先权编号"] = PriorityInfo.priority_num if PriorityInfo else ""
                item["优先权种类"] = PriorityInfo.priority_type if PriorityInfo else ""
                item["优先权商品"] = PriorityInfo.priority_commodity if PriorityInfo else ""
                item["优先权国家/地区"] = PriorityInfo.priority_country if PriorityInfo else ""

                item["共有人中文名称"] = CoOwnerInfo.co_owner_chinese_name if CoOwnerInfo else ""
                item["共有人英文文名称"] = CoOwnerInfo.co_owner_english_name if CoOwnerInfo else ""
                item["共有人中文地址"] = CoOwnerInfo.co_owner_chinese_address if CoOwnerInfo else ""
                item["共有人英文地址"] = CoOwnerInfo.co_owner_english_address if CoOwnerInfo else ""


                item["商标图样的文件服务器路由"] = ImageInfo.image_url if ImageInfo else ""

            except Exception as e:
                pass
        else:
            item["msg"] = "商标名称不存在"

        return Response(item)
