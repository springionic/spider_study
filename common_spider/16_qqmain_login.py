import time
from selenium import webdriver


driver = webdriver.Chrome()
driver.get('https://mail.qq.com/')

# 切换到iframe
driver.switch_to.frame('login_frame')
