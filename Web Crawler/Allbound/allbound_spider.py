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

url = 'https://www.allbound.com/collaborate2016/speakers'

# print 'Processing: page_num=%d, url=%s' %(page_num,url)
soup = getsoup(url)
bodies = soup.find_all('div',{'class','speaker'})
f = open('allbound_items.csv','wb+')
writer = csv.DictWriter(f,['Full Name', 'Title', 'Company', 'Twitter', 'LinkedIn'])
writer.writeheader()

contents = []
content = dict()
for body in bodies:
	fullname, title, company = body.text.encode('utf8').strip().split('\n')
	content['Full Name'] = fullname
	content['Title'] = title
	content['Company'] = company
	links = [link['href'] for link in body.find_all('a',href=True)]
	content['Twitter'] = links[0].encode('utf-8')
	content['LinkedIn'] = links[1].encode('utf-8')
	contents.append(content)
	writer.writerow(content)
	print content



f.close()



