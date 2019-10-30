import requests

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}
p = {'wd': 'python'}
url = 'https://www.baidu.com/s'

r = requests.get(url, headers=headers, params=p)
print(r.status_code)
print(r.request.url)