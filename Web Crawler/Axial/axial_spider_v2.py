# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import requests, re, time, traceback, csv
from bs4 import BeautifulSoup

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


URL = 'http://www.axial.net/companies/'
soup = getsoup(URL)
LINKS = soup.find('ul',{'class','company-dir-listings'}).findAll('a',href=True)
children = [i['href'].encode('utf-8') for i in LINKS]
domain = 'http://www.axial.net'
parenturls = [domain+child for child in children]

ALLLINKS = []
for parenturl in parenturls:
	soup = getsoup(parenturl)
	num_of_page = int(soup.find('div',{'class','pagination'}).findNext('span').text[-1])

	for pagenum in xrange(num_of_page):
		url = parenturl+'/'+str(pagenum+1)
		soup = getsoup(url)
		links = getlinks(soup)
		ALLLINKS += links
		print parenturl, pagenum
		
with open('axial_links.csv','wb+') as flinks:
	writer = csv.writer(flinks,delimiter=' ')
	for link in ALLLINKS:
		writer.writerow(link)
