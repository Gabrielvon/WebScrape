# This script crawls all profile links from http://sandiegoventuregroup.onefireplace.com/members-directory?&tab=1
# The order of this list in the page will change every time you refresh the website

# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import requests, re, time, traceback, csv, pickle
from random import randint
from bs4 import BeautifulSoup

# def save_cookies(requests_cookiejar, filename):
#     with open(filename, 'wb') as f:
#         pickle.dump(requests_cookiejar, f)

# def load_cookies(filename):
#     with open(filename, 'rb') as f:
#         return pickle.load(f)

# #save cookies
# r = requests.get(url)
# save_cookies(r.cookies, filename)

# #load cookies and do a request
# requests.get(url, cookies=load_cookies(filename))

def getsoup(url):
	source_code = requests.get(url)
	content = source_code.content
	soup = BeautifulSoup(content,"html.parser")
	return soup


domain = 'https://mergernetwork.com'
total_pagenum = 532
start_pagenum = 287


profile_links = []
f = open('csv/mergernw_links.csv','r+')
writer = csv.writer(f)
for pagenum in xrange(1000):
	current_page = pagenum+start_pagenum
	if current_page > total_pagenum:
		break
	url = 'https://mergernetwork.com/profiles?page={}'.format(current_page)
	time.sleep(randint(5,10))
	soup = getsoup(url)
	all_links = soup.find_all('a',href=True)
	print 'Pagenum_%d \n' %current_page 
	num_of_links_per_page = 0
	for link in all_links:
		clean_link = link['href']
		if '/mn/' in clean_link:
			num_of_links_per_page += 1
			profile_link = domain+clean_link
			profile_links.append(profile_link)
			writer.writerow([profile_link])
	print "Number of Links Retrieved: %d \n\n" %num_of_links_per_page

	
links = list(set(profile_links))			
f.close()

