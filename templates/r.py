import redis
r = redis.Redis(host='192.168.43.68', port=6379)
# r.expire("list_name",3)

import time
print(str(time.time()*1000000)[0:-2])