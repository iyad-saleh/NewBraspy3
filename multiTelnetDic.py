import telnetlib ,string
import threading
import re
from time import sleep 
import signal 
from datetime import datetime
from mytools import get_credentials 


signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C

READ_TIMEOUT = 5
TELNET_PORT = 23

pattern= re.compile(r"([a-f0-9A-F]{4}-[a-f0-9A-F]{4}-[a-f0-9A-F]{4})")
pattern1=re.compile(r"Info: No online user!")
#def autoTelnet(host,Username,Password,target):
def autoTelnet(Username , Password, target, cmd_level, host,result):
	try:
		result["HOST"]=host
		# print ('-- Connecting .....' + host+"\r\n")
		telnet = telnetlib.Telnet(host, TELNET_PORT, READ_TIMEOUT)
		telnet.read_until(b"Username:")
		send_cmd(telnet ,Username)
		telnet.read_until(b"Password:")
		send_cmd(telnet ,Password)
		sleep(1)
		bras = get_host_name(telnet)
		
		result["bras"]=bras
		send_cmd(telnet ,'screen-length 0 temporary')
		sleep(0.5)
		send_cmd(telnet ,'sys')
		sleep(1)
		# print("1")
		telnet.read_very_eager()
		if str(cmd_level) == "1":# search by User account 
			send_cmd(telnet ,'display access-user username '+ target) # uncomment anas@tarassul.sy   *************
			# send_cmd(telnet ,'display access-user ip-address 192.168.0.2') # comment this line in real world   **********
			sleep(2)
			# send_cmd(telnet ,'disp mac-address') # comment this line in real world   **********
			# sleep(3)
			output =telnet.read_very_eager().decode('ascii') 
			if re.search("No online user",output):
				# print ("<"+bras+'>  '+ ' this User '+ target + " Not online   <<< !!"+'\r\n')
				send_cmd(telnet ,' quit')
				send_cmd(telnet ,' quit')
				result["UserNotOnline"]="No online user"
			elif re.search(pattern,output):	
				target = re.search(pattern,output).group(1)
				result["MAC"]=target
				cmd_level=2
			else:
				print(bras,"ERROR no pattern found!!")
		# print("2")			
		if str(cmd_level) == "2":# search mac
			send_cmd(telnet ,'display access-user mac-address '+target)
			# for tt in range(3):# you can decrement this value 
			# 	
			# 	send_cmd(telnet ,'\x20')
			# 	send_cmd(telnet ,'\r\n')
			sleep(2)
			output2 = telnet.read_very_eager().decode('ascii')
			#for line in iter(output2.split('\r\n')):
			if not re.search(pattern1,output2):
				result["Final_output"]=output2
			else :
				result["MacNotOnline"]="This MAC NOT Online"
			
			send_cmd(telnet ,' quit')
			send_cmd(telnet ,' quit')
			
		telnet.close()	
	except Exception as excp:
		# print(host,str(excp))
		result["Fault"]=excp
	# print(result)	
	return result	

def send_cmd(telnet ,command):
	telnet.write(command.encode('ascii')+"\r\n".encode('ascii'))


def get_host_name(telnet):
	host=""
	out=telnet.read_until(b">").decode('ascii')
	for line in iter(out.split('\n')):
		g=re.findall('<?(.*)>',line)
	for item in g :	
		host= item	
	return host	


def create_threads(Username , Password, target, cmd_level, ipBras):
	result=[{} for x in range(len(ipBras))]
	threads = []
	for i,host in enumerate(ipBras):

		th = threading.Thread(target = autoTelnet ,args = (Username , Password, target, cmd_level, host,result[i]))
		th.start()
		threads.append(th)
	for thr in threads:
		thr.join()

	return 	result
 
if __name__ == "__main__":
	print('~'*50)
	print(" Welcome to Multi and Smart search MyName Iyad saleh !!")
	Username , Password = get_credentials()
	ipBras=[]
	with open('Router.txt','r') as ipfile:
		for  line in ipfile:
			line=line.strip()	
			ipBras.append(line)

	while True:
		
		result=[]
		target = input("Input your Target User Or MAC ADDRESS \n!!ctrl ^ c to break !! :  ")
		print("#"*50)
		print("#"*20,target,"#"*20)
		print("#"*50)
		if   re.search(pattern,target):
			cmd_level=2#serach for mac 
		else :
			cmd_level=1	# search for user account 		
		result=create_threads(Username , Password, target, cmd_level, ipBras)
		for item in result:
			print("#"*50)		
			
			if "bras" in item:
				print(item["bras"],item["HOST"])
			else:
				print(item["HOST"])
			if "Fault" in item:
				print(item["Fault"])
			if "UserNotOnline" in item:
				print(item["UserNotOnline"])
			if "Final_output" in item:
				print(item["Final_output"])	
			if "MacNotOnline" in item:
				print(item["MacNotOnline"])

		repet=input("Do You Want To Repeat This Program!!Press any key to continue or  'q' to exit\n")
		if  repet.lower() == 'q':
			break
			exit()			
	print('*'*50)
	print ("         Exiting the program Thank you !!")
	print('*'*50)


	#civilhaj

	#00c0-8917-559b