import mysql_con
import server_info

"""
信贷信息删除
"""

# --------------xx业务------------
# 信贷库
sfy_v2_db_info = "shoufuyou_v2"
# 信贷风控
sfy_v2_db_risk = "shoufuyou_risk"
# 资金单独库
sfy_v2_db_fund = "shoufuyou_fund"


class Xd_sql(object):

    def __init__(self, env='sit'):
        self.sql_v2 = mysql_con.OperateMysql(sfy_v2_db_info, t_env=env)
        self.sql_risk = mysql_con.OperateMysql(sfy_v2_db_risk, t_env=env)
        # self.sql_fund = mysql_con.OperateMysql(sfy_v2_db_fund, t_env=env)

    def all_v2_delete(self, id_num, mobile):
        res = ""

        user_del_sql = "DELETE  FROM  shoufuyou_v2.`User` WHERE mobile = '{}' ".format(mobile)

        credit_del_sql = "DELETE FROM shoufuyou_v2.`credit_user` WHERE mobile = '{}' ".format(mobile)

        # 删除二一致认证
        Person_del_sql = "DELETE FROM shoufuyou_v2.`Person` where `id_card_number` = '{}' ".format(id_num)

        Application2 = "delete from Application2 WHERE `mobile` ='{}'".format(mobile)

        Applicationlog = "delete from ApplicationLog WHERE `mobile` ='{}'".format(mobile)

        Actcivalog = "delete from Activation WHERE `mobile` ='{}'".format(mobile)

        userext = "DELETE FROM shoufuyou_v2.user_access_ext WHERE id_card_number ='{}' ".format(id_num)

        ocr_del_sql = "DELETE FROM shoufuyou_v2.`FaceIdCard` where `mobile` = '{}'".format(mobile)

        face_del_sql = "delete from shoufuyou_v2.FaceVerify WHERE `mobile` ='{}'".format(mobile)

        bank_card = "DELETE FROM shoufuyou_v2.BankCardInfo WHERE id_card_number ='{}'".format(id_num)

        bank_record = "DELETE FROM shoufuyou_v2.BankCardRecord WHERE id_card_number ='{}'".format(id_num)

        user_judge = "DELETE FROM shoufuyou_v2.UserJudge WHERE `mobile` = '{}'".format(mobile)

        fas_bank = "DELETE FROM shoufuyou_fas.FasBankCard WHERE user_name IN (SELECT DISTINCT(NAME) FROM shoufuyou_fas.Account WHERE cert_no ='{}')".format(id_num)

        fas_psn = "DELETE FROM shoufuyou_fas.FasPsnlAcntInf WHERE cert_no ='{}'".format(id_num)

        fas_account = "DELETE FROM shoufuyou_fas.Account WHERE cert_no ='{}'".format(id_num)

        # =============================《信贷》贷中，贷后==================================================

        o1 = "DELETE FROM shoufuyou_v2.CashLoanOrder WHERE id_card_number ='{}' ".format(id_num)

        o2 = "DELETE FROM shoufuyou_v2.CashRepayment WHERE id_card_number ='{}' ".format(id_num)

        # bank_record = "DELETE FROM shoufuyou_v2.BindCardRecord WHERE id_card_number ={}".format(id_card)
        # ====================================================================================
        cashlao = "DELETE FROM shoufuyou_v2.CashLaowangClick WHERE id_card_number ='{}'".format(id_num)

        cashRepayment = "DELETE FROM shoufuyou_v2.CashRepaymentDetail WHERE bill_number IN ( SELECT bill_number  FROM `CashBill` WHERE `id_card_number` = '{}'".format(
            id_num)

        cashque = "DELETE FROM shoufuyou_v2.CashRepaymentQueue WHERE order_number IN ( SELECT DISTINCT(order_number) FROM `CashBill` WHERE `id_card_number` = '{}'".format(
            id_num)

        cashbill = "DELETE FROM shoufuyou_v2.CashBill WHERE id_card_number ='{}'".format(id_num)

        cashprofit = "DELETE FROM shoufuyou_v2.CashProfitOrder WHERE id_card_number = '{}'".format(id_num)

        cashtrade = "DELETE FROM shoufuyou_v2.CashProfitTrade WHERE id_card_number ='{}'".format(id_num)

        cash_loan_ord = "DELETE FROM shoufuyou_v2.cash_out_loan_order WHERE order_no IN ( SELECT order_no FROM cash_out_apply WHERE mobile = '{}') ".format(
            mobile)

        cash_loan_ord2 = "DELETE FROM shoufuyou_v2.cash_out_order_reg WHERE order_no IN ( SELECT order_no FROM cash_out_apply WHERE mobile = '{}') ".format(
            mobile)

        cash_apply = "DELETE FROM shoufuyou_v2.cash_out_apply WHERE id_card_number ='{}'".format(id_num)

        risk_CashActivationLog = "DELETE FROM shoufuyou_risk.CashActivationLog WHERE id_card_number ='{}'".format(id_num)

        risk_CashCreditLineApplyLog2 = "DELETE FROM shoufuyou_risk.CashCreditLineApplyLog2 WHERE id_card_number={}".format(id_num)

        # user_del_sql, credit_del_sql,
        sql_list = [user_del_sql, credit_del_sql, Person_del_sql, cash_loan_ord, cash_loan_ord2, cash_apply,
                    Application2, Applicationlog, Applicationlog, o1, o2, userext, ocr_del_sql, face_del_sql, bank_card,
                    bank_record, cashlao, cashRepayment, cashque, cashbill, cashprofit, cashtrade, user_judge, fas_bank,
                    fas_psn, fas_account, Actcivalog, bank_record, risk_CashActivationLog, risk_CashCreditLineApplyLog2]

        for i in sql_list:
            res = self.sql_v2.del_data(i)
        if res != "":
            return res

    # 信贷激活前，节点数据删除
    def before_xd(self, id_num, mobile):
        res = ''
        # 删除User表用户信息
        user_del_sql = "DELETE FROM shoufuyou_v2.`User` WHERE mobile = '{}' ".format(mobile)

        credit_del_sql = "DELETE FROM shoufuyou_v2.`credit_user` WHERE mobile = '{}' ".format(mobile)

        Person_del_sql = "DELETE FROM shoufuyou_v2.`Person` where `id_card_number` = '{}' ".format(id_num)

        Application2 = "delete from Application2 WHERE `mobile` ='{}'".format(mobile)

        Application_log = "delete from ApplicationLog WHERE `mobile` ='{}'".format(mobile)

        Activation = "delete from Activation WHERE `mobile` ='{}'".format(mobile)

        user_ext = "DELETE FROM shoufuyou_v2.user_access_ext WHERE id_card_number ='{}' ".format(id_num)

        ocr_del_sql = "DELETE FROM shoufuyou_v2.`FaceIdCard` where `mobile` = '{}'".format(mobile)

        face_del_sql = "delete from shoufuyou_v2.FaceVerify WHERE `mobile` ='{}'".format(mobile)

        bank_card = "DELETE FROM shoufuyou_v2.BankCardInfo WHERE id_card_number ='{}'".format(id_num)

        bank_record = "DELETE FROM shoufuyou_v2.BankCardRecord WHERE id_card_number ='{}'".format(id_num)

        fas_bank = "DELETE FROM shoufuyou_fas.FasBankCard WHERE user_name IN (SELECT DISTINCT(NAME) FROM shoufuyou_fas.Account WHERE cert_no ='{}')".format(
            id_num)

        fas_psn = "DELETE FROM shoufuyou_fas.FasPsnlAcntInf WHERE cert_no ='{}'".format(id_num)

        fas_account = "DELETE FROM shoufuyou_fas.Account WHERE cert_no ='{}'".format(id_num)

        risk_CashActivationLog = "DELETE FROM shoufuyou_risk.CashActivationLog WHERE id_card_number ='{}'".format(id_num)
        risk_CashCreditLineApplyLog2 = "DELETE FROM shoufuyou_risk.CashCreditLineApplyLog2 WHERE id_card_number={}".format(id_num)

        person_info = [user_del_sql, credit_del_sql, Person_del_sql, Application_log, Application2, Activation,
                       user_ext, ocr_del_sql, face_del_sql, bank_card, bank_record, fas_bank, fas_psn,
                       fas_account, risk_CashActivationLog, risk_CashCreditLineApplyLog2]

        for i in person_info:
            res = self.sql_v2.del_data(i)
        print('是否执行成功m,{}'.format(res))
        if res != '':
            return res

    # 激活后->获取到的所有数据
    def after_platform(self, id_num, mobile):
        res = "删除下单数据结果是"
        cash_apply = "DELETE FROM shoufuyou_v2.cash_out_apply WHERE id_card_number ='{}'".format(id_num)

        cashlao = "DELETE FROM shoufuyou_v2.CashLaowangClick WHERE id_card_number ='{}'".format(id_num)

        cashRepayment = "DELETE FROM shoufuyou_v2.CashRepaymentDetail WHERE bill_number IN ( SELECT bill_number  FROM `CashBill` WHERE `id_card_number` = '{}'".format(
            id_num)

        cashque = "DELETE FROM shoufuyou_v2.CashRepaymentQueue WHERE order_number IN ( SELECT DISTINCT(order_number) FROM `CashBill` WHERE `id_card_number` = '{}'".format(
            id_num)

        cashbill = "DELETE FROM shoufuyou_v2.CashBill WHERE id_card_number ='{}'".format(id_num)

        cashprofit = "DELETE FROM shoufuyou_v2.CashProfitOrder WHERE id_card_number = '{}'".format(id_num)

        cashtrade = "DELETE FROM shoufuyou_v2.CashProfitTrade WHERE id_card_number ='{}'".format(id_num)

        cash_loan_ord = "DELETE FROM shoufuyou_v2.cash_out_loan_order WHERE order_no IN ( SELECT order_no FROM cash_out_apply WHERE mobile = '{}') ".format(
            mobile)

        cash_loan_ord2 = "DELETE FROM shoufuyou_v2.cash_out_order_reg WHERE order_no IN ( SELECT order_no FROM cash_out_apply WHERE mobile = '{}') ".format(
            mobile)

        sql_list = [cash_apply, cashlao, cashtrade, cashque, cashRepayment, cashbill, cashprofit, cash_loan_ord2, cash_loan_ord]

        for i in sql_list:
            res = self.sql_v2.del_data(i)
        if res != "":
            return res

    def bill_rest(self, order_num, id_num):
        # 账单还原
        res = ""
        init_bill = "UPDATE shoufuyou_v2.`CashBill` SET fund_paid_time='NULL' WHERE order_number= '{}'".format(
            order_num)

        init_loan = "update shoufuyou_fund.fund_loan_order  set `status`='0',remit_status='failed' WHERE  order_number = '{}'".format(order_num)

        init_cashorder = "update shoufuyou_v2.`CashLoanOrder`  set remit_status='failed', status='reject' WHERE order_number = '{}'".format(
            order_num)

        ll = [init_bill, init_loan, init_cashorder]

        for i in ll:
            res = self.sql_v2.update_data(i)
        return res

    def report_del(self, mobile):
        face_del_sql = "delete from FaceVerify WHERE `mobile` ='{}'".format(mobile)
        risk_del = "DELETE FROM shoufuyou_risk.`CashActivationLog` where `mobile` = '{}'".format(mobile)
        res = self.sql_v2.del_data(risk_del)

    def xd_user_get(self, order_num):
        order_user_id = "SELECT `user_id` FROM `shoufuyou_v2`.`CashLoanOrder` WHERE `order_number` = '{}' limit 10;".format(order_num)
        user_id = self.sql_v2.select_first_data(order_user_id)['user_id']
        order_user_id_card = "SELECT `id_card_number` FROM `shoufuyou_v2`.`CashLoanOrder` WHERE `order_number` = '{}' limit 10;".format(order_num)
        id_card = self.sql_v2.select_first_data(order_user_id_card)['id_card_number']

        return user_id, id_card


if __name__ == "__main__":
    # ord = '320324199007237012'
    # mobiles = '18500000888'

    or2 = '20200829114743021256011'
    xd = Xd_sql(env='sit')
    x1, x2 = xd.xd_user_get(or2)
    print(x1, x2)












# --------------替换授信用户身份证------------
set_FaceIdCard_card = "UPDATE `FaceIdCard` SET `id_card_number` = '{}' where mobile='{}'"
# 修改预授信记录身份证
set_Application2_card = "update Application2 set `id_card_number` = '{}' where mobile='{}'"
set_Application2log_card = "update CashCreditLineApplyLog2 set `id_card_number` = '{}' where mobile='{}'"
# 修改人脸识别结果
set_face_result = "update FaceVerify set `liveness_decision` ='PASS', `verify_decision`='PASS', `decision` ='PASS', `id_card_number` = '{}' where `mobile` = '{}'"

# --------------查询用户id------------
# 查询user表用户id
query_user_id = "SELECT id FROM `User` WHERE `mobile` = '{}' and `utm_source` = '{}'"
# 查询身份证号码是否存在
query_card_id = "select id from `FaceIdCard` where id_card_number='{}' and `app`='{}' "

# --------------添加资金白名单------------
# 插入白名单
add_cash_white_sql = "INSERT INTO `fund_cash_pool_white_list` (`name`, `mobile`, `fund_source`)VALUES ('{}', '{}', '{}') "
# 查询插入白名单
query_cash_white_sql = "select id from fund_cash_pool_white_list where mobile='{}' "

# --------放款--------
# 查询用户借款订单 和 所属资金
query_order_cash_sql = "select order_number,fund_source from CashLoanOrder where mobile='{}' order by id desc"
# 查询借款订单进度 99为放款成功
query_loan_status_sql = "SELECT status,message FROM fund_loan_order  where `order_number` = '{}'"