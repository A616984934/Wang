# -*- coding: UTF-8 -*-
# cython: language_level=3

import flask, json
from flask import request, jsonify
import requests
import subprocess
# import Mongo_sql
import redis
from flask_cors import CORS
import delete_sql, xindai_sql
from mongo_sql import mongo_del
import mongo_con
import redis_con
import server_info

xd = xindai_sql.Xd_sql()
redis_con = redis_con.RedisConnect()
op_sql = delete_sql.Open_plat()

server = flask.Flask(__name__)
CORS(server, supports_credentials=True)
# server.config['JSON_AS_ASCII'] = False
# @server.route()可以将普通函数转变为服务 登录接口的路径、请求方式

java_test = "http://10.10.100.25:6010"
php_test1 = "http://10.10.100.23:6010"
php_test2 = "http://10.10.100.24:6010"
python_test1 = "http://10.10.100.26:6010"
python_test_qtz = "http://10.10.100.22:6010"
qa1_php_1 = "http://10.10.102.38:6010"
sit_java_1 = "http://10.10.100.28:6010"
sit_php_1 = "http://10.10.100.27:6010"
sit_python_1 = "http://10.10.100.29:6010"

new_dict = {"java_test": java_test, "php_test1": php_test1, "php_test2": php_test2, "python_test1": python_test1,
            "python_test_qtz": python_test_qtz, "qa1_php_1": qa1_php_1, "sit_java_1": sit_java_1,
            "sit_php_1": sit_php_1, "sit_python_1": sit_python_1}


def command_exec_ext(command, timeout=5, cwd=None, wait=True):
    try:
        comp = subprocess.run(command, timeout=timeout,
                              stdout=subprocess.PIPE if wait else None,
                              shell=True,
                              cwd=cwd,
                              stderr=subprocess.STDOUT,
                              universal_newlines=True)
        if not wait:
            return None
        result_lines = comp.stdout.splitlines()
        strip_lines = []
        for line in result_lines:
            sl = line.strip()
            if sl:
                strip_lines.append(sl)
        return (comp.returncode, strip_lines)
    except Exception as e:
        print('fail', '测试失败: %s' % (str(e),))
        return None


def server_post(server_name, info):
    # 调用同级服务
    message = ''
    server_name1 = server_name + "/script"
    res1 = requests.post(server_name1, json=info)
    res = res1.text.encode('utf-8').decode('unicode_escape')

    if res is None:
        message = "server connect wrong"
        return message
    else:
        message = res
        return message


@server.route("/restore_account", methods=['POST'])
def delete_restore():
    """
    回复账号状态
    """
    users = []
    if not request.data:
        return "script fails"
    recognize_info = request.data.decode('utf-8')
    del_info = json.loads(recognize_info)
    mobile_num = del_info["account_num"]
    app_name = del_info["app_name"]
    account_status = del_info["account_status"]
    id_card = del_info["id_card"]
    env = del_info["account_env"]

    id_card_origin = ''
    user_ids = op_sql.get_user_id(mobile_num)
    print('=--------=', user_ids)

    if id_card == '' and len(user_ids) > 1:
        id_card, id_card_origin = op_sql.get_id(user_ids[0], env=env, id_num=id_card)
    elif id_card != '':
        id_card_origin = op_sql.get_id_origin(id_num=id_card)

    try:
        if account_status == '外部api':
            mongo_del(id_card=id_card, id_card_origin="1234")
            xd.all_v2_delete(id_card, mobile_num)
            redis_con.delete("mobile:{}".format(mobile_num))
            return "api--delete--success"

        if account_status == '注册-贷前':
            # 平台贷前sdk
            res = op_sql.del_before_platform(tuple(users) + (1, 2), mobile_num)
            # 信贷sdk，需要详细划分/贷前落表或者贷中，贷后落笔
            re2 = xd.before_xd(id_card, mobile_num)
            mongo_del(id_card=id_card, id_card_origin=id_card_origin)

        # 删除进件信息：//贷中，贷后 --->删除信贷sdk--信贷全部信息
        if account_status == '全节点删除':
            res = op_sql.del_after_platform(mobile_num)
            res2 = op_sql.del_before_platform(id_card, mobile_num)
            res3 = xd.all_v2_delete(id_card, mobile_num)
            redis_con.delete("jwt:{}:xyf01".format(mobile_num))
            redis_con.delete("mobile:{}".format(mobile_num))
            mongo_del(id_card=id_card, id_card_origin=id_card_origin)

        return jsonify({"message": "delete_info Success"})
    
    except Exception as e:
        print('出现异常,{}'.format(e))
        return jsonify({"message": "Delete wrong"})


@server.route("/restore_order", methods=['POST'])
def order_restore():
    order_info = json.loads(request.data.decode('utf-8'))
    order_type = order_info["type"]
    date_params = order_info["date_params"]
    order_num = order_info["order_num"]
    order_env = order_info["order_env"]
    order_name = '预设值'
    res = ''
    if order_type == '重新还款':
        order_name = 'init'
        xd.fund_repay(order_num=order_num)

    elif order_type == "还款日期":
        order_name = 'start_time'

    elif order_type == "删除订单":
        # 添加删除所有订单
        return jsonify({"message": "delete order success"})
    try:
        # 'param': date_params,
        order_detail = {
            'type': order_name,
            'order_number': order_num,
            'param': date_params
        }
        res = server_info.form_model(order_restore, order_detail).encode('raw_unicode_escape').decode('utf-8')
        return jsonify({"message": " order restore success"})
    except Exception as e:
        print('wrong because %s' % e)


@server.route("/redis", methods=['POST'])
def redis_api():
    if not request.data:
        return "script fails"
    recognize_info = request.data.decode('utf-8')
    xx = json.loads(recognize_info)
    db_name = xx['db_name']
    meth = xx['method']
    hash_name = xx['hash_name']
    key = xx['key']
    value = xx['value']

    try:
        # 通道
        pool = redis.ConnectionPool(host="redis.testxinfei.cn", port=6379, password='#8keAh!dF%PZedAIShr72n',
                                    db=db_name,
                                    decode_responses=True)
        con = redis.Redis(connection_pool=pool)
        # 批量执行命令-创建通道,将数据加入通道执行
        # pipe = con.pipeline()
        # pipe.hget("name").hget("haha").execute()
        re1 = "操作数据库为{}+目标hash{}+操作key{}".format(db_name, hash_name, key)
        if meth == "change":
            # insert and update
            con.hset(hash_name, key, value)
        if meth == "insert_many":
            con.hmset(hash_name, mapping="")
        if meth == "delete_string":
            con.delete(key)
        if meth == "delete":
            # delete key in hash
            con.hdel(hash_name, "1")
        if meth == "get":
            # re1 = con.hget(hash_name, key="")
            """默认批量取出数据,"""
            con.hmget(hash_name, keys=key)
        if meth == "get_all":
            con.hgetall(hash_name)
        re1 = con.hget(hash_name, key)
        return jsonify(re1)
    except Exception as e:
        return "can't connect redis--reason: {}".format(e)


@server.route("/mongo", methods=['POST'])
def mongo_con():
    if not request.data:
        return "script fails"
    recognize_info = request.data.decode('utf-8')
    xx = json.loads(recognize_info)

    print('当前请求信息: ------{}'.format(xx))
    database = xx['database']
    collection = xx['collection']
    meth = xx['meth']
    aim_data = xx['data']
    da_info = {"db": database, "col": collection}
    old = xx['aim_data']
    mongo_conn = mongo_con.MongoHelp(da_info)

    if meth == "insert":
        re1 = mongo_conn.insert(aim_data)
    if meth == "delete":
        re1 = mongo_conn.delete(aim_data)
    if meth == "find":
        re1 = mongo_conn.find(aim_data)

    if meth == "updated" and old != "":
        re1 = mongo_conn.update(org_data=old, new_data=aim_data)
    if meth == "created":
        re1 = mongo_conn.created(database, collection, data=aim_data)
    res = "执行命令成功"
    return res


@server.route("/vv", methods=['GET'])
def xxx():
    return "this is a test server"


if __name__ == '__main__':
    server.run(debug=True, port=8050, host='0.0.0.0', threaded=True)  # 指定端口、host,0.0.0.0代表不管几个网卡，任何ip都可以访问

