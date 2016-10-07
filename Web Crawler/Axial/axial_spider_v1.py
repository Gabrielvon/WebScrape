# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import requests, re, time, traceback, csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getsoup(url):
	source_code = requests.get(url)
	content = source_code.content
	soup = BeautifulSoup(content,"html.parser")
	return soup

def getlinks(soup):
	links = []
	l_data = soup.find_all('div',{"class": "company-name"})
	for item in l_data:
		rlinks = item.find_all('a',href=True)
		pat = re.compile(r'https://(\S*)"')	
		link = re.search(pat,str(rlinks)).group()[:-1]
		links.append(link)

	return links

def autowebsoup(url):	
	try: 
		webpage = browser.get(url)
		print('Website opened...')
	except Exception as e:
		browser.quit()
		print('Exception found', format(e))
		print('Failed to open website')
	try:
		element = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[3]/div/ui-view/div/div[2]/div[1]/div/p/span/span"))).click()
		print('Website source code loaded...')
	except Exception as e:
		print('Exception found', format(e))
		print('Failed to load source code')
	try:
		browser.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/ui-view/div/div[2]/div[1]/div/div[1]/div/div/p[3]").click()
	except Exception as e:
		print('check industries info')
		pass		
	try:
		browser.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/ui-view/div/div[2]/div[1]/div/div[2]/div/div/div/a").click()
	except Exception as e:
		print('check campaigns info')
		pass
	content = browser.page_source.encode('utf-8')			
	soup = BeautifulSoup(content,"html.parser")	
	return soup

# parenturl = 'http://www.axial.net/companies/venture-capital-firms'
# soup = getsoup(url)
# num_of_page = int(soup.find('div',{'class','pagination'}).findNext('span').text[-1])
# link = "https://network.axial.net/a/company/brook-venture-partners/"
# soup_com = autowebsoup(links[0])

def companypage_crawler(link):
	soup_com = autowebsoup(link)
	fart = open('axial.csv','ab+')
	writer = csv.writer(fart)	
	div1 = soup_com.find('div',{'class','company-title'})
	company_title = str(div1.text).split('\n')

	div2 = soup_com.find('div',{'class','content-wrapper'})
	try:
		cIntro = str(div2.find('p',{'class','description-text'}).text).strip()
	except Exception as e:
		print('Exception found', format(e))
		cIntro = []
		pass
	try:
		cIndus = str(div2.find('div',{'class','industries-container'}).text).strip()
	except Exception as e:
		print('Exception found', format(e))
		cIndus = 'This company has not listed any industries.'	
		pass
	try:	
		cCamp = str(div2.find('div',{'class','company-transaction-profiles'}).find('tbody').text)
	except Exception as e:
		print('Exception found', format(e))
		cCamp = []
		pass
	try:	
		ctrans = div2.find('div',{'class','company-transactions'}).findChildren('div',{'class','back'})
		cTrans = ''.join([item.text for item in ctrans])
	except Exception as e:
		print('Exception found', format(e))
		try:
			cTrans = str(div2.find('div',{'class','company-transactions'}).text).strip()
		except:
			pass
	try:
		cDetLoc = str(div2.find('div',{'class','company-locations'}).text).strip()
	except Exception as e:
		print('Exception found', format(e))
		cDetLoc = []	
		pass	
	div3 = soup_com.find('div',{'class','sidebar-wrapper'})
	try: 
		cTeam = str(div3.find('div',{'class','member-details'}).text).strip()
	except Exception as e:
		print('Exception found', format(e))
		cTeam = []	
		pass
	Company_title = filter(None,company_title)
	cName = Company_title[0]
	cWeb = Company_title[2]
	cType_Loc = Company_title[1]
	cTypeLoc = re.split('[()]',cType_Loc)
	cType = cTypeLoc[0]

	cDetLoc = re.sub('Locations','',cDetLoc)
	cDetLoc = re.sub('Headquarters HQ','',cDetLoc)
	cDetLoc = re.sub('Satellite ','',cDetLoc)
	cDetLoc = filter(None, cDetLoc).strip()

	try:
		cCity = cTypeLoc[1].split(',')[0]
		cStateCountry = cTypeLoc[1].split(',')[1]
	except:
		cCity = cDetLoc
		cStateCountry = []

	alldata = [cName, cType, cCity, cStateCountry, cWeb, cIntro, cIndus, cCamp, cTrans, cDetLoc, cTeam, link]
	writer.writerow(alldata)
	fart.close()
	return [cName,cType]

URL = 'http://www.axial.net/companies/'
SOUP = getsoup(URL)
LINKS = SOUP.find('ul',{'class','company-dir-listings'}).findAll('a',href=True)
children = [i['href'].encode('utf-8') for i in LINKS]
domain = 'http://www.axial.net'
parenturls = [domain+child for child in children]

browser = webdriver.Chrome()
for parenturl in parenturls:
	soup = getsoup(parenturl)
	num_of_page = int(soup.find('div',{'class','pagination'}).findNext('span').text[-1])

	for pagenum in xrange(num_of_page):
		url = parenturl+'/'+str(pagenum+1)
		soup = getsoup(url)
		links = getlinks(soup)
		
		for link in links:
			print 'Processing', pagenum+1, link
			result = companypage_crawler(link)
			print result,'Saved'
			print '\nNext'

browser.quit()		

# writer.writerow(['Name','Type', 'City', 'State or Country', Offical_Web','Introduction','Industries','Campaign','Transactions','Location','Team','References'])	









