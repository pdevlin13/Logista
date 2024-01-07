# version 1.0.2
# QRZ Lookup module by MW0PDV

import os
import requests
import xmltodict
import urllib.request

# open QRZ session and cache session key

def opensession(qrzuser, qrzpass):
	url = "https://xmldata.qrz.com/xml/current/?username="
	url += qrzuser + "&password=" + qrzpass + "&agent=Logista"
	#print(url)
	try:
		file = urllib.request.urlopen(url)
		#print(file.status)
	
		try:   #  check if a session key was generated and return the error if not
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

		
# Querry QRZ with session key and return the key values in qrz_key_lst

def qrz_lookup(call):
	#qrz_key_lst = ['fname', 'addr2', 'country', 'grid']
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
				fname_exist = False
				# test if fname key exist if not use name and format
				if 'fname' in qrz_data.keys():
					qrz_key_lst = ['fname', 'addr2', 'country', 'grid']
					fname_exist = True
				else:
					qrz_key_lst = ['name', 'addr2', 'country', 'grid']
					fname_exist = False
					
				resultlst = []
				
				for elem in range(len(qrz_key_lst)):
					resultlst.append(qrz_data[qrz_key_lst[elem]])
					
				if fname_exist is False:
					resultlst[0] = format_name(resultlst[0])  # format / clean name info
					
				return resultlst
				
			except KeyError:
				resultlst = ['error', 'ok']  # callsign not found
			#print('else')	
			return resultlst
	
	# this is to handle loss of connetion after a session was established		
	except urllib.error.URLError:
			resultlst = ['error', 'fail', 'URL connection lost']
			return resultlst
			
# function to format name, fname is not always used by QRZ user
def format_name(rawname):
	title_list = ['dr', 'mr', 'mr', 'miss', 'mrs', 'ms','doc', 'prof']
	namelst = rawname.split()
	
	if len(namelst) > 1:
		if namelst[0].lower() in (title_list):
			fname = namelst[1]
		else:
			fname = namelst[0]
	else:
		fname = rawname
		
	return fname
	







