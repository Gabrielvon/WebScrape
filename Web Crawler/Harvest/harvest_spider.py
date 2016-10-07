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

url = 'http://harvestsummit.com/people.html'

# print 'Processing: page_num=%d, url=%s' %(page_num,url)
soup = getsoup(url)
bodies = soup.find_all('div',{'class','text-left'})
f = open('harvest_items.csv','wb+')
writer = csv.DictWriter(f,['Full Name', 'Company', 'Bio'])
writer.writeheader()

contents = []
content = dict()
for body in bodies:
	fullname = body.find('h3').text.encode('utf-8')
	company = body.find('h3').next_sibling.text.encode('utf-8')
	bio_parts = body.text.strip().split('\n')[1:]
	bio = '\n'.join([b.encode('utf-8') for b in bio_parts])
	content['Full Name'] = fullname
	content['Company'] = company
	content['Bio'] = bio
	contents.append(content)
	writer.writerow(content)
	print content



f.close()



