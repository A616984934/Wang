import pymysql, json, datetime, logging
from readConfig import ReadConfig


class DateEncoder(json.JSONEncoder):
    """重写dump json默认无法处理字典中datetime"""
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


class OperateMysql(object):
    def __init__(self, db, dbs_name='', t_env='sit', port=3306):
        """
        数据库初始化连接
        :param db: mysql_sql.py文件配置
        :env 默认环境sit
        """

        self.connect_interface_testing = pymysql.connect(
            host="{}".format(ReadConfig(db_name=dbs_name, env=t_env).get_mysql("host")),
            user="{}".format(ReadConfig(db_name=dbs_name, env=t_env).get_mysql("user")),
            passwd="{}".format(ReadConfig(db_name=dbs_name, env=t_env).get_mysql("password")),
            port=int("{}".format(ReadConfig(db_name=dbs_name, env=t_env).get_mysql("port"))),
            database="{}".format(db),
            charset='{}'.format(ReadConfig(db_name=dbs_name, env=t_env).get_mysql("charset")),
            cursorclass=pymysql.cursors.DictCursor
        )

        # 创建游标操作数据库
        self.cursor_interface_testing = self.connect_interface_testing.cursor()

    def select_first_data(self, sql):
        """
        查询第一条数据
        """
        try:
            # 执行 sql 语句
            self.connect_interface_testing.ping(reconnect=True)
            self.cursor_interface_testing.execute(sql)
        except Exception as e:
            print("执行sql异常:%s" % e)
        else:
            # 获取查询到的第一条数据
            first_data = self.cursor_interface_testing.fetchone()
            logging.info("查询结果:{}".format(first_data))
            # print(first_data)
            # 将返回结果转换成 str 数据格式，禁用acsii编码
            # first_data = json.dumps(first_data, ensure_ascii=False, cls=DateEncoder)
            # self.connect_interface_testing.close()
            return first_data

    def select_all_data(self, sql):
        """
        查询结果集
        """
        try:
            self.connect_interface_testing.ping(reconnect=True)
            res = self.cursor_interface_testing.execute(sql)

        except Exception as e:
            print("执行sql异常:%s" % e)
        else:
            first_data = self.cursor_interface_testing.fetchall()
            # first_data = json.dumps(first_data, ensure_ascii=False, cls=DateEncoder)
            self.connect_interface_testing.close()
            return first_data

    def del_data(self, sql):
        """
        删除数据
        """
        res = {}
        try:
            # 执行SQL语句
            self.connect_interface_testing.ping(reconnect=True)

            result = self.cursor_interface_testing.execute(sql)
            print('xxxxxx', result)
            if result != 0:
                # 提交修改
                self.connect_interface_testing.commit()
                res = {'删除成功'}
            else:
                res = {'没有要删除的数据'}
        except:
            # 发生错误时回滚
            self.connect_interface_testing.rollback()
            res = {'删除失败'}
        return res

    def update_data(self, sql):
        """
        修改数据
        """
        try:
            self.connect_interface_testing.ping(reconnect=True)
            logging.info("mysql执行sql:{}".format(sql))
            self.cursor_interface_testing.execute(sql)
            re = self.connect_interface_testing.commit()
            res = {'更新成功====',re}
        except Exception as e:
            self.connect_interface_testing.rollback()
            res = '更新异常,原因是{}'.format(e)
        return res

    def insert_data(self, sql, data=None):
        """
        新增数据
        """
        try:
            self.connect_interface_testing.ping(reconnect=True)
            logging.info("mysql执行sql:{}".format(sql))
            # self.cursor_interface_testing.execute(sql, data)
            self.cursor_interface_testing.execute(sql)
            self.connect_interface_testing.commit()
            res = {data, '新增成功'}

        except Exception as e:
            res = {'新增失败', e}
        return res

    def conn_close(self):
        # 关闭游标
        self.cursor_interface_testing.close()
        # 关闭数据库
        self.connect_interface_testing.close()


if __name__ == "__main__":
    env = 'sit'
    # 默认传递sit环境
    a = OperateMysql('shoufuyou_v2')



