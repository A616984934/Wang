# -*- coding: UTF-8 -*-
# cython: language_level=3

from pymongo import MongoClient
import logging
from readConfig import ReadConfig
from urllib import parse

db_info = {"db": "shoufuyou_reporting", "coll": "plan"}


class MongoHelp(object):
    def __init__(self, db_table_info, t_env='sit'):
        rf = ReadConfig(t_env)
        host = rf.get_mongo("host")
        user = rf.get_mongo("user")
        password = rf.get_mongo('password')
        port = 27017
        print('------', host,user,password,port, '=============')

        self.client = MongoClient(host=host, port=port, username=user, password=password)

        print(db_table_info.get("db"))

        # 数据库名称
        if db_table_info.get("db") in self.client.list_database_names():
            self.col = self.client[db_table_info.get("db")]
        else:
            print("数据库并不存在，创建新的数据库")

        # 数据库数据集合
        collection = db_table_info.get("coll")
        self.col = self.col[collection]

        # db1 = self.client.shoufuyou_reporting // connect 2

    def get_info(self):
        # get current database collection
        self.coll_list = self.col.list_collection_names()
        print("--------", self.coll_list)

    def insert(self, data, flg=True):
        if flg:
            if isinstance(data, dict):
                ret = self.col.insert_one(data)
                return ret

        elif isinstance(data, list):
            for i in data:
                if not isinstance(i, dict):
                    return
            ret = self.col.insert_many(data)
            print("插入数据的id" + ret.inserted_id)
            return ret
        else:
            return "数据格式为dict或者[{},{}]形式的列表但你传入的是%s," % type(data)

    def created(self, database_name=None, collection_name=None, data="a"):
        # create new database and new collection
        if database_name == None:
            # insert a new collection to database
            self.new_coll = self.col[collection_name]
            self.new_coll.insert(data)
            return "在当前数据库创建新的集合成功"
        else:
            self.new_db = self.client[database_name]
            self.new_coll = self.new_db[collection_name]
            res = self.new_coll.insert(data)
            if res != None:
                return res

    def find(self, data, flg=True):
        """查找数据"""
        try:
            if flg:
                rt = self.col.find_one(data)  # 查一条数
                return rt
            else:
                rt = self.col.find(data)  # 查多条数据
                result = []
                for i in rt:
                    result.append(i)
                return result
        except Exception:
            return "查询数据格式有误"

    def update(self, org_data, new_data, flg=True):  # flg = True  只更新一条
        "将匹配目标的字段修改"
        logging.info("mongodb执行更新:org:{} new:{}".format(org_data, new_data))
        if flg:

            ret = self.col.update_one(org_data, {"$set": new_data})  # 只更新一条
            return ret
        else:
            ret = self.col.update_many(org_data, {"$set": new_data})  # 更新全部数据
            return ret

    def delete(self, data, flg=True):
        """删除数据"""
        if flg:
            ret = self.col.delete_one(data)
            return ret
        else:
            ret = self.col.delete_many(data)
            return ret

    def close_conn(self):
        """关闭连接"""
        self.client.close()

if __name__ == '__main__':
    mongo = MongoHelp(db_info)
    # data=[{"name":"自动化测试1"},{"name":"自动化测试2"},{"name":"自动化测试3"}]
    data1 = {"event_id": "100020"}
    ret = mongo.insert(data1)
#     # ret=MongoHelp.update({"name" : "流血的仕途" },{"name":"我的程序之路"})
#     # print(ret)
#     # ret = MongoHelp.delete({"name": "我的程序之路"})
#     # print(ret)
#     res = MongoHelp.find({'user_id': '111111111142012', "device_id": "20201202272085bd7"}, flg=False)
#     print(res)
#     # print(res.get("bank_card_number"))
