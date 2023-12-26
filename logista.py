# version 1.1.2
# Logista is an iPad SOTA log tool by MW0PDV
# This tool is intended to assist in typing up a
# paper SOTA log. It will produce a SOTA csv v2 file and also and an ADIF(adi)
# file. The code is written to fulfill the
# needs of my logging workflow and it meets those needs for me as is :-)
# This code has been shared in order to help others who want to
# have a play with Pythonista and want a starting point or just use as is
# This code is designed to run natively in Pyhonista to allow the use of
# the iPad grahics user iteface.
# A pointer to note is that the graphcics file *.pyui is linked to *.py
# code by the function or method inserted in the action property field of the
# object properties window. This took me few hours to work out when
# first playing with Pythonista.


import os
import ui
import datetime
import time
import qrz_lookup

# this is the path to the Pythonist3 directory on iCloud 
icloud_path = "/private/var/mobile/Library/Mobile Documents"
icloud_path += "/iCloud~com~omz-software~Pythonista3/Documents/"


class logform(ui.View):          # initialise the variable associated with
	def __init__(self):       # with each object in the ui grphics file
		self.othersummit = ""				 # This prevents an undeclared if no data
		self.callsign = ""			 		# is entered into a field
		self.opcall = ""
		self.freq = ""
		self.mode = ""
		self.mysummit = ""
		self.timeon = ""
		self.name = ""
		self.srst = ""
		self.rrst = ""
		self.othersummit = ""
		self.comments = ""
		self.qth = ""
		self.country = ""
		self.grid = ""
		self.header = False
		self.prev_qso = []
		
		
		# check dir exists and if not create it
		if os.path.isdir(icloud_path + 'Log_Files') is False:
			os.mkdir(icloud_path + 'Log_Files')
		
			# setup filenames to use for the sssion increment file number if needed	
		adifchk = False
		i = 0
		while adifchk is not True:
			adifname = icloud_path + 'Log_Files/logista' + str(i) + '.adi'
			if os.path.isfile(adifname) is False:
				adifchk = True
			else:
				i += 1
		self.adifname = adifname
		
		sotafchk = False
		i = 0
		while sotafchk is not True:
			sotafname = icloud_path + 'Log_Files/sota' + str(i) + '.csv'
			if os.path.isfile(sotafname) is False:
				sotafchk = True
			else:
				i += 1
		self.sotafname = sotafname
		
		# load config from cfg.txt
		config = open('cfg.txt', 'r')
		cfgtext = config.read()
		qrzpassstart = cfgtext.find("qrzpass")
		qrzpassstart = cfgtext.find('[', qrzpassstart)
		qrzpassend = cfgtext.find(']', qrzpassstart)
		qrzpass = cfgtext[qrzpassstart + 1:qrzpassend]
		qrzuserstart = cfgtext.find("qrzuser")
		qrzuserstart = cfgtext.find('[', qrzuserstart)
		qrzuserend = cfgtext.find(']', qrzuserstart)
		qrzuser = cfgtext[qrzuserstart + 1:qrzuserend]
		
		qrzautostart = cfgtext.find("qrzauto")
		qrzautostart = cfgtext.find('[', qrzautostart)
		qrzauto = cfgtext[qrzautostart + 1:qrzautostart + 2]
		self.qrzauto = qrzauto
		
		# open QRZ sesion and cache key
		# 2 attempts will be made to open a session
		i = 0
		while i < 2:
			self.qrz_status = qrz_lookup.opensession(qrzuser, qrzpass)
			#print(self.qrz_status)
			if self.qrz_status[0] is True:
				break
			else:
				i += 1
				time.sleep(1)
				
				
	
# each of the get_xxx methods are a bindings to the pyui graphics file
# property field, each graphics object has the name of the function
# without the parenthasis i.e form.get_xx
# Enter or when focus moves from the cell causes the  method for
# that object to be called


	def get_call(self, sender):	  	  # binding to ui template file
		self.callsign = sender.text
		calltxt = v['callsign']
		calltxt.border_color = '0bc20b'

		if self.qrzauto == '1':
			self.lookup(sender)  # set object instance
				
	def get_opcall(self, sender):   # text from binding on ui template file
		self.opcall = sender.text
		
	def get_freq(self, sender):	  # text from binding on ui template file
		self.freq = sender.text
				
	def get_mode(self, sender):		# text from binding on ui template file
		self.mode = sender.text
						
	def get_mysummit(self, sender): 	# binding to ui template file
		self.mysummit = sender.text

	def get_time(self, sender):				# binding to ui template file
		self.timeon = str(sender.date)
		v['datetime'].border_color = '0bc20b'
				
	def get_timenow(self, sender):				# binding to ui template file
		x = datetime.datetime.utcnow()
		sender.superview['datetime'].date = x
		self.timeon = str(x)
		v['datetime'].border_color = '0bc20b'
		
	def timenow_vis(self,sender):
		if sender.value is True:
			v['timenow'].hidden = True
		else:
			v['timenow'].hidden = False
		
		
	def get_name(self, sender):		# binding to ui template file
		self.name = sender.text
			
	def get_qth(self, sender):		# binding to ui template file
		self.qth = sender.text
		self.clearqth = sender.superview['qth']
	
	def get_country(self, sender):		# binding to ui template file
		self.country = sender.text
		
	def get_grid(self, sender):		# binding to ui template file
		self.grid = sender.text
		
	def get_srst(self, sender):			# binding to ui template file
		self.srst = sender.text
	
	def get_rrst(self, sender):		# binding to ui template file
		self.rrst = sender.text
				
	def s2sswitch(self, sender):			# binding to ui template file
		self.switch = sender
		if self.switch.value is True:
			v['othersummit'].hidden = False
		else:
			v['othersummit'].hidden = True
		
	def get_othersummit(self, sender):			# binding to ui template file
		self.othersummit = sender.text
		self.clearothersummit = sender.superview['othersummit']  # set object
		
			
	def get_comments(self, sender = ""):		# binding to ui template file
		self.comments = sender.text
		
	def calcband(self, f):			# function to calculate band from frequency
		if f != "":
			band = 300 / (float(f))
			if band > 9:
				bandstr = (str((int(band / 10)) * 10)) + "M"
			elif band < 1:
				bandstr = "70cm"
			else:
				band = int(band)
				bandstr = (str(band)) + "M"
		else:
			bandstr = "0M"
		return bandstr
	
	# the method below calls qrz_lookup and handles the returned list	
	def lookup(self, sender):  #calls QRZ lookup module
		if self.qrz_status[0] is True:	
			qrz = qrz_lookup.qrz_lookup(self.callsign)
			
			if qrz[0] != 'error':
				obj_lst = ['name', 'qth', 'country', 'grid']
				var_lst = []
				i = 0
				for obj in obj_lst:
					sender.superview[obj].text = qrz[i]
					var_lst.append(qrz[i])
					i += 1
				self.name = var_lst[0]
				self.qth = var_lst[1]
				self.country = var_lst[2]
				self.grid = var_lst[3]
				v['qrz_status_lbl'].text = ""
			elif qrz[1] == "ok":
				sender.superview['name'].text = "QRZ: call not found"
			else:
				v['qrz_status_lbl'].text = "QRZ: connection lost"
		else:
			v['qrz_status_lbl'].text = "QRZ: " + self.qrz_status[1]
	
	def clearform(self):				# clears the form felds for QSO specific fiedls
		v['name'].text = ""
		v['srst'].text = ""
		v['rrst'].text = ""
		v['callsign'].text = ""
		v['qth'].text = ""
		v['country'].text = ""
		v['grid'].text = ""

		if len(self.othersummit) > 0:				# if qso was s2s, set switch off and
			self.clearothersummit.text = ""		# hide sota text box
			self.switch.value = False
			v['othersummit'].hidden = True
		v['callsign'].border_color = 'cacaca'
		v['datetime'].border_color = 'cacaca'
		
	def textout(self, output):
		hd = "Prev QSOs  \n Date 		 Time    Call   	  Name   S  R  \n "
		
		for qso in output:
			for flds in qso:
				hd += flds + "   "
			hd += '\n '
		v['textview'].text = hd
	
	def save(self, sender):  # format for SOTA csv2  and ADI and write to files
		
		# check is time should be set on save
		
		if  v['timesw'].value is True:
			self.get_timenow(sender)
			
		
		
		# each adif field if fomatted and added to the adi_list
		
		adi_list = []
		qsodate = self.timeon[0:10]
		adiqsodate = qsodate.replace('-', '')
		adiqsodate = "<QSO_DATE:" + str(len(adiqsodate)) + ">" + adiqsodate
		adi_list += adiqsodate
		
		timeon = self.timeon[11:16]
		sotatime = timeon
		aditimeon = timeon.replace(':', '')
		aditimeon = "<TIME_ON:" + str(len(aditimeon)) + ">" + aditimeon
		adi_list += aditimeon
		
		aditimeoff = aditimeon.replace('ON', 'OFF')
		adi_list += aditimeoff
		
		freq = str(self.freq)
		adifreq = "<FREQ:" + str(len(freq)) + ">" + freq
		adi_list += adifreq
		
		adiband = self.calcband(self.freq)
		adiband = "<BAND:" + str(len(adiband)) + ">" + adiband
		adi_list += adiband
		
		call = self.callsign
		adicall = "<CALL:" + str(len(call)) + ">" + call
		adi_list += adicall
		
		adirrst = self.rrst
		adirrst = "<RST_RCVD:" + str(len(adirrst)) + ">" + adirrst
		adi_list += adirrst
		
		adisrst = self.srst
		adisrst = "<RST_SENT:" + str(len(adisrst)) + ">" + adisrst
		adi_list += adisrst
		
		adiname = self.name
		adiname = "<NAME:" + str(len(adiname)) + ">" + adiname
		adi_list += adiname
		
		adiqth = self.qth
		adiqth = "<QTH:" + str(len(adiqth)) + ">" + adiqth
		adi_list += adiqth
		
		adimode = self.mode
		adimode = "<MODE:" + str(len(adimode)) + ">" + adimode
		adi_list += adimode
		
		adicomment = self.comments
		adicomment = "<COMMENT:" + str(len(adicomment)) + ">" + adicomment
		adi_list += adicomment
		
		operator = self.opcall
		adioperator = "<OPERATOR:" + str(len(operator)) + ">" + operator
		adi_list += adioperator
		
		adigrid = self.grid
		adigrid = "<GRIDSQUARE:" + str(len(adigrid)) + ">" + adigrid
		adi_list += adigrid
		
		adistate = ""
		adistate = "<STATE:" + str(len(adistate)) + ">" + adistate
		adi_list += adistate
		
		adicountry = self.country
		adicountry = "<COUNTRY:" + str(len(adicountry)) + ">" + adicountry
		adi_list += adicountry
		
		adi_list += "<eor>\n"
		
		
		# Open Files 		
		adifile = open(self.adifname, 'ta')
		sotacsv = open(self.sotafname, 'ta')
				
		# write headed to file
		if self.header is False:
			headertxt = "Logista SOTA loggging by MW0PDV "
			headertxt += str(datetime.datetime.utcnow())[0:10]
			headertxt += " ProgramID:5>PyLog<EOH> \n"
			adifile.write(headertxt)
			self.header = True
		
		# write tha adif fields to file
			
		for i in range(len(adi_list)):
			adifile.write(adi_list[i])
			
	# fotmat date string for sota csv
		sotadate = qsodate[-2:] + "/" + qsodate[-5:-3] + "/" + qsodate[-8:-6]
		
		# format the sota csv fields
		sotalist = []
		sotalist.append("v2,")
		sotalist.append(operator + ",")
		sotalist.append(self.mysummit + ",")
		sotalist.append(sotadate + ",")
		sotalist.append(sotatime + ",")
		sotalist.append(freq + "MHz" + ",")
		sotalist.append(self.mode + ",")
		sotalist.append(call + ",")
		sotalist.append(self.othersummit + ",")
		sotalist.append(self.name + ",")
		sotalist.append('\n')
		
		
		sotacsv.writelines(sotalist)
		
		# create a 2d list of previous qso's
		txout = [sotadate, sotatime, call, self.name, self.srst, self.rrst]
		self.prev_qso.insert(0,txout)
		form.textout(self.prev_qso)
		
		form.clearform()
		adifile.close()
		sotacsv.close()
		
		
# end of methods


form = logform()  # instantiate class obect form

# load graphics form
v = ui.load_view('sota_log_form')
v.present('sheet')


