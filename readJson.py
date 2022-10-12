import json, os
from Port_info import appConf


class ReadJson:
    root_dir = os.path.dirname(os.path.abspath(''))

    @classmethod
    def get_json(cls, filename, param):
        """
        读取json配置
        :param filename:/Data/filename
        :param param:接口key名字
        :return:
        """

        jsonPath = os.path.join(os.path.dirname(__file__) + os.sep + appConf.json_path + filename)
        with open(jsonPath, "r", encoding="utf-8") as f:
            file_res = json.load(f)
            return file_res.get(param)

if __name__ == '__main__':
     jsonPath = os.path.join(os.path.dirname(__file__) + os.sep + appConf.json_path + 'xindai.json')
     with open(jsonPath, "r", encoding="utf-8") as f:
           res = json.load(f)
           print(res['login'])
           print(type(res.get('login')))









