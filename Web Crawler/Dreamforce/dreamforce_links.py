# This script crawls all profile links from http://sandiegoventuregroup.onefireplace.com/members-directory?&tab=1
# The order of this list in the page will change every time you refresh the website

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

url = 'https://www.salesforce.com/dreamforce/DF16/keynotes/'
domain = 'https://www.salesforce.com'

soup = getsoup(url)
link_soups = soup.find_all('div',{'class','cta'})
links = []
for item in link_soups:
	link = item.find('a',href=True)['href'].encode('utf-8')
	links.append(domain+link)

links = links[1:]

with open('csv/dreamforce_links.csv','wb+') as f:
	writer = csv.writer(f)
	for link in links:
		writer.writerow([link])
		print link