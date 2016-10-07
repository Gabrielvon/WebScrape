# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import requests, re, time, pickle, csv
from bs4 import BeautifulSoup
from random import randint

class LinkedIn_Crawl:	

	def __init__(self,username,password):
		self.username = username
		self.password = password		

	def phamton(self,UserAgent=None):
		print 'Starting PhantomJS...'
		if UserAgent:
			dcap = dict(DesiredCapabilities.PHANTOMJS)
			dcap["phantomjs.page.settings.userAgent"] = (UserAgent)
			self.driver = webdriver.PhantomJS(desired_capabilities=dcap)
		else:
			self.driver = webdriver.PhantomJS()                        

		time.sleep(3)

	def chrome(self, UserAgent=None):		
		print 'Starting Chrome...'
		if UserAgent:
			opts = Options()		
			opts.add_argument("user-agent={UA}".format(UA=UserAgent))
			self.driver = webdriver.Chrome(chrome_options=opts)
		else:
			self.driver = webdriver.Chrome()
		time.sleep(3)						

	def login(self):
		self.driver.implicitly_wait(30)
		self.driver.get('https://www.linkedin.com/uas/login')
		login_email = self.driver.find_element_by_xpath('//*[@id="session_key-login"]')
		login_email.clear()
		login_email.send_keys(self.username)
		login_password = self.driver.find_element_by_xpath('//*[@id="session_password-login"]')
		login_password.clear()
		login_password.send_keys(self.password)
		submit = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn-primary"]')))
		submit = self.driver.find_element_by_name('signin').click()

	def save_cookies(self, file_path_to_save):
		if 'phantomjs' in self.driver.name:
			LINE1 = "document.cookie = '{name}={value}; path={path}; domain={domain}; expires={expires}';\n"
			LINE2 = "document.cookie = '{name}={value}; path={path}; domain={domain}';\n"
			with open(file_path_to_save, 'w') as file :
				for cookie in self.driver.get_cookies() :
					try:
					    file.write(LINE1.format(**cookie))
					except:
						file.write(LINE2.format(**cookie))
		elif 'chrome' in self.driver.name:
			with open(file_path_to_save, 'w') as file :
				pickle.dump(self.driver.get_cookies(),file)								
		else:
			raise AssertionError('This function only accept PhantomJS and Chrome')

	
	def load_cookies(self, file_path_to_load):
		if 'phantomjs' in self.driver.name:
			with open(file_path_to_load, 'r') as file:
				self.driver.execute_script(file.read())
		elif 'chrome' in self.driver.name:
			cookies = pickle.load(open(file_path_to_load, "r"))
			for cookie in cookies:
			    self.driver.add_cookie(cookie)										
		else:
			raise AssertionError('This function only accept PhantomJS and Chrome')		

	def get(self,link):
		self.driver.implicitly_wait(120)
		self.driver.get(link)
		return self.driver.current_url

	def current_page_soup(self):
		self.soup = BeautifulSoup(self.driver.page_source,"html.parser")			
		return self.soup

	def retrieve_info_from_body_session(self, body_session):		
		Name = body_session.find_all('a',{'class','main-headline'})
		name = Name[0].text.encode('utf-8')
		profile_link = Name[0]['href'].encode('utf-8')			

		Desc = body_session.find_all('div',{'class','description'})
		desc = Desc[0].text.encode('utf-8') if Desc else []

		link_msg = body_session.find('a',{'class','primary-action-button'})
		link_msg = link_msg['href'].encode('utf8') if link_msg else []		

		if ('messaging/compose?connId=' in link_msg) | ('msgToConns?displayCreate=&connId=' in link_msg):
			pat = re.compile(r'connId=\d*')
			connID = re.findall(pat,link_msg)[0]
			link_msg_box = 'https://www.linkedin.com/messaging/compose?' + connID + '&subject=&body='
		else:
			link_msg_box = ''

		info = [name, desc, profile_link, link_msg_box]				
		return info				    

	def click_button(self, partial_link_text):
		try:
			self.driver.implicitly_wait(10) 
			Next_button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, partial_link_text)))
			Next_button.click()
			time.sleep(randint(5,10))    
		except Exception as e:
			print e
			print 'Maybe multiple button with partially same link_text occurs.'	

	def total_result(self):
		search_info = self.driver.find_element_by_class_name('search-info').text
		total_results = re.findall(r'\d+',search_info)[0].encode('utf8')
		print 'total_results:' , total_results
		return total_results

	def pause(self):
		programPause = raw_input("Press the <ENTER> key to continue...")

	def close(self):
		self.driver.close()

	def Crawl_By_Location(self,location_code,start_page_num=1):
		Results_Link = 'https://www.linkedin.com/vsearch/p?openAdvancedForm=true&locationType=Y&f_G={}&rsid=108067751474267063351&orig=ADVS&openFacets=N,G,CC&page_num={}&pt=people&f_N=F'.format(location_code,start_page_num)
		self.get(Results_Link)	
		time.sleep(randint(5,10))
		self.total_result()
		Note = ''

		try:
			WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="results"]/li[1]/div/h3/a')))
			print "Page is ready!"
		except Exception as e:
			print "Loading took too much time!"
			Note = 'Check link:   ' + Results_Link

		num_of_visit += 1
		time.sleep(randint(5,10))
		search_info = self.driver.find_element_by_class_name('search-info').text
		total_results = re.findall(r'\d+',search_info)[0].encode('utf8')
		print 'total_results:' , total_results

		try:
			WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="results"]/li[1]/div/h3/a')))
			print "Page is ready!"
		except Exception as e:
			Note = 'Check link:   ' + Results_Link
			print "Loading took too much time!",Note	

		flag = 1
		num_of_click = 1
		
		while flag==1: 					
			time.sleep(5)
			current_pagenum = num_of_click+start_page_num-1
			current_url = self.driver.current_url
			if '/vsearch/' not in current_url:
				print 'CHECK THE ERROR LINK: ', current_url
				time.sleep(30)
				self.driver.implicitly_wait(120)
				next_url = 'https://www.linkedin.com/vsearch/p?openAdvancedForm=true&locationType=Y&f_G=us%3A70&f_I={}&rsid=472653141474658107851&orig=ADVS&f_N=F&page_num={}&pt=people'.format(indus,current_pagenum)
				self.get(next_url)

			soup = BeautifulSoup(self.driver.page_source,"html.parser")	
			print '\n\nProcess: Page %d,  Industry = %d-%s' %(current_pagenum,industry_value,industry_name), '\n', current_url, '\n'		
			bodies = soup.find_all('div',{'class','bd'})
			for body in bodies:	
				name, desc, profile_link, link_msg_box = retrieve_info_from_body_session(body)
				if name in profiles: continue						
				info = [name, desc, profile_link, link_msg_box, industry_name, industry_value, Note]
				writer.writerow(info)
				print [name, industry_name, industry_value, Note], 'recorded.'
				infos.append(info)

			pagelinks = soup.find_all('a',{'class','page-link'})
			pagetext = [num.text for num in pagelinks]		
			flag = sum(['Next' in item for item in pagetext])

			if flag:		
				try: 
					click_button('Next')
					num_of_click += 1
				except Exception as e:
					print e
					msg = raw_input('If this is the last page, please press <ENTER>')
					try:
						click_button('Next')
						num_of_click += 1
					except:
						msg = raw_input('If this is the last page, please press <ENTER>')
						break		

	def Crawl_By_Industry(self,start_page_num=1,file_path_to_save='Crawl_By_Industry.csv'):
		all_indus_idxes = [47,94,120,125,127,19,50,111,53,52,41,12,36,49,138,129,54,90,51,128,118,109,3,5,4,48,24,25,91,18,65,1,99,69,132,112,28,86,110,76,122,63,43,38,66,34,23,101,26,29,145,75,148,140,124,68,14,31,137,134,88,147,84,96,42,74,141,6,45,46,73,77,9,10,72,30,85,116,143,55,11,95,80,97,135,126,17,13,139,71,56,35,37,115,114,81,100,57,113,123,87,146,61,39,15,131,136,117,107,67,83,105,102,79,98,78,82,62,64,44,40,89,144,70,32,27,121,7,58,20,33,104,22,8,60,130,21,108,92,59,106,16,93,133,142,119,103]
		flinks = open(file_path_to_save, 'w+') 
		num_of_visit = 1
		Note = ''
		for indus in all_indus_idxes:
			time.sleep(randint(10,20))
			writer = csv.writer(flinks,delimiter=',')
			reader = csv.reader(flinks)
			profiles = [row[0] for row in reader]
			Results_Link = 'https://www.linkedin.com/vsearch/p?openAdvancedForm=true&locationType=Y&f_G=us%3A70&f_I={}&rsid=472653141474658107851&orig=ADVS&f_N=F&page_num={}&pt=people'.format(indus,start_page_num)
			try:
				print 'Loading industry(%d)...\n' %indus
				self.driver.implicitly_wait(120)
				self.driver.get(Results_Link)	
			except Exception as e:
				print e
				print 'Error occurs: ', indus, ' --- ', Results_Link
				break

			num_of_visit += 1
			time.sleep(randint(5,10))
			total_results = self.total_result()
			if int(total_results)==0: continue

			try:
				WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="results"]/li[1]/div/h3/a')))
				print "Page is ready!"
			except Exception as e:
				Note = 'Check link:   ' +  Results_Link
				print "Loading took too much time!",Note
				break		

			flag = 1
			num_of_click = 1
			infos = []
			
			while flag==1: 					
				time.sleep(5)
				current_pagenum = num_of_click+start_page_num-1
				current_url = self.driver.current_url
				if '/vsearch/' not in current_url:
					print 'CHECK THE ERROR LINK: ', current_url
					time.sleep(30)
					driver.implicitly_wait(120)
					next_url = 'https://www.linkedin.com/vsearch/p?openAdvancedForm=true&locationType=Y&f_G=us%3A70&f_I={}&rsid=472653141474658107851&orig=ADVS&f_N=F&page_num={}&pt=people'.format(indus,current_pagenum)
					self.get(next_url)

				soup = self.current_page_soup()
				industry_name = soup.find_all('li',{'class','pivot'})[2].contents[0]
				industry_name = industry_name.encode('utf8').split(':')[1].strip()
				industry_value = indus

				print '\n\nProcess: Page %d,  Industry = %d-%s' %(current_pagenum,industry_value,industry_name), '\n', current_url, '\n'		
				bodies = soup.find_all('div',{'class','bd'})
				for body in bodies:	
					name, desc, profile_link, link_msg_box = self.retrieve_info_from_body_session(body)
					if name in profiles:
						print name, ' existed.'
						continue	
					info = [name, desc, profile_link, link_msg_box, industry_name, industry_value, Note]
					writer.writerow(info)
					print [name, industry_name, industry_value, Note], 'recorded.'
					infos.append(info)


				pagelinks = soup.find_all('a',{'class','page-link'})
				pagetext = [num.text for num in pagelinks]		
				flag = sum(['Next' in item for item in pagetext])

				if flag:		
					try: 
						self.click_button('Next')
						num_of_click += 1
					except Exception as e:
						print e
						msg = raw_input('If this is the last page, please press <ENTER>')
						try:
							self.click_button('Next')
							num_of_click += 1
						except:
							msg = raw_input('If this is the last page, please press <ENTER>')
							break

			num_of_visit += num_of_click
			self.infos = infos
			self.num_of_visit = num_of_visit
			print 'Visit Times: ', num_of_visit
			# if num_of_visit >= 100 and len(infos)>800:
			# 	print 'Visit times is over 100 or number of extractions is over 800.'
			# 	print 'Current Progress: num_of_visit:{}, num_of_click:{},industry:{} {}'.format(num_of_visit,num_of_click,industry_value,industry_name)

		flinks.close()
		self.close()

if __name__ == '__main__':
	loginEmail = 'alex@visionary.is'
	loginPassword = 'linkedinAugust'	
	lkc = LinkedIn_Crawl(loginEmail, loginPassword)
	mychrome = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
	mysafari = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50"

	lkc.phamton(UserAgent=mysafari)
	lkc.login()
	# lkc.save_cookies('../Cookies/alex_phamton_20161006.js')
	lkc.get('https://www.linkedin.com')
	lkc.load_cookies('../Cookies/alex_phamton_20161006.js')

	lkc.chrome(UserAgent=mychrome)
	lkc.login()

	lkc.Crawl_By_Industry()


