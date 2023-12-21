import os
import requests
import xmltodict
import urllib.request

def opensession(qrzuser, qrzpass):
	url = "https://xmldata.qrz.com/xml/current/?username="
	url += qrzuser + "&password=" + qrzpass + "&agent=q5.0"
	#print(url)
	try:
		file = urllib.request.urlopen(url)
		#print(file.status)
	
		try:
			data = file.read()
			file.close()
			data = xmltodict.parse(data)
			session_key = data['QRZDatabase']['Session']['Key']
			f = open('cache.txt', 'w')
			f.write(session_key)
			f.close()
			sessionlist = [True]
			#print('try')
			
		except KeyError:    
			#print('exception')
			error_key = data['QRZDatabase']['Session']['Error']
			sessionlist = [False, error_key]
		finally:
			return sessionlist
	except  urllib.error.URLError:
		sessionlist = [False,"Could not reach URL"]
		#print('else')
		return sessionlist

		

def qrz_lookup(call):
	qrz_key_lst = ['fname', 'addr2', 'country', 'grid']
	f = open('cache.txt','r')
	qkey = f.readline()
	
	try:
		url2 = 'https://xmldata.qrz.com/xml/current/?s='
		file1 = urllib.request.urlopen(url2 + qkey + ";callsign=" + call)
			
		# print(file1.status)
		if file1.status == 200:
			qrz_lookup = file1.read()
			file1.close()
			qrz_data = xmltodict.parse(qrz_lookup)
			try:
				qrz_data = qrz_data['QRZDatabase']['Callsign']
				resultlst = []
				for elem in range(len(qrz_key_lst)):
					resultlst.append(qrz_data[qrz_key_lst[elem]])
					
				return resultlst
				
			except KeyError:
				resultlst = ['error', 'ok']
			#print('else')	
			return resultlst
			
	except urllib.error.URLError:
			resultlst = ['error', 'fail', 'URL connection lost']
			return resultlst
	
		







