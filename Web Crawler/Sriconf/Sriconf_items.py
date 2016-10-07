# This script crawls all profile content from file 'lica_links.csv'

# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#Spider 1

import requests, csv, re
from bs4 import BeautifulSoup

with open('csv/sriconf_links.csv','r') as flinks:
	reader = csv.reader(flinks)
	links = [row[0] for row in reader]


# print links

def getsoup(url):
	source_code = requests.get(url)
	content = source_code.content
	soup = BeautifulSoup(content,"html.parser")
	return soup

def split_full_name(full_name):
	fulln = full_name.split(' ')	
	firstn = fulln[0]
	other = ' '.join(fulln[1:])
	return [firstn,other]


contents = []
f = open('csv/Sriconf_speakers.csv','wb+')
Label = ['Full Name', 'First Name', 'Last Name', 'Headline', 'Bio', 'Reference']
writer = csv.DictWriter(f, Label)
writer.writeheader()
for link in links:
	print 'Processing:  ', link
	soup = getsoup(link)
	body = soup.find_all('h2')[0].parent
	body_text = body.text.encode('utf8').split('\n')

	full_name = body_text[1].strip()
	fn = split_full_name(full_name)[0].strip()
	ln = split_full_name(full_name)[1].strip()
	hl = '\n'.join(body_text[2:-2]).strip()
	bio_str = body_text[-2]

	print 'full_name: ', full_name
	print 'first_name: ',  fn
	print 'last_name: ', ln
	print 'headline: ', hl
	print 'bio: ', bio_str,'\n'

	# [full_name, fn, ln, hl, bio_str, link]
	mydict = {'Full Name':full_name,'First Name':fn,'Last Name':ln, 'Headline':hl,'Bio':bio_str,'Reference':link}
	writer.writerow(mydict)

	

# Label = lnki_all[0].keys()
# fi = open('csv/Alex_1stConn_ALL_NoHold.csv','wb+')
# w = csv.DictWriter(fi, Label)
# w.writeheader()
# for info in infos:
# 	w.writerow(info)

# fi.close()	
