import configparser
import os
from Port_info import appConf


class ReadConfig:
    """定义一个读取配置文件的类"""

    def __init__(self, env='sit', filepath=None):
        self.env = env
        if filepath:
            self.configPath = filepath
        else:
            self.configPath = os.path.join(os.path.dirname(__file__) + os.sep + appConf.conf_path + "Port_info/config.ini")

        self.cf = configparser.ConfigParser()
        # 读取配置
        self.cf.read(self.configPath, encoding="utf-8")

        # 此方法无法识别替代符%
        self.rf = configparser.RawConfigParser()
        self.rf.read(self.configPath, encoding="utf-8")

    def get_section(self):
        """
        获取文件中所有的section [name]
        :return:
        """
        return self.cf.sections()

    def get_option(self, sectionName):
        """
        获取某个[section]下面的所有键值
        :param sectionName: [name]中name名字
        :return:
        """
        # print('this',self.cf.options(sectionName))
        return self.cf.options(sectionName)

    def get_redis(self, param):
        """
        读取mysql配置
        :param param: 配置项
        :return:
        """
        sql_db = "Sit-redis"
        if self.env == 'qa1':
            sql_db = "Qa1-redis"
        if param in self.get_option(sql_db):
            value = self.rf.get(sql_db, param)
            return value
        else:
            print("配置文件获取mysql参数:{} 不存在".format(param))

    def get_mongo(self, param):
        """
        读取mongodb配置
        :param param: 配置项
        :return:
        """
        print('============当前内容===========')
        mo_db = "Sit-Mongodb"
        if self.env == 'qa1':
            mo_db = "qa1-Mongodb"
        if param in self.get_option(mo_db):
            value = self.rf.get(mo_db, param)
            return value
        else:
            print("配置文件获取mongo参数:{} 不存在".format(param))

    def get_mysql(self, param):
        """
        读取mysql配置
        :param param: 配置项
        :return:
        """
        sql_db = "Sit-Mysql"
        if self.env == 'qa1':
            sql_db = "Qa1-Mysql"
        if param in self.get_option(sql_db):
            value = self.rf.get(sql_db, param)
            return value
        else:
            print("配置文件获取mysql参数:{} 不存在".format(param))

    def get_request_info(self, param):
        """
        :param section: [name]
        :param param: key
        :return:
        """
        re_info = "Qa1-Info"

        if param in self.get_option(re_info):
            value = self.cf.get(re_info, param)
            return value
        else:
            print("配置文件获取接口参数:{} 不存在".format(param))

    def get_config_info(self, section, param):
        """
        获取配置文件内容
        :param param:
        :return:
        """
        if param in self.get_option(section):
            value = self.cf.get(section, param)
            return value
        else:
            print("配置文件参数:{} 不存在".format(param))


if __name__ == '__main__':
    rc = ReadConfig()
    t = rc.get_mongo('password')
    xx = rc.get_option('Sit-Mongodb')
