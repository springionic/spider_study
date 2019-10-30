import requests

proxies = {
    'http': '124.192.123.243:3128'
}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',}

r = requests.get('http://www.baidu.com', proxies=proxies, headers=headers)
print(r.status_code)
