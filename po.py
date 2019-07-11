import urllib,requests,_thread

import threading
from time import ctime,sleep,time
s = 0
def t(s):
    
    f = requests.get("http://127.0.0.1")
    
   
    
    

# while(True):
#     _thread.start_new_thread(t, ("Thread-1", 2,))
#     _thread.start_new_thread(t, ("Thread-2", 4,))

a= time()
for l in range(0,1000000):
    _thread.start_new_thread(t, (s,))


print(time()-a)
sleep(2)