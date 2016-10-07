# This script crawls all profile content from file 'lica_links.csv'

# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#Spider 1

import requests, csv
from bs4 import BeautifulSoup



with open('sdvg_links.csv','rb+') as flinks:
	reader = csv.reader(flinks)
	links = [row[0] for row in reader]

# print links

def getsoup(url):
	source_code = requests.get(url)
	content = source_code.content
	soup = BeautifulSoup(content,"html.parser")
	return soup



dict_list = []
for link_num in xrange(len(links)):
	soup = getsoup(links[link_num])
	my_dict = dict()

	labels = [i.text.encode('utf8').strip() for i in soup.find_all('div',{'class','fieldLabel'})][1:]
	bodies = [i.text.encode('utf8').strip() for i in soup.find_all('div',{'class','fieldBody'})][1:]
	Link_To = [i.text.encode('utf8') for i in soup.find_all('a',{'class','bundlContact'})]
	Link_To = Link_To[0].replace('\n\n','')
	try:
		Link_To_M = [i.text.encode('utf8') for i in soup.find_all('tbody')]
		Link_To_M = Link_To_M[0].replace('\n\n','')
	except:
		Link_To_M = ''
		pass

	for x in xrange(len(bodies)):
		my_dict[labels[x]] = bodies[x]

	my_dict['Reference'] = links[link_num]
	my_dict['Link_To'] = Link_To
	my_dict['Link_To_M'] = Link_To_M
	dict_list.append(my_dict)		

	print link_num+1, '\n', links[link_num], ' Finished'
	print my_dict, '\n\n'	


f = open('sdvg_full.csv', 'wb+')
x = []
[x.extend(i.keys()) for i in dict_list]
Labels = set(x)
w = csv.DictWriter(f,Labels)
w.writeheader()
num = 0
for d in dict_list:
	num += 1
	try:
		w.writerow(d)
	except Exception as e:
		print num, e
		continue

f.close()