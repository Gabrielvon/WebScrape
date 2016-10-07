import csv,re,os

# def fixname(Nameline):
# 	a = re.sub(r'\([^)]*\)','', Nameline) #remove parenthesis
# 	b = re.sub(r'\[[^)]*\]','', a) #remove bracket	
# 	c = b.split(',')[0]
# 	# pat = re.compile(r'^\w*\S*\w$')
# 	# d = re.findlnki(pat,c)
# 	return c

def csv2dict(filename,access):	
	with open(str(filename),str(access)) as csvfile:
		mydict = list(csv.DictReader(csvfile))
	return mydict	


############### Import CSV Files ###############
# From saleforce
dircsv = os.listdir('csv')
dircsv.remove('.DS_Store')
dircsv.remove('mergernw_links.csv')
dircsv.remove('mergernw_member.csv')
dircsv.remove('mergernw.csv')

mydicts = []
for file in dircsv:
	mydict = csv2dict('csv/'+file,'r')
	print len(mydict)
	mydicts.extend(mydict)

tups = list()
k = mydicts[0].keys()
for item in mydicts:
	tup = tuple()
	for v in item.values():
		tup += (v,)
	tups.append(tup)

mergernw = []
fullname = []
fullname_ALL = []
for d in mydicts:
	fullname_ALL.append(d['Full Name'])
	if d['Full Name'] in fullname:
		continue
	mergernw.append(d)
	fullname.append(d['Full Name'])



fi = open("csv/mergernw.csv", 'wb+')
w = csv.DictWriter(fi, k)
w.writeheader()
for info in mergernw:
	w.writerow(info)

fi.close()
	
			




