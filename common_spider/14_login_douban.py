import time
from selenium import webdriver

# 实例化driver
driver = webdriver.Chrome()
driver.get('https://www.douban.com/')
## 切换iframe子框架
driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])

driver.maximize_window()  # 最大化窗口
driver.find_element_by_css_selector('li.account-tab-account').click()  # 点击密码登录的标签
driver.find_element_by_id('username').send_keys('13343396443')
driver.find_element_by_id('password').send_keys('lilei120400')
# 点击‘登录豆瓣’按钮
# 这里需要注意，当元素的class属性有好几个的时候，此函数的参数填class的第一个就好
driver.find_element_by_class_name('btn').click()  # 元素的class属性：btn btn-account
# 获取cookies,字典推导式
cookies = {i['name']: i['value'] for i in driver.get_cookies()}
print(cookies)

time.sleep(5)
driver.quit()  # 退出浏览器




