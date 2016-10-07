# This script crawls all profile content from file 'lica_links.csv'

# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#Spider 1

import requests, csv
from bs4 import BeautifulSoup



with open('ted_links.csv','rb+') as flinks:
	reader = csv.reader(flinks)
	links = [row[0] for row in reader]

# print links

def getsoup(url):
	source_code = requests.get(url)
	content = source_code.content
	soup = BeautifulSoup(content,"html.parser")
	return soup


dict_list = []
f = open('ted_speakers.csv', 'wb+')
Labels = ['Full Name', 'Headline', 'Personal Links', 'Submenu Links', 'Profile Introduction', 'Talk Briefing', 'Other Talks', 'More Information']
w = csv.DictWriter(f,Labels)
w.writeheader()

for link_num in xrange(len(links)):
	soup = getsoup(links[link_num])

	fullname = soup.find('h1',{'class','profile-header__name'}).text.encode('utf-8')
	headline = soup.find('div',{'class','profile-header__summary'}).text.encode('utf-8').strip()

	header_links = soup.find('div',{'class','profile-header__links__inner'}).find_all('a')
	indi_links = []
	for item in header_links:
		link_text = item.text.encode('utf-8')
		link_link = item['href'].encode('utf-8')
		indi_links.append(link_text+link_link.strip())

	submenu_links = soup.find_all('li',{'class','submenu__item'})
	submenu_urls = []
	for item in submenu_links:
		child_url = item.find('a')['href']
		fullurl = 'http://www.ted.com'+child_url
		submenu_urls.append(fullurl)

	profile_intro = soup.find('div',{'class','profile-intro'}).text.encode('utf-8')
	talk_brief = soup.find('div',{'class','section--minor'}).text.encode('utf-8').strip()

	talks = soup.find_all('div',{'class','talk-link'})
	other_talk_links = []
	for item in talks:
		topic = item.find('div',{'class','media__message'}).find('a').text.encode('utf-8').strip()
		child_url = item.find('div',{'class','media__message'}).find('a')['href'].encode('utf-8')
		fullurl = 'http://www.ted.com'+child_url
		other_talk_links.append(topic+'\n'+fullurl+'\n\n')

	others = soup.find_all('div',{'class','profile-blog'})
	more_infos = []
	for item in others:
		more_info = item.text.encode('utf8').lstrip()
		more_infos.append(more_info)

	my_dict = dict()
	my_dict['Full Name'] = fullname
	my_dict['Headline'] = headline
	my_dict['Personal Links'] = ''.join(indi_links)
	my_dict['Submenu Links'] = ''.join(submenu_urls)
	my_dict['Profile Introduction'] = ''.join(profile_intro)
	my_dict['Talk Briefing'] = ''.join(talk_brief)
	my_dict['Other Talks'] = ''.join(other_talk_links)
	my_dict['More Information'] = ''.join(more_infos)

	dict_list.append(my_dict)		

	print link_num+1, '\n', links[link_num], ' Finished'
	print my_dict, '\n\n'	

	try:
		w.writerow(my_dict)
	except Exception as e:
		w.writeheader
		print e
		continue


f.close()