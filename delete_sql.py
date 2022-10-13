import server_info
import mysql_con

# --------------平台相关数据清除--------------------

# 数据库名称
xyf_open_platform = "xyf_open_platform"

"""
基础数据获取
"""

sql_open_plat = mysql_con.OperateMysql(xyf_open_platform)


class Open_plat(object):
    sql_open_cur = sql_open_plat

    @staticmethod
    def get_user_id(mobile):
        users = []
        user_ids_sql = "SELECT `user_id` FROM `xyf_service_user`.`xyf_user` WHERE `mobile` = '{}' limit 10;".format(mobile)
        try:
            users_list = sql_open_plat.select_all_data(user_ids_sql)
            for i in users_list:
                users.append(i['user_id'])
            return users
        except Exception as e:
            return {"status": "false", "message": '无法获取users_id,因为{}'.format(e)}

    @staticmethod
    def get_id_origin(id_num):
        q_no = '123'
        servers = "https://sit-api.testxinfei.cn/data-center/user/id-put?q_no={}".format(q_no)
        info = {
            "id_card_no": id_num,
            "key": "test-D0Ujo6bTtABiF4C2"
        }
        id_card_md5 = server_info.id_card_get(servers, info)['id_card_protyle']
        return id_card_md5

    @staticmethod
    def get_id(user_id, env='sit', id_num=''):
        q_no = '123'
        servers = "默认服务器"
        id_card_origin = "SELECT id_card_protyle FROM `xyf_open_platform`.`user_identify_ocr` WHERE `user_id` = {}".format(
            user_id)
        id_res = sql_open_plat.select_first_data(id_card_origin)

        if env == "sit":
            servers = "https://sit-api.testxinfei.cn/data-center/user/id-get?q_no={}".format(q_no)
        elif env == "qa1":
            servers = "https://qa1-api.testxinfei.cn/data-center/user/id-get?q_no={}".format(q_no)

        id_card = id_num
        t_card = '无法获取到对应的脱敏身份证'
        if id_res is not None:
            t_card = id_res.get('id_card_protyle')
            info = {
                "id_card_protyle": t_card,
                "key": "test-D0Ujo6bTtABiF4C2"
            }
            id_card = server_info.id_card_get(servers, info)['id_card_no']
        return id_card, t_card

    # 平台Sdk贷前认证
    @staticmethod
    def del_before_platform(Users, phone, id_card_number="1234"):
        """
        :param id_card_number:
        :param Users: 用户id组成的列表
        :param phone: 手机号
        :return:
        """
        sync_old_user_info = "DELETE FROM `xyf_open_platform`.`sync_old_user_info` WHERE `user_id` in {}".format(Users)

        user_check = "DELETE FROM `xyf_open_platform`.`user_check` WHERE `user_id` in {}".format(Users)

        user_identify_ocr = "DELETE FROM `xyf_open_platform`.`user_identify_ocr` WHERE `user_id` in {}".format(Users)

        user_identify_live = "DELETE FROM `xyf_open_platform`.`user_identify_live` WHERE `user_id` in {}".format(Users)

        user_identify_person = "DELETE FROM `xyf_open_platform`.`user_identify_person` WHERE `user_id` in {}".format(Users)

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

        # 现金贷激活日志
        CashActivationLog = "DELETE FROM `shoufuyou_risk`.`CashActivationLog` WHERE `id_card_number` = '" + id_card_number +"'"

        sql_list = [sync_old_user_info, user_check, user_order, user_identify_ocr, user_identify_live, user_identify_person,
                    user_bind_card, user_risk_level, distribute, user_additional, dialog_confirm_record,user_credit_apply, del_server_user]

        if id_card_number != 1234:
            sql_list.append(CashActivationLog)

        for i in sql_list:
            print('当前执行sql: {}'.format(i))
            sql_open_plat.del_data(i)
        message = 'delete mobile success'
        return message

    @staticmethod
    def del_after_platform(phone):

        cash_out_loan_order="DELETE FROM `shoufuyou_v2`.`cash_out_loan_order` WHERE `ua` = 'xyfpt'  AND `user_id` = (SELECT id FROM `shoufuyou_v2`.`credit_user` WHERE `mobile` = '"+phone+"' AND  app='xyf01' )"

        CashLoanOrder="DELETE FROM `shoufuyou_v2`.`CashLoanOrder` WHERE `mobile` = '"+phone+"' "

        fund_loan_order="DELETE FROM `shoufuyou_fund`.`fund_loan_order` WHERE `mobile` = '"+phone+"'"

        CashBill = "DELETE  FROM `shoufuyou_v2`.`CashBill` WHERE `user_id` in  (SELECT id FROM `shoufuyou_v2`.`credit_user` WHERE `mobile` = '"+phone+"' AND  app='xyf01')"

        sql_list = [cash_out_loan_order, CashLoanOrder, fund_loan_order, CashBill]

        for i in sql_list:
            print('当前执行sql: {}'.format(i))
            sql_open_plat.del_data(i)
        message = 'delete mobile success'
        return message

    @staticmethod
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
    ids_card = '130526199310113643'
    us = '111111133992'
    op = Open_plat()
    id_cd2 = op.get_id_origin(ids_card)
    print(id_cd2)


