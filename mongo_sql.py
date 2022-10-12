import bson
import time
from Port_info import appConf
import mongo_con
"""
    mongodb相关库 表
    xx_db_table_info = {"db": "库", "tb": "表"}
    需要执行sql
    xx_sql = {"challenge_item": "bank_card"}
    xx_sql = [{"challenge_item": "bank_card"}]
"""


# --------------xx业务------------
# xx业务
xx_db_table_info = {"db": "shoufuyou_crcs", "tb": "challengeItemSaveLog"}
# 查询demo
xx_sql = {"challenge_item": "bank_card"}

# --------------替换授信用户身份证------------
# ocr
ocr_db_table_info1 = {"db": "shoufuyou_crcs", "tb": "challengeItemSaveLog"}
# 风险挑战项身份证修改 org:初始值 new:需要改为的值
set_challenge_card = {"org": {"id_card_number": appConf.id_card, "app": "{}"},
                      "new": {'id_card_number': '{}'}}
# 预授信
ocr_db_table_info2 = {"db": "shoufuyou_crcs", "tb": "crcsCashPerson"}
set_credit_card = {"org": {"id_card_number": appConf.id_card, "app": "{}"},
                   "new": {'id_card_number': '{}'}}

# --------------上报信息------------

# 上报通讯录 库-表
submit_db_table_info1 = {"db": "shoufuyou_reporting", "tb": "contacts"}

# 默认请求加密数据org初始值user_id=111111126112 需要替换落库明文
set_contact_info = {"org": {"user_id": "111111126112"},
                    "new": {"event_time": bson.int64.Int64(int(time.time())), "device_id": "{}", "user_id": "{}",
                            "session_id": "{}",
                            "app": "{}", "created_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}}

# 上报通话记录 库-表 -查询和替换数据同set_contact_info
submit_db_table_info2 = {"db": "shoufuyou_reporting", "tb": "callRecord"}

# 上报短信库-表 -查询和替换数据同set_contact_info
submit_db_table_info5 = {"db": "shoufuyou_reporting", "tb": "sms"}

# 上报设备指纹 库-表
submit_db_table_info3 = {"db": "shoufuyou_crcs", "tb": "deviceFingerprintLog7Day"}
# 默认请求加密数据org初始值user_id=111111126112需要替换落库明文
set_device_finger7d_info = {"org": {"user_id": "111111126112"},
                            "new": {"device_id": "{}", "user_id": "{}",
                                    "created_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}}
# -查询和替换数据同set_device_finger7d_info
submit_db_table_info4 = {"db": "shoufuyou_crcs", "tb": "deviceFingerprint"}


def mongo_del(id_card, id_card_origin):
    """
    db_info = {"db": "shoufuyou_reporting", "coll": "plan"}
    :return:
    """
    shou_db = {"db": "shoufuyou_crcs", "coll": "challengeItemSaveLog"}
    sfy_cur = mongo_con.MongoHelp(shou_db)

    shou_db_person = {"db": "shoufuyou_crcs", "coll": "crcsCashPerson"}
    sfy_per_cur = mongo_con.MongoHelp(shou_db_person)

    report_db = {"db": "xinyongfei_reporting", "coll": "challengeItemSaveLog"}
    report_cur = mongo_con.MongoHelp(report_db)

    # mongo.shoufuyou_crcs ====>challengeltemSaveLog 根据用户身份证删除信息所有相关的信息
    # mongo.shoufuyou_crcs ====>deviceFingerprintLog 根据device删除信息所有相关的信息
    # mongo.shoufuyou_reporting库=====>gps表 , picinfo表, callRecord表     device_id
    id_card_info = {"id_card_number": id_card}
    try:
        res = sfy_cur.delete(id_card_info, flg=False)
        res2 = sfy_per_cur.delete(id_card_info, flg=False)
        print('删除结果res', res, '删除结果2', res2)
        return res
    except Exception as e:
        print("false because:-{}".format(e))
        return False


def mongo_find(biz_num):
    # 查找激活失败原因
    wrong_list = []
    wrong_db = {"db": "xinyongfei_rcs_decision", "coll": "rcsDecisionLog"}
    reason_cur = mongo_con.MongoHelp(wrong_db)
    try:
        biz_dic = {"biz_flow_number": "{}".format(biz_num)}
        res = reason_cur.find(biz_dic)
        print(res['decision'])
        sum_rule = res['hit_rule_sets'].__len__()
        for i in range(sum_rule):
            rule_score = res['hit_rule_sets'][i]['rule_set_score']
            if rule_score > 0:
                risk_reason = res['hit_rule_sets'][i]['hit_rules'][0]['rule_name']
                wrong_list.append(risk_reason)
        return wrong_list
    except Exception as e:
        print("当前无法获取结果,因为{}".format(e))
        return False


