import urllib.request


baidu = urllib.request.urlopen("http://127.0.0.1:5000/")
print(baidu.read())

