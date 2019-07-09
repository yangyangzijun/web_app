import redis
re = redis.Redis(host='192.168.43.68', port=6379)
#re.set("232",'1')
print(re.get('232'))