# This script crawls all profile links from http://sandiegoventuregroup.onefireplace.com/members-directory?&tab=1
# The order of this list in the page will change every time you refresh the website

# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests, re, time, traceback, csv
from bs4 import BeautifulSoup


def getsoup_autoweb(driver,xpath):	
	try:
		button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
		src_code = driver.page_source.encode('utf-8')
	except Exception as e:
		src_code = []
		print('xpath')
		print('page option button is not clickable')
		pass

	soup = BeautifulSoup(src_code,"html.parser")	
	return soup

def getlinks(soup):
	links = []
	for link in soup.find_all('a', href=True):
		links.append(link['href'])
	pat = re.compile(r'http://sandiegoventuregroup.onefireplace.com/Sys/PublicProfile/\d*/\d*')
	links = re.findall(pat,str(links))
	return links
# tr = soup.find('tr',{'class','normal'})
# tr = soup.find_all('tr',{'class','normal'})

url = 'http://sandiegoventuregroup.onefireplace.com/members-directory'
opts = range(21)

LINKS = []
driver = webdriver.Chrome()
driver.get(url)
for num in opts: 	
	opt_xpath = '//*[@id="idPagingData"]/select/option[%d]' %(num+1)
	soup = getsoup_autoweb(driver,opt_xpath)	
	links = getlinks(soup)
	print '\n\n\n\n',(num+1),'    ',opt_xpath
	print links
	LINKS.extend(links)
driver.quit()		
	
## writerow expects an iterable, each element of which will be written to 
## the file, separated by the delimiter. Hence when you give it a string 
##  (which itself is an iterable), it writes each character to the file, 
## separated by the delimiter. What you want to do instead, is to supply 
## the "row" as a list of strings. In your case, each row has only one 
## string, so supply each row as a list with only one string.
with open('sdvg_links1.csv','wb+') as flinks:
	writer = csv.writer(flinks)
	for link in LINKS:
		writer.writerow([link])
