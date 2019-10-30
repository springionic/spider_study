# 简书爬虫项目

### 目录结构
- lilei_spider
    - ____init____.py
    - jianshu_index.py
    - config.py
    - storage.py
    - utils
        - db.py
        - tools.py
        
## 文件说明：
#### jianshu_index.py
> 简书爬虫整体逻辑实现，也是运行项目的入口文件

#### config.py
> 项目中用到的配置参数

#### storage.py
> 实现数据的存储

#### db.py
> 数据库连接相关

#### tools.py
> 工具函数及工具类

#### article.sql
> 导出的数据库文件

#### requirements.txt
> 项目依赖库

### 技术说明
- python网络请求库：requests
- 数据解析方法：xpath(lxml库)
- 连接数据库：pymysql
- 多线程：threading，queue