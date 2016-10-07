# This script crawls all profile links from http://www.licapital.org/page-1524067

# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#Spider 1

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests, re, time, traceback, csv
from bs4 import BeautifulSoup


def getsoup_autoweb(url,nextpage):
	driver = webdriver.Chrome()
	try:
		driver.get(url)
		button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(By.XPATH, "//*[@id='idPagingData']/select/option[2]"))
		if nextpage:
			button.click()
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='membersTable']/tbody/tr[1]/td[1]/div[2]")))
		src_code = driver.page_source.encode('utf-8')
	except Exception as e:
		print e
		pass
	finally:
		driver.quit()

	soup = BeautifulSoup(src_code,"html.parser")	
	return soup

def getlinks(soup):
	links = []
	for link in soup.find_all('a', href=True):
		links.append(link['href'])
	pat = re.compile(r'http://www.licapital.org/Sys/PublicProfile/\d*/\d*')
	links = re.findall(pat,str(links))
	return links
# tr = soup.find('tr',{'class','normal'})
# tr = soup.find_all('tr',{'class','normal'})

url = 'http://www.licapital.org/page-1524067'
soup_1 = getsoup_autoweb(url,False)
links_1 = getlinks(soup_1)
soup_2 = getsoup_autoweb(url,True)
links_2 = getlinks(soup_2)
links = links_1 + links_2
with open('lica_links.csv','wb+') as flinks:
	writer = csv.writer(flinks,delimiter=' ')
	for link in links:
		writer.writerow(link)
