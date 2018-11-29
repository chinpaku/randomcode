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
		probeport80()
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
		print "starting scan on " + target 
		nmapfile = 'nmap-' + target + '.txt'
		nmap()
		#print "setting username"
               # username = a
                #print username
                print "searching nmap results for next attack vectors/ports"
		checkNmapResultsAndAttack()



main()
