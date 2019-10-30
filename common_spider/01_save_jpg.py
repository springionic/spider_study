import requests

# 发送请求
response = requests.get('https://fallbacks.carbonads.com/nosvn/fallbacks/38a1311c86da027a73d11526122f4dfc.png')
# 保存
with open('a.png', 'wb') as f:
    f.write(response.content)
