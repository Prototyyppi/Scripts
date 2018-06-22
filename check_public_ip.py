import json
import sys
import smtplib # For sending email
from urllib2 import urlopen
from time import sleep


def show_help():
	print("~~~~~~~~~~~HELP~~~~~~~~~~~")
	print("1. Argument gmail username")
	print("2. Argument gmail password")
	print("3. Target email address")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~")

def get_email_values():
	# my_gmail, my_gmail_passwd, target_email
	email_values = (sys.argv[1], sys.argv[2], sys.argv[3])
	return email_values

def get_value():
	filehandle = urlopen('https://api.ipify.org?format=json')
	data = json.load(filehandle)
	print(data)
	return data["ip"]

def send_message(ip_addr, email_values):
	# To be implemented...
	server = smtplib.SMTP('smtp.gmail.com', 587) # init server
	server.login(email_values[0], email_values[1])
	message = "IP change detected. New ip is " + ip_addr
	server.sendmail(email_values[0]+"@gmail.com", email_values[2], message)
	server.quit()

''' Check mail sending capability '''
if len(sys.argv) < 4:
	show_help()
	sys.exit()

''' Get email values '''
email_values = get_email_values()

''' Initialize ip '''
ip = get_value()

''' Start infinite loop '''
while True:
	current_ip = get_value()
	if ip != current_ip:
		ip = current_ip
		print("IP change detected")
		send_message(ip, email_values)
	sleep(30)
