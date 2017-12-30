"""
Author: Wajih Siddiqui
Email: wajihsid@gmail.com
Created On: 30/12/2017
"""
from bs4 import BeautifulSoup
import requests
import sys
import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--url", help="Url for the draw containing serial numbers")
parser.add_argument("--filepath", help="File Path Containing Serial Numbers of your Prize Bonds.")
args = parser.parse_args()

# Might change depending on the bonds, so update accordingly.
SERIAL_NUMBERS_LENGTH = 6

def main():
	if not args.url:
	    print "---------------Please enter url to continue.-----------------------"
	    sys.exit()

	if not args.filepath:
		print "----Error: Please Enter the file path containing serials numbers ----"
		sys.exit()

	print "-------------------Processing List of Prize Bonds ---------------------"
	try:
		path = os.getcwd() + '/' + args.filepath
		file = open(path, 'r')
		user_serial_numbers = []

		# Using readlines might not give line to line validation here so not using that.
		for line in file:
			line = line.rstrip()
			if not isinstance(line, str) or len(line) != SERIAL_NUMBERS_LENGTH:
				print "------------Invalid entry in serial numbers: Aborting!--------------"
				sys.exit()

			user_serial_numbers.append(line)
	except:
		print "-----------------------Invalid file path or file provided: Bailing out!--------------"
		sys.exit()


	print "-------------------Parsing prize bonds list from provided url----------"

	html_content = ''
	try:
		response = requests.get(args.url)
		html_content = response.content
	except:
		print "-------------Invalid data received from provided url: Bailing Out!-----------"
		sys.exit()

	soup = BeautifulSoup(html_content, 'html.parser')

	list_numbers = []
	try:
		all_serial_numbers =  soup.article.div.div.find_all('div')[-2].find_all('span')
		for sno in all_serial_numbers:
			list_numbers.append(str(sno.text).strip())

	except:
		print "-------------------Failed to parse data from website: Bailing out!------------"


	print "-------------------------Now Comes the good part!------------------\n ------------Searching for your serial numbers in the list----------"

	draw = []

	for serial in user_serial_numbers:
		if serial in list_numbers:
			draw.append(serial)

	if not draw:
		print "-------------------------Sorry no luck :( ----------------------------------"
		print "--------------------------------Exiting---------------------------------"
		sys.exit()


	print "-----------What!!!!!!!!!-- You Actually won something bro!---------"
	print "---- Here is the list of numbers you won %s" % draw


# Entry point
if __name__ == '__main__':
	main()