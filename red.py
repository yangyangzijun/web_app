from redis import StrictRedis

redis = StrictRedis(host='127.0.0.1', port=6379, db=0, password='')
redis.set('name', 'Bob')
print(redis.get('name'))