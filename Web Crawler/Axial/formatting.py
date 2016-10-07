import csv,re

info = []
with open('axial.csv','rb') as finfo:
	reader = csv.reader(finfo)
	for row in reader:
		info.append(row)
		
for i in xrange(len(info)):
	if i == 0:
		continue
	cType_Loc = info[i][1]
	cTypeLoc = re.split('[()]',cType_Loc)
	cType = cTypeLoc[0]
	cCity = cTypeLoc[1].split(',')[0]
	cStateCountry = cTypeLoc[1].split(',')[1]
	print i, '   ', cType, '||', cCity, '||', cStateCountry

