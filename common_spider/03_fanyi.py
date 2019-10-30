import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}
data = {
    'from': 'zh',
    'to': 'en',
    'query': '你好',
    'transtype': 'translang',
    'simple_means_flag': '3',
    'sign': '232427.485594',
    'token': 'ec591ecc4f290d6bfe50f4431cf12583',
}
post_url = 'https://fanyi.baidu.com/v2transapi'

r = requests.post(post_url, data=data, headers=headers)
print(r.content.decode())  # 失败，破解不了sign和token参数