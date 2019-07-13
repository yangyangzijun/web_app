import redis
re = redis.Redis(host='192.168.43.68', port=6379)
print(re.get("poo"))