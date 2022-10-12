import random

# -----Redis-----
sit_redis_host = 'sit-redis.testxinfei.cn'
redis_host = 'redis.testxinfei.cn'
redis_password = '#8keAh!dF%PZedAIShr72n'
redis_port = 6379
redis_database = 0

# ----mongo------
mon_host = 'mongodb.testxinfei.cn'
mon_user = 'test'
mon_password = '7iAzOn84S7^^Mc1i$iEaN8NSn'
mon_port = 27017


# ----mysql------
qa_host = 'qa1-mysql.testxinfei.cn'
qa_user = 'php_user'
qa_passwd = '@$pBVilsKI@nEhT7npGX%o0T#'
qa_port = 3306


sit_host = 'sit-mysql.testxinfei.cn'
sit_user = 'php_user'
sit_passwd = '@$pBVilsKI@nEhT7npGX%o0T#'
sit_port = 3306


# -----路径配置----
# 日志路径
log_path = "./Log"
# idcard和face图片
png_path = "./Png"
# json数据文件路径
json_path = "/"
# 配置文件路径
conf_path = ""

app_name = 'xyf01'

# 重置密码依赖 - 验证码校验返回值
set_password_ticket = None
# 重置密码依赖 - 获取密码salt返回值
salt = None
# jwt-token
jwt_token = None
# token
token = None
# userId--credit_user表id--信贷使用
userId = None
# user_id--user表id -- 风控使用
user_id = None
# 上传身份证前创建order_id
card_order_id = None
# 人脸识别前创建order_id
face_order_id = None
# 默认上传图片ocr的身份证号码
id_card = "433130199009162362"

# ---xyf---
# appid-数据库查询
# appid = "1000020"
# app_name = "xyf"
# # sdk名字
# utm_source = "xyf01_app"
# # 渠道
# app = "xyf01"


# ---cxh---
# appid-数据库查询
# appid = "1000005"
# app_name = "cxh"
# utm_source = "cxh_app"
# app = "cxh"

# 版本
version_code = "40801"

# sign签名ios-key
ios_key = "kHrfhNx@ATfzorQ32pwTSI3$D4VEv0y5"
# 设备号
device_id = "20201202272085bd7"

# -------------个人基本信息-废弃-------------
# 学历
education = random.choice([r"博士及以上", r"硕士", r"本科", r"专科", r"高中/中专/技校", r"初中及以下"])
# 职业
job = random.choice(["公司员工", "事业单位", "私营业主", "学生", "自由职业者", "其他"])
# 薪资
monthly_income = random.choice(["1,200以内", "1,200~2,500", "2,500~4,000", "4,000~6,000", "6,000~10,000", "10,000~20,000",
                                "20,000~50,000", "50,000以上"])
