import requests
import re
import json

class NeihanSpider(object):
    """内涵段子，百思不得其姐，正则爬取一页的数据"""
    def __init__(self):
        self.temp_url = 'http://www.budejie.com/text/{}'  # 网站地址，给页码留个可替换的{}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def pass_url(self, url):  # 发送请求，获取响应
        print(url)
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def get_first_page_content_list(self, html_str):  # 提取第一页的数据
        content_list = re.findall(r'<div class="j-r-list-c-desc">\s*<a href="/detail-.*">(.+?)</a>', html_str)  # 非贪婪匹配
        return content_list

    def save_content_list(self, content_list):
        with open('neihan.txt', 'a', encoding='utf-8') as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False))
                f.write('\n')  # 换行
            print('成功保存一页！')

    def run(self):  # 实现主要逻辑
        for i in range(20):  # 只爬取前20页数据
            # 1. 构造url
            # 2. 发送请求，获取响应
            html_str = self.pass_url(self.temp_url.format(i+1))
            # 3. 提取数据
            content_list = self.get_first_page_content_list(html_str)
            # 4. 保存
            self.save_content_list(content_list)

if __name__ == '__main__':
    neihan = NeihanSpider()
    neihan.run()