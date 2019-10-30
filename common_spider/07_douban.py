import json
import requests


class DoubanSpider(object):
    """爬取豆瓣热门国产电视剧的数据并保存到本地"""

    def __init__(self):
        # url_temp中的start的值是动态的，所以这里用{}替换，方便后面使用format方法
        self.url_temp = 'https://movie.douban.com/j/search_subjects?type=tv&tag=%E5%9B%BD%E4%BA%A7%E5%89%A7&sort=recommend&page_limit=20&page_start={}'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }

    def pass_url(self, url):  # 发送请求，获取响应
        print(url)
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def get_content_list(self, json_str):  # 提取数据
        dict_ret = json.loads(json_str)
        content_list = dict_ret['subjects']
        return content_list

    def save_content_list(self, content_list):  # 保存
        with open('douban.txt', 'a', encoding='utf-8') as f:
            for content in content_list:
                f.write(json.dumps(content, ensure_ascii=False))  # 一部电视剧的信息一行
                f.write('\n')  # 写入换行符进行换行
        print('保存成功！')


    def run(self):  # 实现主要逻辑
        num = 0
        while True:
            # 1. start_url
            url = self.url_temp.format(num)
            # 2. 发送请求，获取响应
            json_str = self.pass_url(url)
            # 3. 提取数据
            content_list = self.get_content_list(json_str)
            # 4. 保存
            self.save_content_list(content_list)
            if len(content_list) < 20:
                break
            # 5. 构造下一页url地址，进入循环
            num += 20  # 每一页有二十条数据


if __name__ == '__main__':
    douban_spider = DoubanSpider()
    douban_spider.run()
