from selenium import webdriver
# webdriver.Chrome

from selenium import webdriver

# config.selenium.driver_chrome
# config.selenium.driver_phantomjs
#
# for uid, password in accounts:
#     driver = webdriver.Chrome(config.selenium.driver_chrome)
#     driver.get(config.gitlab.host)
#     driver.find_element_by_xpath('//*[@id="username"]').send_keys(uid)
#     driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
#     driver.find_element_by_xpath('//div[{conditions}]//input[@name="commit"]'.format(conditions=' and '.join([
#         'contains(concat(" ", @class, " "), " login-box ")',
#         'contains(concat(" ", @class, " "), " active ")'
#     ]))).click()
#     driver.save_screenshot('capture/{uid}.png'.format(uid=uid))
#     driver.close()
#     driver.quit()
