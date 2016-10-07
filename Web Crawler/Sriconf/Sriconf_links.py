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

url = 'http://www.sriconference.com/agenda/2016-conference-speakers.html'
domain = 'http://www.sriconference.com/'

soup = getsoup(url)
center = soup.find_all('center')
links = []
for item in center:
	center_links = item.find_all('a',href=True) 
	for center_link in center_links:
		link = center_link['href'].encode('utf8')
		if re.search('agenda/speaker', link):
			links.append(domain+link)

links = list(set(links))			

with open('csv/sriconf_links.csv','wb+') as f:
	writer = csv.writer(f)
	for link in links:
		writer.writerow([link])
		print link