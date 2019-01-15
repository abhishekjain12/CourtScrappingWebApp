proxy_dict = {
    "http": 'socks5h://localhost:9050',
    "https": 'socks5h://localhost:9050',
}

# import requests
# r = requests.request('GET', 'http://httpbin.org/ip')
# r = requests.request('GET', 'http://httpbin.org/ip', proxies=proxy_dict)

# print(r.text)
