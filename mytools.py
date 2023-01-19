from __future__ import absolute_import, division, print_function

from getpass import getpass


def get_credentials():

	try:
		f =open("credentials.txt","r")
	
		Username =f.readline().strip()
		Password =f.readline().strip()	
		if not Password :Password = getpass("Enter user '%s' password: " % Username)
		f.close()
	except Exception as e:
		print(e,"credentials file not found!!!")
		exit()
	return Username , Password

def get_input(prompt=''):
	try:
		line = raw_input(prompt)
	except NameError:
		line = input(prompt)
	return line

