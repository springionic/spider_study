import requests
import threading
from queue import Queue
from lxml import etree

from config import INDEX_ADDRESS as index_address
from config import ADDRESS as address
from config import HEADERS as headers
from storage import Storage
from utils.tools import DecodingUtil


class JianshuSpider(object):
    """爬取简书首页数据的爬虫类"""
    def __init__(self):
        self.max_page = 2  # 爬取总文章数：300*7=2100
        self.params_queue = Queue()  # 存放地址发送post请求参数的队列
        self.url_queue = Queue()  # 存放文章url的队列
        self.index_queue = Queue()  # 存放首页响应的新文章列表的队列
        self.article_queue = Queue()  # 存放文章响应内容的队列
        self.content_queue = Queue()  # 存放格式化后的文章数据内容的队列

    def get_params_list(self):
        """构造post请求的page参数队列"""
        for i in range(1, self.max_page+1):
            self.params_queue.put({'page': i})

    def pass_post(self):
        """发送POST请求，获取新的文章列表，请求参数从队列中取出"""
        while True:
            response = requests.post(index_address, data=self.params_queue.get(), headers=headers)
            self.index_queue.put(DecodingUtil.decode(response.content))  # 返回结果放入队列
            self.params_queue.task_done()  # 计数减一
            print('pass_post', '@'*10)

    def parse_url(self):
        """根据首页返回的新的文章列表，解析出文章对应的url"""
        while True:
            content = self.index_queue.get()  # 从队列中取出一次POST请求的文章列表数据
            html = etree.HTML(content)
            a_list = html.xpath('//a[@class="title"]/@href')  # 每个li标签包裹着一篇文章
            for a in a_list:
                url = a  # xpath解析出文章的相对路径
                article_url = address + url
                self.url_queue.put(article_url)  # 放入队列
            self.index_queue.task_done()
            print('parse_url', '@'*10)

    def pass_get(self):
        """发送GET请求，获取文章内容页"""
        while True:
            article_url = self.url_queue.get()  # 从队列中获取文章的url
            response = requests.get(article_url, headers=headers)
            self.article_queue.put(DecodingUtil.decode(response.content))  # 返回结果放入队列
            self.url_queue.task_done()
            print('pass_get', '@'*10)

    def get_content(self):
        while True:
            article = dict()
            article_content = self.article_queue.get()
            html = etree.HTML(article_content)
            # 标题：title，钻石：diamond，创建时间：create_time，字数：word_number
            # 阅读量：read_number，评论数：comment_number，点赞数：like_number，文章内容：content
            article['title'] = html.xpath('//h1[@class="_2zeTMs"]/text()')[0].strip('\n').strip('\t')
            try:
                article['diamond'] = html.xpath('//span[@class="_3tCVn5"]/span/text()')[0]
            except IndexError:
                article['diamond'] = ''
            article['create_time'] = html.xpath('//div[@class="s-dsoj"]/time/text()')[0].replace('\n', '')
            article['word_number'] = html.xpath('//div[@class="s-dsoj"]/span[2]/text()')[0].split(' ')[-1]
            article['read_number'] = html.xpath('//div[@class="s-dsoj"]/span[last()]/text()')[0].split(' ')[-1]
            article['comment_number'] = html.xpath('//div[@class="_3nj4GN"][1]/span/text()[last()]')[0]
            article['like_number'] = html.xpath('//div[@class="_3nj4GN"][last()]/span/text()[last()]')[0]
            content = html.xpath('//article[@class="_2rhmJa"]')  # html富文本内容
            article['content'] = DecodingUtil.decode(etree.tostring(content[0], method='html', encoding='utf-8'))
            self.content_queue.put(article)  # 放入队列
            self.article_queue.task_done()  # 上一队列计数减一
            print('get_content', '@'*10)

    def save(self):
        """保存数据"""
        while True:
            article_info = self.content_queue.get()  # 队列中获取文章信息
            # print(article_info)
            Storage.save_to_mysql(article_info)  # 文章数据保存到mysql数据库
            self.content_queue.task_done()
            print('save', '*'*20)

    def run(self):
        # 0.各个方法之间利用队列来传送数据
        # 1.简书首页加载新数据方式为POST请求，url不变，参数page变化，所以首先构造一个params集
        # 2.遍历params集发送POST请求，获取响应
        # 3.根据每一次获取的文章列表，再获取对应的真正文章内容的页面url
        # 4.向文章内容页面发送请求，获取响应
        # 5.提取对应的数据
        # 6.保存数据，一份存入数据库，一份存入excel
        thread_list = list()  # 模拟线程池
        t_params = threading.Thread(target=self.get_params_list)
        thread_list.append(t_params)
        for i in range(2):  # 为post请求开启3个线程
            t_pass_post = threading.Thread(target=self.pass_post)
            thread_list.append(t_pass_post)
        for j in range(2):  # 为解析url开启3个线程
            t_parse_url = threading.Thread(target=self.parse_url)
            thread_list.append(t_parse_url)
        for k in range(5):  # 为get请求开启5个线程
            t_pass_get = threading.Thread(target=self.pass_get)
            thread_list.append(t_pass_get)
        for m in range(5):  # 为提取数据开启5个线程
            t_get_content = threading.Thread(target=self.get_content)
            thread_list.append(t_get_content)
        # for n in range(5):  # 为保存数据开启5个线程
        t_save = threading.Thread(target=self.save)  # 保存数据一个线程
        thread_list.append(t_save)
        # =====================================================================================================
        for t in thread_list:
            t.setDaemon(True)  # 把子线程设置为守护线程，主线程结束，子线程结束
            t.start()
        for q in [self.params_queue, self.url_queue, self.index_queue, self.article_queue, self.content_queue]:
            q.join()  # 让主线程等待阻塞，等待队列的任务完成之后再结束
        print('主线程结束......')


if __name__ == '__main__':
    jianshu_spider = JianshuSpider()
    jianshu_spider.run()