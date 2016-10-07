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

def autowebsoup(url):	
	try: 
		webpage = browser.get(url)
		print('Website opened...')
	except Exception as e:
		print('Exception found', format(e))
		print('Failed to open website')
	try:
		element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, 
			"/html/body/div[1]/div/div[3]/div/ui-view/div/div[1]/div/div/h2"
			)))
		print('Website source code loaded...')
	except Exception as e:
		print('Failed to load source code')	
		element = 0


	try:
		element = WebDriverWait(browser, 10).until(
			EC.element_to_be_clickable((By.XPATH, 
				"/html/body/div[1]/div/div[3]/div/ui-view/div/div[2]/div[1]/div/p/span/span")
			)).click()
	except Exception as e:
		pass
	try:
		browser.find_element_by_xpath(
			"/html/body/div[1]/div/div[3]/div/ui-view/div/div[2]/div[1]/div/div[1]/div/div/p[3]"
			).click()
	except Exception as e:
		pass		
	try:
		browser.find_element_by_xpath(
			"/html/body/div[1]/div/div[3]/div/ui-view/div/div[2]/div[1]/div/div[2]/div/div/div/a"
			).click()
	except Exception as e:
		pass

	if element:
		content = browser.page_source.encode('utf-8')			
		soup = BeautifulSoup(content,"html.parser")	
	else:
		soup = 0

	return soup		


def companypage_crawler(soup):
	div1 = soup.find('div',{'class','company-title'})
	company_title = div1.text.encode('utf8').split('\n')

	div2 = soup.find('div',{'class','content-wrapper'})
	try:
		cIntro = div2.find('p',{'class','description-text'}).text.encode('utf8').strip()
	except Exception as e:
		cIntro = []
		pass
	try:
		cIndus = div2.find('div',{'class','industries-container'}).text.encode('utf8').strip()
		cIndus_list = cIndus.split(' \n')
		cIndus_list_clean = [re.sub(r'\n\s*', '', string) for string in cIndus_list]
		cIndus_OneCell = '\n\n'.join(cIndus_list_clean)
	except Exception as e:
		cIndus = []	
		cIndus_OneCell = []	
		pass
	try:	
		cCamp = str(div2.find('div',{'class','company-transaction-profiles'}).find('tbody').text)
	except Exception as e:
		cCamp = []
		pass
	try:	
		ctrans = div2.find('div',{'class','company-transactions'}).findChildren('div',{'class','back'})
		cTrans = ''.join([item.text for item in ctrans])
	except Exception as e:
		try:
			cTrans = div2.find('div',{'class','company-transactions'}).text.encode('ut8').strip()
		except:
			pass
	try:
		cDetLoc = div2.find('div',{'class','company-locations'}).text.encode('utf8').strip()
		cDetLoc = re.sub('Locations','',cDetLoc)
		cDetLoc = re.sub(r'(\n\s*)',r'\n',cDetLoc)
		# cDetLoc = re.sub('Headquarters HQ','',cDetLoc).split('Satellite')
		cDetLoc = filter(None, cDetLoc).strip()
	except Exception as e:
		cDetLoc = []	
		pass	
	div3 = soup.find('div',{'class','sidebar-wrapper'})
	try: 
		cTeam = div3.find_all('div',{'class','member-details'})
		cTeam_list = [item.text.encode('utf8').strip() for item in cTeam]
		cTeam_OneCell = '\n\n'.join(cTeam_list)
	except Exception as e:
		cTeam = []	
		pass
	Company_title = filter(None,company_title)
	cName = Company_title[0]

	cWeb = Company_title[2]
	cType_Loc = Company_title[1]
	cTypeLoc = re.split('[()]',cType_Loc)
	cType = cTypeLoc[0]	

	try:
		cCity = cTypeLoc[1].split(',')[0]
		cStateCountry = cTypeLoc[1].split(',')[1]
	except:
		cCity = cDetLoc
		cStateCountry = []
		pass

	alldata = [cName, cType, cCity, cStateCountry, cWeb, cIntro, cIndus_OneCell, cCamp, cTrans, cDetLoc, cTeam_OneCell, link]
	return alldata


with open('axial_links.csv','rb+') as flinks:
	reader = csv.reader(flinks)
	links = [str(row[0]).replace(" ","") for row in reader]

browser = webdriver.Chrome()

fart = open('axial.csv','ab+')
writer = csv.writer(fart)	
writer.writerow(['Name','Type', 'City', 'State or Country', 'Offical_Web','Introduction','Industries','Campaign','Transactions','Location','Team','References'])	

for link in links:
	print '\nProcessing', link
	try:
		
		soup = autowebsoup(link)
		result = companypage_crawler(soup)
		writer.writerow(result)
		print result[0],'Saved'
	except Exception as e:
		result = link
		writer.writerow(result)
		print e
		print link, 'failed to loaded'


fart.close()
browser.quit()