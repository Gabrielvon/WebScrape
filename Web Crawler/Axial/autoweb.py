#automate browser test

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


url = 'https://network.axial.net/a/company/brook-venture-partners/'
browser = webdriver.Chrome()
try: 
	webpage = browser.get(url)
	print('Website opened...')
except Exception as e:
	browser.quit()
	print('Exception found', format(e))
	print('Failed to open website')

try:
	# element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.TAG_NAME, "h2")))
	element = WebDriverWait(browser, 10).until(
		EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[3]/div/ui-view/div/div[2]/div[1]/div/p/span/span")
			)).click()
	print('Website source code loaded...')
except Exception as e:
	print('Exception found', format(e))
	print('Failed to load source code')

try:
	browser.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/ui-view/div/div[2]/div[1]/div/div[1]/div/div/p[3]").click()
except Exception as e:
	print('Exception found', format(e))

try:
	browser.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/ui-view/div/div[2]/div[1]/div/div[2]/div/div/div/a").click()
except Exception as e:
	print('Exception found', format(e))	

content = browser.page_source.encode('utf-8')	
soup = BeautifulSoup(content,"html.parser")
browser.quit()

div2 = soup.find_all('div',{'class','industries-row row'})
print str([i.text for i in div2]).split('\\n')


# 