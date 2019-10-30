from selenium import webdriver

# 实例化一个浏览器
driver = webdriver.Chrome()  # 并非我们平常用的浏览器
# 发送请求
driver.get('https://www.baidu.com')
# 设置窗口大小
# driver.set_window_size(1920, 1080)
# 最大化窗口
driver.maximize_window()

# 进行页面截屏
driver.save_screenshot('./baidu.png')

# 元素定位的方法
driver.find_element_by_id('kw').send_keys('python') # 在输入框输入内容
driver.find_element_by_id('su').click()  # 点击按钮

html = driver.page_source()  # 页面信息


# 获取cookie
cookies = driver.get_cookies()
print(cookies)

# 退出浏览器
driver.quit()








