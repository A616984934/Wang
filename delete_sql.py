import server_info
import mysql_con


# --------------平台相关数据清除--------------------

# ---节点1：贷前----------

# 数据库名称
xyf_open_platform = "xyf_open_platform"

"""
基础数据获取
"""

# 手机号获取user_id
user_ids = "SELECT `user_id` FROM `xyf_service_user`.`xyf_user` WHERE `mobile` = '{}' limit 10;"

# 获取open游标
sql_open_plat = mysql_con.OperateMysql(xyf_open_platform)


def get_id(user_id, env='sit', id_num=''):
    # 获取加密后的原始身份证
    q_no = '123'
    servers = "默认服务器"

    id_card_protyle = "SELECT id_card_protyle FROM `xyf_open_platform`.`user_identify_ocr` WHERE `user_id` = {}".format(user_id)
    id_res = sql_open_plat.select_first_data(id_card_protyle)

    if env == "sit":
        servers = "https://sit-api.testxinfei.cn/data-center/user/id-get?q_no={}".format(q_no)
    elif env == "qa1":
        servers = "https://qa1-api.testxinfei.cn/data-center/user/id-get?q_no={}".format(q_no)

    id_card = id_num
    rel_card = '无法获取到对应的原始身份证'
    if id_res is not None:
        rel_card = id_res.get('id_card_protyle')
        info = {
            "id_card_protyle": rel_card,
            "key": "test-D0Ujo6bTtABiF4C2"
        }
        id_card = server_info.id_card_get(servers, info)

    return id_card, rel_card


# 平台Sdk贷前认证
def del_before_platform(Users, phone, id_card_number="1234"):
    """
    :param Users: 用户id组成的列表
    :param phone: 手机号
    :return:
    """
    sync_old_user_info = "DELETE FROM `xyf_open_platform`.`sync_old_user_info` WHERE `user_id` in {}".format(Users)

    user_check = "DELETE FROM `xyf_open_platform`.`user_check` WHERE `user_id` in {}".format(Users)

    user_identify_ocr = "DELETE FROM `xyf_open_platform`.`user_identify_ocr` WHERE `user_id` in {}".format(Users)

    user_identify_live = "DELETE FROM `xyf_open_platform`.`user_identify_live` WHERE `user_id` in {}".format(Users)

    user_identify_person = "DELETE FROM `xyf_open_platform`.`user_identify_person` WHERE `user_id` in {}".format(Users)

    cash_out_apply = "DELETE FROM `shoufuyou_v2`.`cash_out_apply` WHERE `mobile` = '" + phone + "' "

    user_bind_card = "DELETE FROM `xyf_open_platform`.`user_bind_card` WHERE `mobile` = '" + phone + "'"

    user_risk_level = "DELETE FROM  `xyf_open_platform`.`user_risk_level` WHERE `user_id` in {}".format(Users)

    distribute = "DELETE FROM  `xyf_open_platform`.`distribute` WHERE `user_id` in {}".format(Users)

    user_additional = "DELETE FROM  `xyf_open_platform`.`user_additional` WHERE `user_id` in {}".format(Users)

    # 用户中心记录
    del_server_user = "DELETE FROM  `xyf_service_user`.`xyf_user` WHERE `mobile` = '{}'".format(phone)

    dialog_confirm_record = "DELETE FROM  `xyf_open_platform`.`dialog_confirm_record` WHERE `user_id` in {}".format(Users)

    # 预授信激活，
    user_credit_apply = "DELETE FROM  `xyf_open_platform`.`user_credit_apply`  WHERE `user_id` in {}".format(Users)
    user_order = "DELETE FROM `xyf_open_platform`.`user_order` WHERE `user_id` in {}".format(Users)

    # 非默认的情况下执行此sql
    CashActivationLog = "DELETE FROM `shoufuyou_risk`.`CashActivationLog` WHERE `id_card_number` = '" + id_card_number +"'"

    # ocr_rz = "DELETE FROM `shoufuyou_risk`.`CashActivationLog` WHERE `user_id` in {}".format(Users)

    sql_list = [sync_old_user_info, user_check, user_order, user_identify_ocr, user_identify_live, user_identify_person,
                cash_out_apply, user_bind_card, user_risk_level, distribute, user_additional, dialog_confirm_record,user_credit_apply, del_server_user,] # ocr_rz]

    if id_card_number != 1234:
        sql_list.append(CashActivationLog)

    for i in sql_list:
        print('当前执行sql: {}'.format(i))
        sql_open_plat.del_data(i)
    message = 'delete mobile success'
    return message


def del_after_platform(phone):
    user_order="DELETE FROM `xyf_open_platform`.`user_order` WHERE `user_id` in (SELECT user_id FROM `xyf_service_user`.`xyf_user` WHERE `mobile` = '"+phone+"')"

    cash_out_loan_order="DELETE FROM `shoufuyou_v2`.`cash_out_loan_order` WHERE `ua` = 'xyfpt'  AND `user_id` = (SELECT id FROM `shoufuyou_v2`.`credit_user` WHERE `mobile` = '"+phone+"' AND  app='xyf01' )"

    CashLoanOrder="DELETE FROM `shoufuyou_v2`.`CashLoanOrder` WHERE `mobile` = '"+phone+"' "

    fund_loan_order="DELETE FROM `shoufuyou_fund`.`fund_loan_order` WHERE `mobile` = '"+phone+"'"

    CashBill= "DELETE  FROM `shoufuyou_v2`.`CashBill` WHERE `user_id` in  (SELECT id FROM `shoufuyou_v2`.`credit_user` WHERE `mobile` = '"+phone+"' AND  app='xyf01')"

    sql_list = [user_order, cash_out_loan_order, CashLoanOrder, fund_loan_order, CashBill]

    for i in sql_list:
        print('当前执行sql: {}'.format(i))
        sql_open_plat.del_data(i)
    message = 'delete mobile success'
    return message


def reset_bill(ord_nums, user_id, mobile):

    # 重新放款
    order_reset = "UPDATE shoufuyou_v2.`CashLoanOrder` SET `remit_status` = 'none'  WHERE `order_number`  = {}".format(ord_nums)
    delete_bill = "DELETE  FROM `CashBill` WHERE `user_id` = {}".format(user_id)

    change_fund_status = "UPDATE  shoufuyou_fund.`fund_loan_order` SET STATUS=60, status_history='1,10,20,30,40,50,60', `remit_status` = 'pending', `message` = '', `failed_reason` ='' WHERE `order_number` = {}".format(ord_nums)

    login_status = "UPDATE `credit_user` SET `last_login_time` = '2022-01-11 11:47:55' WHERE `mobile` = {}".format(mobile)

    login2 = "UPDATE `credit_user` SET `last_login_time` = NULL WHERE `mobile` = {}".format(mobile)

    bill_update = [order_reset, change_fund_status, login_status, login2]
    try:
        for i in bill_update:
            sql_open_plat.update_data(i)

        sql_open_plat.del_data(delete_bill)

        return "Success to update order"

    except Exception as e:
        return "false {}".format(e)


if __name__ == '__main__':
    # del_before_platform('dict', '12323')
    # s = sql_open_plat.select_all_data(user_id.format('13761709401'))
    # phone = '13011196605'
    # del_server_user = "DELETE FROM  `xyf_service_user`.`xyf_user` WHERE `mobile` = '{}'".format(phone)
    # # sql_ser = projects.tools.mysql_con.OperateMysql('xyf_service_user')
    # # res = sql_ser.del_data(del_server_user)
    # # print(res)
    # res = sql_open_plat.del_data(del_server_user)
    # print('xxxxx',res)
    us = '111111133992'
    id2, id_cd2 = get_id(us, env='sit')
