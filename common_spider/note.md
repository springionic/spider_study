### 正则使用的注意点
- 非贪婪匹配
```python
import re

a = '<meta name="baidu-site-verification" content="cZdR4xxR7RxmM4zE" /><eta http-equiv="Pragma" cont ent="no-cache">'

re.findall('<.+>', a)  # 贪婪匹配，列表中只返回一次匹配结果，开头到结尾
re.findall('<.+?>', a)  # 非贪婪匹配，列表中返回两次匹配结果
# 加上一个 ? 就可以变成非贪婪匹配
```
- `re.findall('a(.*?)b', 'str)`，能够返回括号中的内容
- 原始字符串r，带匹配字符串中有反斜杠的时候，使用r能忽略转义的效果
- 点号默认匹配不到`\n`
- `\s`能匹配到空白字符，不仅仅包含空格，还有`\t\r\n`

### XPath 学习重点
- 使用xpath helper或者是chrome中的copy xpath都是从element中提取的数据，但是爬虫获取的是url对应的响应，
往往和elements不一样
- 获取文本
    - `a/text()` 获取a下的文本
    - `a//text()` 获取a下所有标签的文本
    - `//a[text()="下一页]` 选择文本为“下一页”三个字的a标签 
- `@符号`
    - `a/@href`
    - `//ul[@id="detail-list]`
- `//`
    - 在xpath开始的 时候表示从当前html中任意位置开始选择
    - `li//a` 表示的是li下的任何一个a标签
    
### lxml使用注意点
- lxml能够修正HTML代码，但是可能改错了
    - 使用etree.tostring观察修改之后的html的样子，根据修改之后的html字符串写xpath
- lxml模块，能接受bytes和str的字符串
- 提取页面数据的思路
    - 先分组，取到一个包含分组标签的列表
    - 遍历，取其中每一组数据进行提取，不会造成数据的对应错乱

### xpath 的包含
- `//div[contains(@class, 'i')]` class包含i的div

### 实现爬虫的套路
#### 一、准备url
- 准备start_url
    - url地址规律不明显，总数不确定
    - 通过代码提取下一页的url
        - xpath
        - 寻找url地址，部分参数在当前的响应中(比如，当前页码数和总的页码数在当前响应中)
- 准备url_list
    - 页码总数明确
    - url地址规律明显
#### 二、发送请求，获取响应
- 添加随机的User-Agent，反反爬虫
- 添加随机的代理IP，反反爬虫
- 在对方判断出我们是爬虫之后，应该添加更多的headers字段，包括cookie
- cookie的处理可以使用session来解决(requests的session)
- 准备一堆能用的cookie，组成cookie池
    - 如果不登录
        - 准备刚开始能成功请求对方网站的cookie，即接收对方网站设置在response的cookie
        - 下一次请求的时候，使用之前的列表的cookie来请求
    - 如果登录
        - 准备多个账号
        - 使用程序获取每一个账号的cookie
        - 之后请求登录之后才能访问的网站，随机的选择cookie
#### 三、提取数据
- 确定数据的位置
    - 如果数据在当前的url地址中
        - 提取的是列表页的数据
            1. 直接请求列表页中的url地址，不用进入详情页
        - 提取的是详情页的数据
            1. 确定url地址
            2. 发送请求
            3. 提取数据
            4. 返回
    - 如果数据不在当前的url地址中
        - 在其它的响应中，寻找数据的位置
            1. 从network中从上往下找
            2. 使用chrome中的过滤，选择除了js、css、img之外的按钮
            3. 使用chrome中的search all file，最好搜索数字和英文
- 数据的提取
    - re：提取max_time,price，html中的字符串等
    - xpath：从html中提取整块的数据，先分组，之后每一组再提取
    - json
#### 保存
- 保存在本地：json、text、csv
- 保存在数据库

### 验证码的识别
- 云打码平台网站
- url不变，验证码不变
    - 请求验证码的地址，获得响应，识别
- url不变，验证码会变
    - 思路：对方服务器返回验证码的时候，会把每个用户的信息和验证码进行一个对应，之后，在用户发送post请求的时候，会对比post请求中发送的验证码和当前用户真正存储在服务器的验证码是否相同
    - 1.实例化session
    - 2.使用session请求登录页面，获取验证码的地址
    - 3.使用session请求验证码，识别
    - 4.使用session发送post请求
- 使用selenium登录，遇到验证码
    - url不变，验证码不变，同上
    - url不变，验证码会变
        - 1.selenium请求登录页面，同时拿到验证码的地址
        - 2.获取登录页面driver中的cookie，交给requests模块发送
        - 3.输入验证码，点击登录
    
### selenium使用的注意点
- 获取文本和获取属性
    - 先定位到元素，然后调用`.text`属性或者`get_attribute()`方法获得
- selenium获取的页面数据是浏览器中elements的内容
- find_element和find_elements的区别
    - find_element返回一个element，没有就会报错
    - find_elements返回一个列表，没有就空列表
    - 在判读是否有下一页的时候，使用find_elements来根据结果的列表长度来判断
- 如果页面中含有iframe或者frame，需要先调用`driver.switch_to.frame()`方法切换到frame中才能定位元素
- selenium请求第一页的时候会等待页面加载完了之后再获取数据，但是点击翻页之后，会直接获取数据，肯能会报错，因为数据还没有加载出来，需要time.sleep(),不过经测试，新版本可能已经不用了
- selenium中find_element_by_class只能接收一个class对应的一个值，不能传入多个
