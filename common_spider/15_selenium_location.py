from selenium import webdriver


driver = webdriver.Chrome()

driver.get('http://www.budejie.com/text/')

# 返回一个列表
res1 = driver.find_elements_by_xpath('//div[@class="j-r-list"]/ul/li')
# print(res1)
for r in res1:
    # 这里的方法只能获取到element，所以xpath表达式不允许返回一个字符串，只能写到获取element的级别
    # 然后可以用text属性获取内容，get_attribute()方法获取属性
    print(r.find_element_by_xpath('.//div[@class="j-r-list-c-desc"]/a').text)
    print(r.find_element_by_xpath('.//div[@class="j-r-list-c-desc"]/a').get_attribute('href'))

driver.quit()