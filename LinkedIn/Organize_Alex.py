import csv,re

def fixname(Nameline):
	a = re.sub(r'\([^)]*\)','', Nameline) #remove parenthesis
	b = re.sub(r'\[[^)]*\]','', a) #remove bracket	
	c = b.split(',')[0]
	# pat = re.compile(r'^\w*\S*\w$')
	# d = re.findlnki(pat,c)
	return c

def csv2dict(filename,access):	
	with open(str(filename),str(access)) as csvfile:
		mydict = list(csv.DictReader(csvfile))
	return mydict	

def Area_Config(x):
    return {
    	'LA': 'Log Angeles',
        'SF': 'San Francisco',
        'SD': 'San Diego',
    }[x]

def Area_Hash(x):
    return {
    	'LA': 'us%3A49',
        'SF': 'us%3A84',
        'SD': 'us%3A732',
    }[x]	


############### Import CSV Files ###############
# From saleforce
onhold = csv2dict('csv/Alex Salzman HOLD 20160912 - Sheet1.csv','r')
onhold[-6:] = []

# From linkedin webcrawler
# Area_Code = '##' #Please double check this.
Area_Code = 'SF' #Please double check this.
Area = csv2dict('csv/Alex_1stConn_%s.csv' %Area_Hash(Area_Code),'r') 
Area = [(item['Full Name'], item['Headline']) for item in Area]
Area_Unique = list(set(Area))

# From linkedin offical exporter
lnki = []
with open('csv/alex_linkedin_connections_export_microsoft_outlook.csv','rb+') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		lnki_old_name = ['E-mail Address', 'First Name', 'Company', 'Job Title', 'Last Name']
		lnki_new_name = ['Email', 'First Name', 'Account Name', 'Title', 'Last Name']
		mydict = {lnki_new_name[idx]: row[lnki_old_name[idx]] for idx in xrange(len(lnki_old_name))}
		lnki.append(mydict)	

############### Integrate and Process ###############
lnki_Name = [fixname(item['First Name']+' '+item['Last Name']) for item in lnki]
Hold = [[item['First Name']+' '+item['Last Name'], item['Email']] for item in onhold]
Hold_Name = [item[0] for item in Hold]

hold_in_list = [] 
for name in Hold_Name:
	fn = name.split(' ')[0]
	ln = name.split(' ')[1]
	print 'On hold: ', name
	for item in Area_Unique:			
		fn_s = re.search(fn, item[0])
		ln_s = re.search(ln, item[0])		
		if fn_s and ln_s and name:	
			print 'Remove:', item, '---------- Checked'
			hold_in_list.append(item)	
			Area_Unique.remove(item)
			break


infos = []
for item in Area_Unique:
	try:
		idx = lnki_Name.index(item[0])
		pat = r'\W?(inc|llc|ltd|llp|lp)\W?'		
		lnki[idx]['Account Name'] = re.sub(pat, '', lnki[idx]['Account Name'], flags=re.I).strip()
		lnki[idx]['Mailing City'] = Area_Config(Area_Code)
		lnki[idx]['Mailing State/Province'] = 'CA'
		infos.append(lnki[idx])
	except Exception as e:
		print e
		pass

# first_conn = list(set(Area))
# first_conn_nohold = len(Area_Unique)	
# first_conn_nohold_email = len(infos)
# first_conn_nohold_noemail = len(Area_Unique) - len(infos)



Label = ['Email','First Name', 'Account Name', 'Title', 'Last Name', 'Mailing City', 'Mailing State/Province']
fi = open("csv/ReadyToUpload/test_Alex's 1st Connections LinkedIn %s 20160924.csv" %Area_Config(Area_Code),'wb+')
# fi = open("csv/ReadyToUpload/Alex's 1st Connections LinkedIn Los Angeles 20160924.csv",'wb+')
# fi = open("csv/ReadyToUpload/Alex's 1st Connections LinkedIn San Francisco 20160924.csv",'wb+')
# fi = open("csv/ReadyToUpload/test_Alex's 1st Connections LinkedIn San Diego 20160924.csv",'wb+')
w = csv.DictWriter(fi, Label)
w.writeheader()
for info in infos:
	w.writerow(info)

fi.close()
	
			




