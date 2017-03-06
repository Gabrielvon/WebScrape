# -*- coding:utf-8 -*-

import urllib
import chardet #字符集检测

def auto_detect(url):
	content = urllib.urlopen(url).read()
	result = chardet.detect(content) #检测编码类型
	encoding = result['encoding']
	return encoding



# urls = ['http://www.iplaypython.com',
# 		'http://www.baidu.com',
# 		'http://www.163.com',
# 		'http://www.jd.com',
# 		'http://www.dangdang.com'
# 		]

urls = ['http://bgr.com/2015/10/16/apple-tv-launch-date-november-5/',
		# 'http://www.xueqiu.com',
		# 'http://www.youtube.com',
		# 'http://www.wsj.com'
		]

for url in urls:
	print url, auto_detect(url)