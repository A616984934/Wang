import requests
import demjson
from requests_toolbelt import MultipartEncoder
from urllib import parse


java_test = "http://10.10.100.25:6010"
php_test1 = "http://10.10.100.23:6010"
php_test2 = "http://10.10.100.24:6010"
python_test1 = "http://10.10.100.26:6010"
python_test_qtz = "http://10.10.100.22:6010"
php_qa1 = "http://10.10.102.38:6010"
sit_java_1 = "http://10.10.100.28:6010"
sit_php_1 = "http://10.10.100.27:6010"
sit_python_1 = "http://10.10.100.29:6010"


new_dict = {"java_test": java_test, "php_test1": php_test1, "php_test2": php_test2, "python_test1": python_test1,
            "python_test_qtz": python_test_qtz, "php_qa1": php_qa1, "sit_java_1": sit_java_1,
            "sit_php_1": sit_php_1, "sit_python_1": sit_python_1}


def server_post(server_name, info, task_name, tail=1):
    # 调用目标服务
    message = ''
    server_name1 = ''
    if tail == 1:
        server_name1 = server_name + "/script"
    # 2 请求部署覆盖率
    if tail == 2:
        server_name1 = server_name + "/code"
    # 3 统计结果
    if tail == 3:
        try:
            server_name1 = server_name + "/sum-res"
            res2 = requests.post(server_name1, json=info)
            server_name2 = server_name + "/display"
            res3 = requests.post(server_name2, json=info)
            if len(res3.content) > 20:
                # 写入不成功的问题？
                f = open('/data/report/{}.zip'.format(task_name), 'wb')
                f.write(res3.content)
                f.close()
                res = res2.text.encode('utf-8').decode('unicode_escape').split(',')
                return res
            # 如果没有写入成功，则直接返回报错
            else:
                return False
        except Exception as e:
            print('错误'.format(e))
            return '目标服务出现错误'
    if tail == 4:
        # 删除多余的文件
        server_name1 = server_name + "/delete"
    res1 = requests.post(server_name1, json=info)
    res = res1.text.encode('utf-8').decode('unicode_escape')
    if res is None:
        message = "server connect wrong"
        return message
    else:
        message = res
        return message


def form_model(servers, info):
    # 表单形式请求数据
    rel_info = MultipartEncoder(info)
    # headers = {"Content-Type": "application/form-data"}
    res1 = requests.post(servers, data=rel_info, headers={'Content-Type': rel_info.content_type})
    res = res1.text.encode('utf-8').decode('unicode_escape')
    if res is None:
        message = "server connect wrong"
        return message
    else:
        message = res
        return message


def id_card_get(servers,info):
    # www.format 格式
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    rel_info = parse.urlencode(info)
    res1 = requests.post(servers, data=rel_info, headers=headers)
    res = res1.json().get('data')
    if res is None:
        message = "server connect wrong"
        return message
    else:
        message = res
        return message







