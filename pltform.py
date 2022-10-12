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

xd = xindai_sql.Xd_sql()
redis_con = redis_con.RedisConnect()

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

    # 删除信息  ${new_mobile}
    res, re2 = '测试默认值', 'ss'
    users_id = delete_sql.user_ids.format(mobile_num)
    users_list = delete_sql.sql_open_plat.select_all_data(users_id)
    print('此手机号相关的user_id', users_list[0].get("user_id"))

    if len(users_list) == 0:
        return jsonify({"message": '已经不存在此手机相关数据'})
    else:
        # 获取加密后的身份证号码
        id_card_origin = delete_sql.get_id(users_list[0].get("user_id"), env=env)
        if id_card == '无法获取到对应的原始身份证':
            return u"失败"

    print('当前user_list-------{}'.format(users_list))
    # mongo基本信息
    for i in users_list:
        users.append(i['user_id'])

    if account_status == '注册-贷前':
        # 平台贷前sdk
        res = delete_sql.del_before_platform(tuple(users) + (1, 2), mobile_num)
        # 信贷sdk，需要详细划分/贷前落表或者贷中，贷后落笔
        re2 = xd.before_xd(id_card, mobile_num)
        mongo_del(id_card=id_card, id_card_origin=id_card_origin)

    # 删除进件信息：//贷中，贷后 --->删除信贷sdk--信贷全部信息
    if account_status == '全节点删除':
        res = delete_sql.del_after_platform(mobile_num)
        res2 = delete_sql.del_before_platform(id_card, mobile_num)
        res3 = xd.all_v2_delete(id_card, mobile_num)
        redis_con.delete("jwt:{}:xyf01".format(mobile_num))
        redis_con.delete("mobile:{}".format(mobile_num))
        mongo_del(id_card=id_card, id_card_origin=id_card_origin)

    print('删除账号信息结果', res, re2)
    return jsonify({"message": u'delete_info 成功'})


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
