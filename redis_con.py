from Port_info import appConf
import redis


class RedisConnect(object):
    # env的不同，不同host
    def __init__(self, env='sit'):
        if env == 'sit':
            self.host = appConf.sit_redis_host
        else:
            self.host = appConf.redis_host
        try:
            print(self.host)
            self.conn = redis.Redis(host=self.host, password=appConf.redis_password, port=appConf.redis_port,
                                    db=appConf.redis_database, decode_responses=True)
        except Exception as e:
            print('redis连接失败，错误信息%s' % e)

    def get(self, key):
        """获取key所对应的值"""
        return self.conn.get(key)

    def set(self, key, value):
        """设置值"""
        return self.conn.set(key, value)

    def delete(self, key):
        """直接根据key删除整个值"""
        result = self.conn.keys()
        # if bytes(key, encoding="utf-8") in result:
        if key in result:
            # self.conn.hdel(key, vaule) 只根据字典删除部分满足键值对
            return self.conn.delete(key)  # 连同key 和key 所对应的的值一块删除
        else:
            return "此%s不存在" % key

    def close_redis(self):
        """关闭连接"""
        self.conn.close()


if __name__ == '__main__':
    # print(RedisConnect.delete("fund-system:qj-order-lend:20210602111340021346883"))
    new = RedisConnect()
    list_keys = new.conn.keys("13800005223")

    # new.delete("jwt:18500000888:xyf01")
    print(new.get("mobile:13800005223"))
    new.close_redis()
