import pymysql


class DB(object):
    """数据库连接"""
    _host = '127.0.0.1'
    _user = 'root'
    _password = 'lilei120400'
    _db = 'homework'

    @classmethod
    def conn_mysql(cls):
        return pymysql.connect(host=cls._host, user=cls._user, password=cls._password, db=cls._db, charset='utf8')


conn = DB.conn_mysql()