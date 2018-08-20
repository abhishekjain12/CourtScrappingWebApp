import requests

res = requests.request('GET', 'http://hcmjudgment.man.nic.in')
for cookie in res.cookies:
    print(cookie.__dict__['name'])
    print(cookie.__dict__['value'])
    print(cookie)
