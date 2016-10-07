# This script process the following:
# 1. login linkedin account
# 2. download all links for composing message to 1st connections
# 3. Export links to csv file

# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests, re, time, traceback, csv
from bs4 import BeautifulSoup
from random import randint


url_login = 'https://www.linkedin.com/uas/login'
driver = webdriver.Chrome()
driver.get(url_login)
# loginEmail = 'alex@visionary.is'
# loginPassword = 'linkedinAugust'
# # loginEmail = 'yangbodu@alum.mit.edu'
# # loginPassword = 'Rh31nh3$$en_'
loginEmail = 'fwlg1113@gmail.com'
loginPassword = '1532awds1231A'
login_email = driver.find_element_by_xpath('//*[@id="session_key-login"]').send_keys(loginEmail)
login_password = driver.find_element_by_xpath('//*[@id="session_password-login"]').send_keys(loginPassword)
driver.implicitly_wait(10)
# time.sleep(5)
submit = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btn-primary"]')))
submit = driver.find_element_by_name('signin').click()

def pause():
    programPause = raw_input("Press the <ENTER> key to continue...")

def search(keys):
	elem_search_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'main-search-box')))
	time.sleep(randint(1,3))
	elem_search_box.send_keys('\b'*1000)
	time.sleep(randint(1,3))
	for key in keys:
		try:
			elem_search_box.send_keys(key)
		except:
			pass

	driver.implicitly_wait(10)
	try:
		elem_search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'search')))
		elem_search_button.click()	
		time.sleep(randint(1,3))
	except:
		elem_search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="global-search"]/fieldset/button')))	
		elem_search_button.click()	
		time.sleep(randint(1,3))
	

	try:
		elem_1st_result = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="results"]/li[2]/div/h3/a')))	
		time.sleep(randint(1,3))
		elem_1st_result.click()	
		time.sleep(randint(1,3))
	except Exception as e:
		pass

	src_code = driver.page_source.encode('utf8')
	soup = BeautifulSoup(src_code,"html.parser")
	return soup

def get_profile(soup):
	profile_name = soup.find('span',{'class','full-name'})
	profile_name = profile_name.text.encode('utf-8') if profile_name else []
	profile_link = soup.find('a',{'class','view-public-profile'})
	profile_link = profile_link.text.encode('utf-8') if profile_link else []	

	profile_position = soup.find('p',{'class','title'})
	profile_position = profile_position.text.encode('utf-8') if profile_position else []
	profile_location = soup.find('a',{'name','location'})
	profile_location = profile_location.text.encode('utf-8') if profile_location else []
	profile_headline = soup.find('a',{'name','industry'})
	profile_headline = profile_headline.text.encode('utf-8') if profile_headline else []
	profile_curr_comp = soup.find('tr',{'id','overview-summary-current'})
	profile_curr_comp = profile_curr_comp.find('td').text.encode('utf-8') if profile_curr_comp else []	

	return [profile_name, profile_link, profile_position, profile_location, profile_headline, profile_curr_comp]


Namelists = []
Namelists2 = []
with open('sdvg_full.csv','r') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		Namelists.append([row['First name'], row['Last name'], row['Company']])
		Namelists2.append([row['First name'], row['Last name'], row['Business Type']])


csvfile = open('sdvg_linkedin2.csv','r+')
writer = csv.writer(csvfile)
writer.writerow(['First Name','Last Name','linkedin_name','LinkedIn'])

profiles = [] 
for num in range(70,len(Namelists)):
	if Namelists[2]:
		print '\n\n',str(num+1),'  Searching_By_Company\n'
		original_name = Namelists[num]
		search_text = ', '.join(original_name)
		first_results_soup = search(search_text)
		linkedin_name, linkedin_link = get_profile(first_results_soup)
		if linkedin_link:		
			profile = [' '.join(original_name[:2]), linkedin_name, linkedin_link, 'Search_By_Company']
			print profile,'\n'
		else:
			print str(num+1),'  Searching_By_Type\n'
			original_name = Namelists2[num]
			search_text = ', '.join(original_name)
			first_results_soup = search(search_text)
			linkedin_name, linkedin_link = get_profile(first_results_soup)
			if linkedin_link:		
				profile = [' '.join(original_name[:2]), linkedin_name, linkedin_link, 'Search_By_Type']
				print profile,'\n'
			else:
				print '\nAnomaly occurs when searching ', search_text,'\n'
				profile = [' '.join(original_name[:2]),'','','Anomaly occur. Double check manually.']
	else:
		print str(num+1),'  Company is empty. Searching_By_Type\n'
		original_name = Namelists2[num]
		search_text = ', '.join(original_name)
		first_results_soup = search(search_text)
		linkedin_name, linkedin_link = get_profile(first_results_soup)
		if linkedin_link:		
			profile = [' '.join(original_name[:2]), linkedin_name, linkedin_link, 'Search_By_Type']
			print profile,'\n'
		else:
			print '\nAnomaly occurs when searching ', search_text,'\n'
			profile = [' '.join(original_name[:2]),'','','Anomaly occur. Double check manually.']		

	writer.writerow(profile)
	print 'Recorded\n'
	profiles.append(profile)

	if num >= 200:
		pause()

		
csvfile.close()		

		

# with open('sdvg_linkedin.csv','wb+') as csvfile:
# 	writer = csv.writer(csvfile)
# 	writer.writerow(['First Name','Last Name','Company','LinkedIn'])
# 	for row in profiles:
# 		writer.writerow(row)

