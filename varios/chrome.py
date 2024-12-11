from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

c_d = "C:\Python\src\rpa1\chromedriver\chromedriver.exe"
c_o = Options()
c_o.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome(c_d, chrome_options=c_o)
print (driver.title )

element = driver.find_element(By.CSS_SELECTOR , '.ui-dialog')


print (element.get_attribute('innerHTML'))

text = element.find_element(By.CSS_SELECTOR, '.duxmsgboxbody')
print(text.get_attribute('innerHTML'))
btn = element.find_element(By.CSS_SELECTOR, '.ui-button-text-only')

print(btn.get_attribute('innerHTML'))

btn.click()