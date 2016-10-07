

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

url = 'http://women.inc.com/speakers/'

# print 'Processing: page_num=%d, url=%s' %(page_num,url)
soup = getsoup(url)
bodies = soup.find_all('div',{'class','speakerRow'})
f = open('WomenInc_items.csv','wb+')
writer = csv.DictWriter(f,['Full Name', 'Blurb','Bio'])
writer.writeheader()

contents = []
content = dict()
for body in bodies:
	fullname = body.find_all('div',{'class','speaker-name'})[0].text.encode('utf8')
	blurb = body.find_all('h4',{'class','speaker-blurb'})[0].text.encode('utf8')
	bio = body.find_all('div',{'class','speaker-content'})[0].text.encode('utf8')
	content['Full Name'] = fullname
	content['Blurb'] = blurb
	content['Bio'] = bio
	contents.append(content)
	writer.writerow(content)
	print content



f.close()



