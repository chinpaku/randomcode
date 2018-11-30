import subprocess
import sys
import getopt
import os
from ftplib import FTP

username = ""
smbshare = ""
command = ""

def usage():
	print "Python Recon Tool"
	print "Usage :"
	print "htbrecon -t target-host"
	sys.exit(0)

def nmap():
	global target
	global nmapfile
	#nmapfile = 'nmap-'+target+'.txt'
	abspath = os.path.abspath(nmapfile)

	if os.path.exists(abspath):
		print "nmap already done on the host"	
		f = open(abspath,'r')
		file_content = f.read()
		print file_content
	else:
		out = subprocess.call(['nmap','-sV','-vv','-oN',nmapfile, target])
		print out
	checkNmapResultsAndAttack()
	

def  checkNmapResultsAndAttack():
	global nmapfile
	#print nmapfile
	#print "file" + os.path.abspath(nmapfile)
	outport80 = subprocess.call(['grep','80/tcp',os.path.abspath(nmapfile)])
	outport445 = subprocess.call(['grep','445/tcp',os.path.abspath(nmapfile)])
	outport21 = subprocess.call(['grep','21/tcp',os.path.abspath(nmapfile)])
	outport139 = subprocess.call(['grep','139/tcp',os.path.abspath(nmapfile)])
	outport443 = subprocess.call(['grep','443/tcp',os.path.abspath(nmapfile)])
	if not outport80 > 0:
		print "found port 80 - Web"
		webAttack()
		#probeport80()
	if not outport445 >0:
		print "found port 445 - SMB"
		probesmb()

	print "testing FTP"

	if not outport21 >0:
		print "found port 21 - FTP"
		probeftp()
	if not  outport139 > 0:
		print "found port 139 - Linux SMB"
		probesmb()
	if not outport443 >0:
		print "found port 443 - Web"
		probeport443()
	sys.exit(0)


def probeport443():
	global target
	print "Runnig gobuster ----"
	try:
		dirb = subprocess.call(['gobuster','-w', '/usr/share/wordlists/dirb/common.txt','-o','gobuster-'+target+'.txt','-u', 'https://'+target])
		print dirb
	except:
		print "Error runnig gobuster...."


	print "Running Nikto ---"
	nik = subprocess.call(['nikto','-o','nikto-'+target+'.txt','-h',target])
	#sys.exit(0)

def webAttack():
	global target
	gobusterfile = 'gobuster-'+target+'.txt'
	niktofile = 'nikto-'+target+'.txt'
	dirbfile = 'dirb-'+target+'.txt'
	wgetresponsefile = 'wget'+target+'.txt'

	tmp=1
	while tmp>0:
		print "------Web Attack ----"
		print "1 : gobuster"
		print "2 : Nikto"
		print "3 : dirb"
		print "4 : wget and print response"
		print "0 : Exit"
		inp = int(input("Please select an option"))
		print inp
		if inp==1:
			try:
				gobusterabspath = os.path.abspath(gobusterfile)
				if os.path.exists(gobusterabspath):
					inpfile = raw_input("gobuster scan fie exists, do you want to run scan again and overwrite file? y/n ")
					if inpfile=="y":
						print "Runnig gobuster ----"
						dirb = subprocess.call(['gobuster','-w', '/usr/share/wordlists/dirb/common.txt','-o','gobuster-'+target+'.txt','-u', 'https://'+target])
						print dirb
					elif inpfile=="n":
						print "showing gobuster scan results"
						f = open(gobusterabspath,'r')
						file_content = f.read()
						print file_content
						#sys.exit(1)
					else:
						print "wrong input"
				else:
					print "Runnig gobuster ----"
					dirb = subprocess.call(['gobuster','-w', '/usr/share/wordlists/dirb/common.txt','-o','gobuster-'+target+'.txt','-u', 'http://'+target])
					print dirb
			except Exception as e:
				print "Error runnig gobuster...." + str(e)
		elif inp==2:
			try:
				niktoabspath = os.path.abspath(niktofile)
				if os.path.exists(niktoabspath):
					inpfile = raw_input("Nikto scan fie exists, do you want to run scan again and overwrite file? y/n ")
					if inpfile=="y":
						print "Running Nikto ---"
						nik = subprocess.call(['nikto','-o','nikto-'+target+'.txt','-h',target])
						print nik
					elif inpfile=="n":
						print "showing Nikto scan results"
						f = open(niktoabspath,'r')
						file_content = f.read()
						print file_content
						#sys.exit(1)
					else:
						print "wrong input"
				else:
					print "Running Nikto ---"
					nik = subprocess.call(['nikto','-o','nikto-'+target+'.txt','-h',target])
					print nik

			except Exception as e:
				print "error runing nikto - " + str(e)

		elif inp==4:
			print "Running wget http://"+target
			wgt = subprocess.call(['wget','-O',wgetresponsefile,'http://',target])
			wgetoabspath = os.path.abspath(wgetresponsefile)
			if os.path.exists(wgetoabspath):
				f = open(wgetoabspath,'r')
				file_content = f.read()
				print file_content
	
		elif inp==0:
			tmp=0
		else:
			print "select correct option"



def InitialProbe():
	global target
	global nmapfile

	ini=1
	while ini>0:
		print "------Available options ----"
		print "1 : run nmap basic: nmap -sV -vv -oN <host>"
		print "2 : run nmap all comprehensive : nmap -p- -T4 -A -vv <host>"
		print "3 : show nmap results"
		print "4 : check nmap results and probe ports"
		print "0 : Exit"
		inp = int(input("Please select an option : "))
	
		if inp==1:
			print "Runnig nmap basic : nmap -sV -vv -oN <host>"
			try:
				abspath = os.path.abspath(nmapfile)

				if os.path.exists(abspath):
					print "nmap already done on the host"
					inpfile = raw_input("run nmap again and overrite file? y/n ")
					if inpfile=="y":
						out = subprocess.call(['nmap','-sV','-vv','-oN',nmapfile, target])
						print out
					elif inpfile=="n":
						print "going back to main menu"
						#sys.exit(1)
					else:
						print "wrong input"
					f = open(abspath,'r')
					file_content = f.read()
					print file_content
				else:
					out = subprocess.call(['nmap','-sV','-vv','-oN',nmapfile, target])
					print out
				#checkNmapResultsAndAttack()
			except Exception as e:
				print "Error runnig nmap comprehensive...."+str(e)
		elif inp==2:
			print "Running nmap comprehensive : nmap -p- -T4 -A -vv <host>"
			try:
				abspath = os.path.abspath(nmapfile)

				if os.path.exists(abspath):
					print "nmap already done on the host"
					inpfile = raw_input("run nmap again and overrite file? y/n ")
					if inpfile=="y":
						out = subprocess.call(['nmap','-p-','-vv','-T4','-A','-oN',nmapfile, target])
						print out
					elif inpfile=="n":
						print "going back to main menu"
						#sys.exit(1)
					else:
						print "wrong input"
				else:
					out = subprocess.call(['nmap','-p-','-vv','-T4','-A','-oN',nmapfile, target])
					print out
				#checkNmapResultsAndAttack()
			except Exception as e:
				print "Error runnig nmap comprehensive...."+str(e)
		elif inp==3:
			try:
				abspath = os.path.abspath(nmapfile)

				if os.path.exists(abspath):
					print "opening nmap scan fie"
					f = open(abspath,'r')
					file_content = f.read()
					print file_content
				else:
					print "nmap scan file does not exists"
				#checkNmapResultsAndAttack()	
			except:
				print "Error runnig nmap comprehensive...."
		elif inp==4:
			checkNmapResultsAndAttack()
		elif inp==0:
			ini=0


def probeport80():
	global target
	gobusterfile = 'gobuster-'+target+'.txt'
	niktofile = 'nikto-'+target+'.txt'

	gobusterabspath = os.path.abspath(gobusterfile)

	if os.path.exists(gobusterabspath):
		print "gobuster fie exists for host"	
		f = open(gobusterabspath,'r')
		file_content = f.read()
		print file_content
	else:
		print "Runnig gobuster ----"
		dirb = subprocess.call(['gobuster','-w', '/usr/share/wordlists/dirb/common.txt','-o',gobusterfile,'-u', target])
		print dirb

	niktoabspath = os.path.abspath(niktofile)

	if os.path.exists(niktoabspath):
		print "Nikto already exists for host"	
		f = open(niktoabspath,'r')
		file_content = f.read()
		print file_content
	else:
		print "Running Nikto ---"
		nik = subprocess.call(['nikto','-o',niktofile,'-h',target])	

	
	#sys.exit(0)

def probesmb():
	global target
	global username
	global password
	global smbshare
	global command


	if len(smbshare) and not len(username) and len(command):
		sbclient = subprocess.call(['smbclient','//'+target+'/'+smbshare,'-N','-c',command])


	if len(username):
		smbmap = subprocess.call(['smbmap','-H',target,'-u',username])
		sbclient = subprocess.call(['smbclient','//'+target+'/'+smbshare,'-U',username+'%'+password,'-c',command])
	else:
		smbmap = subprocess.check_output(['smbmap','-H',target])
		print smbmap
		filesmbmap = open('smbmap'+target+'.txt','w')
		filesmbmap.write(smbmap)
		filesmbmap.close()
		
		smbclient = subprocess.check_output(['smbclient','-L','//'+target,'-N'])
		print smbclient
		filesmbclient = open('smbclient'+target+'.txt','w')
                filesmbclient.write(smbclient)
                filesmbclient.close()

	#sys.exit(0)

def probeftp():
	global target

	print('starting ftp check - using anonymous login')
	ftp = FTP(target,'anonymous','anonymous@test.com')
	print ftp
	#ftp.login()
	files = ftp.dir()#print dir listing
	print files
	#sys.exit(0)


def main():
	global target
	global nmapfile
	global username
	global password
	global smbshare
	global command
	
	if not len(sys.argv[1:]):
		usage()

	try:
		opts, args = getopt.getopt(sys.argv[1:],"h:t:u:p:s:x:",["help","target","username","pasword","share","command"])
	except getopt.GetoptError as err:
		print str(err)
		usage()


	for o,a in opts:
		if o in ("-h","--help"):
			usage()
		elif o in ("-t","--target"):
			target = a
			#print "starting scan on " + target 
			#nmapfile = 'nmap-' + target + '.txt'
			#nmap()
			#sys.exit(0)
		elif o in ("-u","--username"):
			#print "setting username"
			username = a
			#print username
			#print "searching nmap results for next attack vectors/ports"
                        #checkNmapResultsAndAttack()
		elif o in ("-p","--pasword"):
			password = a
		elif o in ("-s","--share"):
			smbshare = a
		elif o in ("-x","comand"):
			command = a
		else:
			assert False,"Unhandled Option"
			#sys.exit(0)

	if len(target):
		#print "starting scan on " + target 
		print "Initial screen" 
		
		nmapfile = 'nmap-' + target + '.txt'
		InitialProbe()
		#nmap()
		#print "setting username"
               # username = a
                #print username
                #print "searching nmap results for next attack vectors/ports"
		#checkNmapResultsAndAttack()



main()
