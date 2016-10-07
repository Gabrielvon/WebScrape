# This script crawls all profile content from file 'lica_links.csv'

# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#Spider 1

import requests, csv
from bs4 import BeautifulSoup



with open('lica_links.csv','rb+') as flinks:
	reader = csv.reader(flinks)
	links = [str(row[0]).replace(" ","") for row in reader]

# print links

def getsoup(url):
	source_code = requests.get(url)
	content = source_code.content
	soup = BeautifulSoup(content,"html.parser")
	return soup

dict_list = []
for link_num in xrange(len(links)):
	soup = getsoup(links[link_num])
	Name = soup.find('h2').text.encode('utf-8')
	Company = soup.find('h3').text.encode('utf-8')
	div_fieldLabel = soup.find_all('div',{'class','fieldLabel'})
	Label = [item.text.encode('utf-8').strip() for item in div_fieldLabel]	
	div_fieldBody = soup.find_all('div',{'class','fieldBody'})
	Body = [item.text.encode('utf-8').strip() for item in div_fieldBody]
	Label[0] = 'Full Name'	
	Body[0] = Name
	my_dict = {}
	for x in xrange(len(Body)):
		my_dict[Label[x]] = Body[x]

	del_exception = ['Logo/Photo','\xc2\xa0']
	for del_e in del_exception:
		if del_e in Label:
			try: 
				my_dict.pop(del_e)
			except:
				pass

	my_dict['Reference'] = links[link_num]
	dict_list.append(my_dict)		

	print link_num+1, '\n', links[link_num], ' Finished'
	print my_dict, '\n\n'	

Label.append('Reference')

f = open('info.csv', 'wb+')
w = csv.DictWriter(f, Label)
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



# Full_name
# Membership_level
# First_name
# Last_name
# Email
# Phone
# Company
# Company_desc
# Website
# Reference


