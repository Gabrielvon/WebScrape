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

url = 'http://www.thegccworld.com/speakers/'

link_soups = soup.find_all('a',{'class','text-link'},href=True)
with open('gcc_links.csv','wb+') as f:
	writer = csv.writer(f)
	for item in link_soups:
		link = item['href'].encode('utf-8')
		writer.writerow([link])
		print link