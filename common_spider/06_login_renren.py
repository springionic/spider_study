import requests

session = requests.session()
url = 'http://www.renren.com/970569144'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Cookie': 'anonymid=jxd9lmrc-4ihjmg; depovince=HEB; _r01_=1; JSESSIONID=abcJanbU-skr0hgJd8tUw; ick_login=a1c520fd-d16e-4088-8e8e-db7080094342; t=09e2cde47f61e68ae299feb456e1659b4; societyguester=09e2cde47f61e68ae299feb456e1659b4; id=970569144; xnsid=6c0f9630; jebecookies=d885cdb5-91f8-458c-ada1-bb342e6eb3de|||||; ver=7.0; loginfrom=null; jebe_key=c0681323-5578-4ccf-8996-c42894d00213%7Cb0f34315e7b1b8e0aa889acd1cf03234%7C1561555147696%7C1%7C1561555147880; jebe_key=c0681323-5578-4ccf-8996-c42894d00213%7Cb0f34315e7b1b8e0aa889acd1cf03234%7C1561555147696%7C1%7C1561555147894; wp_fold=0',
}

r = session.get(url, headers=headers)
print(r.content.decode())
