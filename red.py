from redis import StrictRedis

redis = StrictRedis(host='127.0.0.1', port=6379, db=0, password='')
redis.hset('user','yang','1')
if redis.hget('user','ol') is None:
    print('ok')
print(redis.hget('user','ol'))