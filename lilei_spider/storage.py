import pandas as pd
from utils.db import conn
from utils.tools import rep_invalid_char


class Storage(object):
    """存储数据"""
    cursor = conn.cursor()
    excel_writer = pd.ExcelWriter('article.xlsx')

    def __init__(self):
        pass

    @classmethod
    def save_to_mysql(cls, article:dict):
        """字典类型的文章数据保存到数据库"""
        title = article.get('title', '')
        diamond = article.get('diamond', '')
        create_time = article.get('create_time', '')
        word_number = article.get('word_number', '')
        read_number = article.get('read_number', '')
        comment_number = article.get('comment_number', '')
        like_number = article.get('like_number', '')
        content = rep_invalid_char(article.get('content', ''))
        # content = article.get('content', '')

        sql = "INSERT INTO `article2` (`title`,`diamond`,`create_time`,`word_number`,`read_number`,`comment_number`," \
              "`like_number`,`content`) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}');".format(title, diamond,
              create_time, word_number, read_number, comment_number, like_number, content)
        try:
            cls.cursor.execute(sql)
            conn.commit()
        except Exception as e:
            print(e)
            # raise RuntimeError('保存至数据库过程Error！')
            print('保存至数据库过程Error！')
