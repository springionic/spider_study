import requests
import json
import threading
from queue import Queue
from lxml import etree


class QiubaSpider(object):
    """爬取糗事百科的热门下的数据"""

    def __init__(self):
        self.url_temp = 'https://www.qiushibaike.com/text/page/{}/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        self.url_queue = Queue()  # 存放url的队列
        self.html_queue = Queue()  # 存放响应的队列
        self.content_queue = Queue()  # 存放content_list的对列

    def get_url_list(self):  # 构造url_list
        # return [self.url_temp.format(i) for i in range(1, 14)]
        for i in range(1, 14):
            self.url_queue.put(self.url_temp.format(i))  # 每一个构造出的url放入队列

    def pass_url(self):  # 发送请求
        while True:
            url = self.url_queue.get()  # 从队列里面取出一个url
            print(url)
            response = requests.get(url, headers=self.headers)
            # return response.content.decode()
            self.html_queue.put(response.content.decode())  # 将返回的结果放入队列
            self.url_queue.task_done()  # 使计数减一
            print(1)

    def get_content_list(self):  # 提取数据
        while True:
            html_str = self.html_queue.get()  # 从队列中取出
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
            # return content_list
            self.content_queue.put(content_list)
            self.html_queue.task_done()  # 计数减一
            print(2)

    def save_content_list(self):  # 保存
        while True:
            content_list = self.content_queue.get()  # 获取
            with open('qiuba.txt', 'a', encoding='utf-8') as f:
                f.write(json.dumps(content_list, ensure_ascii=False, indent=4))
                f.write('\n')  # 换行
            self.content_queue.task_done()  # 计数减一
            print(3)


    def run(self):  # 实现主要逻辑
        """ 每一件事开启一个线程，现在都是从队列里面获取，不用传参"""
        thread_list = []  # 用来存取线程,因为四个线程一个个启动太麻烦
        # 1.构造url_list,热门的一共13页
        t_url = threading.Thread(target=self.get_url_list)
        thread_list.append(t_url)
        # 2.遍历发送请求，获取响应
        for i in range(5):  # 为发送请求这里开启5个线程，直接循环即可
            t_pass = threading.Thread(target=self.pass_url)
            thread_list.append(t_pass)
        # 3.提取数据
        for i in range(3):  # 为提取数据这里开启3个线程
            t_html = threading.Thread(target=self.get_content_list)
            thread_list.append(t_html)
        # 4.保存数据
        t_save = threading.Thread(target=self.save_content_list)
        thread_list.append(t_save)
        for t in thread_list:
            t.setDaemon(True)  # 把子线程设置为守护线程，该线程不重要；主线程结束，子线程结束
            t.start()
        for q in [self.url_queue, self.html_queue, self.content_queue]:
            q.join()  # 让主线程等待阻塞，等待队列的任务完成之后再完成
        print('主线程结束！')


if __name__ == '__main__':
    qiubai = QiubaSpider()
    qiubai.run()
