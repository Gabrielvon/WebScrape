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

domain = 'http://www.ted.com'
speakers_links = []
for page_num in xrange(65):
	url = 'http://www.ted.com/people/speakers?page={}&per_page=30'.format(page_num+1)
	print 'Processing: page_num=%d, url=%s' %(page_num,url)
	soup = getsoup(url)
	link_soups = soup.find_all('a',href=True)
	for link in link_soups:
		children_url = link['href'].encode('utf-8')
		if '/speakers/' in children_url:
			speakers_link = domain + children_url
			speakers_links.append(speakers_link)


with open('ted_links.csv','wb+') as f:
	writer = csv.writer(f)
	for item in speakers_links:
		writer.writerow([item])