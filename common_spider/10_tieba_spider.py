import requests
import json
from lxml import etree

class TiebaSpider(object):
    """利用手机版"""
    def __init__(self, tieba_name):
        self.tieba_name = tieba_name
        self.temp_url = 'https://tieba.baidu.com/f?kw=' + tieba_name + '&mo_device=1&pn={}&'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        self.part_url = 'https://tieba.baidu.com/f'

    def pass_url(self, url):  # 发送请求，获取响应
        print(url)
        response = requests.get(url, self.headers)
        return response.content.decode()

    def get_content_list(self, html_str):
        html = etree.HTML(html_str)
        li_list = html.xpath('//li')  # 根据li分组
        print(li_list)
        content_list = []
        for li in li_list:
            item = {}
            item['title'] = li.xpath('./a/div[@class="ti_title"]/span/text()')[0] if len(li.xpath('./a/div[@class="ti_title"]/span/text()')) else None
            item['href'] = self.part_url + li.xpath('./a/@href')[0] if len(li.xpath('./a/@href')) else None
            item['img_list'] = li.xpath('./img/@src') if len(li.xpath('./img/@href')) else None
            content_list.append(item)
        return content_list

    def save_content_list(self, content_list):  # 保存数据
        file_path = self.tieba_name + '.txt'
        with open(file_path, 'a', encoding='utf-8') as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False, indent=4))
                f.write('\n')
        print('保存成功！')



    def run(self):  # 实现主要逻辑
        number = 0
        while True:
            # 1.start_url
            # 2.发送请求获取响应
            html_str = self.pass_url(self.temp_url.format(number))
            # 3.提取数据，提取下一页的url地址
            content_list = self.get_content_list(html_str)
            # 4.保存数据
            self.save_content_list(content_list)
            # 5.请求下一页的url地址，进入循环2-5步
            if len(content_list) < 25:
                break
            number += 30  # 每一页30条数据

if __name__ == '__main__':
    tieba_spider = TiebaSpider('李毅')
    tieba_spider.run()
# 失败，最终未成功