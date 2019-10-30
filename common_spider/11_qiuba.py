import requests
import json
from lxml import etree


class QiubaSpider(object):
    """爬取糗事百科的热门下的数据"""

    def __init__(self):
        self.url_temp = 'https://www.qiushibaike.com/text/page/{}/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def get_url_list(self):  # 构造url_list
        return [self.url_temp.format(i) for i in range(1, 14)]

    def pass_url(self, url):  # 发送请求
        print(url)
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def get_content_list(self, html_str):  # 提取数据
        html = etree.HTML(html_str)
        div_list = html.xpath('//div[@id="content-left"]/div')  # 分组
        content_list = []
        for div in div_list:
            item = {}
            # 底下全是利用xpath和一些函数对数据的处理
            item['content'] = div.xpath('.//div[@class="content"]/span/text()')
            item['content'] = [i.replace('\n', '') for i in item['content']]
            item['author_gender'] = div.xpath('.//div[contains(@class, "articleGend")]/@class')
            item['author_gender'] = item['author_gender'][0].split(' ')[-1].replace('Icon', '') if len(
                item['author_gender']) > 0 else None
            item['author_age'] = div.xpath('.//div[contains(@class, "articleGend")]/text()')
            item['author_age'] = item['author_age'][0] if len(item['author_age']) > 0 else None
            item['author_img'] = div.xpath('.//div[@class="author clearfix"]//img/@src')
            item['author_img'] = 'https' + item['author_img'][0] if len(item['author_img']) > 0 else None
            item['stats_vote'] = div.xpath('.//span[@class="stats-vote"]/i/text()')
            item['stats_vote'] = item['stats_vote'][0] if len(item['stats_vote']) > 0 else None
            content_list.append(item)
        return content_list

    def save_content_list(self, content_list):
        with open('qiuba.txt', 'a', encoding='utf-8') as f:
            f.write(json.dumps(content_list, ensure_ascii=False, indent=4))
            f.write('\n')  # 换行


    def run(self):  # 实现主要逻辑
        # 1.构造url_list,热门的一共13页
        url_list = self.get_url_list()
        # 2.遍历发送请求，获取响应
        for url in url_list:
            html_str = self.pass_url(url)
            # 3.提取数据
            content_list = self.get_content_list(html_str)
            # 4.保存数据
            self.save_content_list(content_list)
        pass


if __name__ == '__main__':
    qiubai = QiubaSpider()
    qiubai.run()
