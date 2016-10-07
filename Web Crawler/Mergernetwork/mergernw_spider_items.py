# This script crawls all profile content from file 'lica_links.csv'

# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import requests, csv, re, time, pickle
from random import randint
from bs4 import BeautifulSoup

def save_cookies(requests_cookiejar, filename):
    with open(filename, 'wb') as f:
        pickle.dump(requests_cookiejar, f)

def load_cookies(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

def getsoup(url,cookie):
	source_code = requests.get(url,cookies=cookie)
	content = source_code.content
	soup = BeautifulSoup(content,"html.parser")
	return soup

def split_full_name(full_name):
	fulln = full_name.split(' ')	
	firstn = fulln[0]
	other = ' '.join(fulln[1:])
	return firstn,other

with open('csv/mergernw_links.csv','r') as flinks:
	reader = csv.reader(flinks)
	links = [row[0] for row in reader]

# #save cookies
# r = requests.get(url)
# save_cookies(r.cookies, filename)

f = open('csv/mergernw_member6.csv','wb+')
reader = csv.reader(f)
name_existed = [i[0] for i in reader]

Label = ['Full Name', 'First Name', 'Last Name', 'Post', 'Followers', 'Following', 'Location','Industry','Languages','Membership',
	'Identity Verified','Follows You', 'Brief', 'People To Know', 'Reference']
writer = csv.DictWriter(f, Label)
writer.writeheader()

num_of_row = 1
num_of_start = 7570
# num_of_start = 
cookie = load_cookies('mergernw.pkl')
for num in xrange(len(links)):
	try:
		url = links[num+num_of_start]
		soup = getsoup(url,cookie)
	except Exception as e:
		print e
		print "Stopped Time: ", time.asctime()
	except IndexError as e:
		print 'Finished'
		print "Stopped Time: ", time.asctime()
		break
	print 'Processing:  %d/%d  ' %(num_of_row, num_of_row+num_of_start-1), url	

	if ('Page Not Found' in soup.text) | ('has a private profile' in soup.text):
		print 'Page Not Found | Private Profile' 
		print soup.text, '\n\n'
		continue

	try:
		stats = soup.find('ul',{'class','nav-tabs'}).find_all('strong')
	except:
		time.sleep(600)
		soup = getsoup(url,cookie)

	fullname = soup.find_all('h1')[0].text.encode('utf8').strip()
	if fullname in name_existed:
		print 'Existed: ', fullname
		continue

	fn, ln = split_full_name(fullname)
	hl = soup.find_all('h2')[0].text.encode('utf8')
	clean_hl = filter(None, hl.strip().split('\t'))
	title = clean_hl[0].strip()
	try:
		company = clean_hl[1].strip()
	except:
		company = ''
	stats = soup.find('ul',{'class','nav-tabs'}).find_all('strong')
	num_of_post = stats[1].text.encode('utf8')
	num_of_followers = stats[2].text.encode('utf8') 
	num_of_following = stats[3].text.encode('utf8') 

	panels = []
	panel_body = soup.find('div',{'class','panel-body'}).text.encode('utf8').split('\n')
	for item in panel_body:
		item_strip = item.strip()
		if item_strip:
			panels.append(item_strip)

	panels.remove('Languages:')
	location, indus, lang, membership, identity_verified, follows_you = panels[:6]
	identity_verified = re.sub('Identity Verified: ', '', identity_verified)
	follows_you = re.sub('Follows You: ', '', follows_you)
	brief = ' '.join(panels[6:])

	Ppl_To_Know = ''
	list_group = soup.find('div',{'class','list-group'}).find_all('div',{'class','row'})
	for item in list_group:
		body = re.sub('\n+','\n',item.text.encode('utf8')).lstrip()
		body = re.sub('\n ','\n',body)
		link = 'https://mergernetwork.com' + item.find('a',href=True)['href'].encode('utf8')
		Ppl_To_Know = Ppl_To_Know + body + link + '\n\n'


	print 'Full Name: ', fullname
	print 'Followers: ', num_of_followers
	print 'Reference: ', url,'\n'

	mydict = {'Full Name': fullname, 'First Name': fn, 'Last Name': ln, 'Post': num_of_post, 
		'Followers': num_of_followers, 'Following': num_of_following, 'Location': location,
		'Industry': indus, 'Languages': lang, 'Membership': membership,
		'Identity Verified': identity_verified, 'Follows You': follows_you, 'Brief': brief, 
		'People To Know': Ppl_To_Know, 'Reference': url}
	writer.writerow(mydict)
	time.sleep(randint(5,20))

	num_of_row += 1
	if num_of_row % 1000 == 0:
		time.sleep(randint(1800,3600))

f.close()

# Label = lnki_all[0].keys()
# fi = open('csv/Alex_1stConn_ALL_NoHold.csv','wb+')
# w = csv.DictWriter(fi, Label)
# w.writeheader()
# for info in infos:
# 	w.writerow(info)

# fi.close()	
