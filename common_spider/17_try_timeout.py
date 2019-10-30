from selenium import webdriver
import time


driver = webdriver.Chrome()
driver.get('http://www.budejie.com/text/')


res1 = driver.find_element_by_xpath('//div[@class="j-r-list"]/ul/li').text
print(res1)

driver.find_element_by_class_name('pagenxt').click()
res2 = driver.find_element_by_xpath('//div[@class="j-r-list"]/ul/li').text
print(res2)

driver.quit()