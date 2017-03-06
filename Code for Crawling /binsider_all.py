# www.businessinsider.com
# We can easily find the time and title in the link.


# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import requests
from bs4 import BeautifulSoup
import re, time, traceback, csv

keywords = 'apple'

def getsoup(url):
	source_code = requests.get(url)
	content = source_code.content
	soup = BeautifulSoup(content,"html.parser")
	return soup

def binsider(keywords):
	########----------Find the page ranges----------########
	print time.asctime(), ":     Finding the page ranges"
	statpage = 0
	endpage = 0
	statdate = re.compile(r'\w*.*, 2014')
	enddate = re.compile(r'\w*.*, 2015')
	for i in range(10000):
		try:
			page = i+1
			url = 'http://www.businessinsider.com/s?q=%s&vertical=&author=&contributed=1&sort=date&page=%d#' %(keywords,page)
			soup = getsoup(url)
		except Exception,e:
			print e
			time.sleep(60*20)			
			soup = getsoup(url)
		
		# Find pages
		g_data = soup.findAll('span',{'data-bi-format':'date'})

		#Start page
		if statpage == 0:
			for item in g_data:
				datetext = str(item.text)

				try:
					cdate1 = re.search(enddate,datetext).group()
					print cdate1
					statpage = page
					print 'Starting page = ', page
					break
				except:
					cdate1 = ""
					continue
			if statpage > 0:
				print "Starting Page Got"
		
		#Ending page
		for item in g_data:
			datetext = str(item.text)

			try:
				cdate2 = re.search(statdate,datetext).group()
				print cdate2
				endpage = page
				print 'Ending page = ', page
				break
			except:
				cdate2 = ""
				continue
		
		current = re.search(r'20\w\w',datetext).group()
		if (statpage >=1) & (endpage >=1):
			print "Ending Page Got"
			break
		else: 
			if(current < 2013): 
				print 'Cannot find articles from 2014 to 2015'
				statpage = 1
				endpage = 2
				break

	print time.asctime(), ":     Page ranges is from "+str(statpage)+" to "+str(endpage)		
	#################

	########----------Crawling Part 1----------########
	# statpage = 425 #get from former part
	# endpage = 431	#get from former part
	# endpage = 430
	tol = 5
	print time.asctime(), ":     Getting all links"

	links = []
	# flinks = open('binsiderlinks_all.csv','ab+')
	for i in range(statpage-1,endpage+tol):
		try:
			page = i+1
			url = 'http://www.businessinsider.com/s?q=%s&vertical=&author=&contributed=1&sort=date&page=%d#' %(keywords,page)
			soup = getsoup(url)
		except Exception,e:
			print e
			time.sleep(60*20)
			soup = getsoup(url)

		l_data =soup.find_all('a')
		for item in l_data:
			link = str(item.get('href'))
			pat = re.compile(r'http://www\.businessinsider\.com/\S*20\S*\d$')
			if re.search(pat,link) and (link not in links):
				# flinks.write(link+'\n')
				links.append(link)
	print time.asctime(), ":     All links retrived"
	###################


	########----------Crawling Part 2----------########
	ii = 0
	fart = open('binsiderart_all.csv','ab+')
	writer = csv.writer(fart)
	writer.writerow(['Number','keywords','Datetime','Title','Url','Text'])
	print '>>>>>-------Downloading Articles-------<<<<<'
	for link in links:
		try:
			soup = getsoup(link)
		except Exception,e:
			print e
			time.sleep(60*20)
			soup = getsoup(url)
			
		g_data = soup.find_all('div',{'class':'content post'})
		oneart = []
		for item in g_data:
			for art in item.findAll('p'):
				try:
					oneart.append(str(art.text.encode('utf8')))
				except Exception,e:
					# print 'oneart',e
					oneart = ['Article Is Not Available',str(e)]
					# continue

		tl_data = soup.find_all('div',{'class':'sl-layout-post'})
		for item in tl_data:
			for tt in item.find_all('h1'):
				try:
					title = tt.text.encode('utf8').strip()
				except Exception,e:
					# print 'title',e
					title = ['Title Is Not Available',str(e)]

		tm_data = soup.findAll('span',{'data-bi-format':'date'})
		for item in tm_data:
			try:
				datetime = str(item.text.strip())
			except Exception,e:
				# print 'datetime',e'
				datetime = ['Datetime Is Not Available',str(e)]

		ii += 1		
		try:
			alldata = ["%d" %ii, keywords, datetime, title, link, oneart,]
			writer.writerow(alldata)
			print title,'\n',datetime,'\n',link
			print 'Retrived Articles %d' %ii
			print '\n\n'	
		except Exception,e:
			print 'Error occurs when writing into csv: ',str(e),'\n\n'
			alldata = ["%d" %ii, keywords, '', '', link, '']
			writer.writerow(alldata)
			continue

	fart.close()
	print '\nGet', ii, 'articles\n'
	print time.asctime(), ':     All articles retrived and saved'

toget = ['AAPL', 'Apple Iphone', 'Ipad', 'Apple watch', 'macbook',' mac pro', 'Apple IOS', 'Apple OSX', 'Apple pay', 'Apple TV', 'retina', 'imac', 'Apple facetime', 'Apple siri', 'Apple Imessage', '3D touch', 'icloud', 'Apple', 'Ipod', 'Apple music', 'Apple support', 'Apple store', 'Apple service', 'Ibook', 'apple X service', 'apple Xsan', 'Timothy Donald Cook']
for word in toget:
	binsider(word)
