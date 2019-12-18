from flask_server.common import com_reserve
#
#
# # RESULT = com_reserve.find({}).skip(752)
RESULT = com_reserve.find({})
# # RESULT = com_reserve.find({"push": "0","tel_check" : "实号", "mark":"知产"}).limit(250)
# # RESULT = com_reserve.find({}).limit(100).skip(100)
COUNT = 0
for _ in RESULT:
#     # _["mark"] = "资质"
#     # _["push"] = "0"
#     # del _["push"]
    _["tel_check"] = "实号"
    id = _["_id"]
    com_reserve.update({"_id":id},_)
#     COUNT += 1
print(COUNT)

