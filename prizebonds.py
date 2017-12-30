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
import datetime

def validate_date(s):
	try:
		s = s.split('-')
		year = s[0]
		month = s[1]
		day = s[2]
		dt = datetime.datetime(int(year), int(month), int(day))
		dt = dt.strftime("%Y-%m-%d")
	except ValueError:
		msg = "Not a valid date: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)

	return dt

base_url = 'http://saving.com.pk/'
parser = argparse.ArgumentParser()
# parser.add_argument("--url", help="Url for the draw containing serial numbers", required=True)
parser.add_argument("--amount", help="Amount of the Prize Bond you wish to search", required=True)
parser.add_argument("--date", help="Date of the draw. The format is YYYY-MM-DD", type=validate_date, required=True)
parser.add_argument("--filepath", help="File Path Containing Serial Numbers of your Prize Bonds.", required=True)

args = parser.parse_args()

# Might change depending on the bonds, so update accordingly.
SERIAL_NUMBERS_LENGTH = 6

def main():

	print "-------------------Processing: Processing List of Prize Bonds ---------------------"
	try:
		path = os.getcwd() + '/' + args.filepath
		file = open(path, 'r')
		user_serial_numbers = []

		# Using readlines might not give line to line validation here so not using that.
		for line in file:
			line = line.rstrip()
			if not isinstance(line, str) or len(line) != SERIAL_NUMBERS_LENGTH:
				print "------------Error: Invalid entry in serial numbers: Aborting!--------------"
				sys.exit()

			user_serial_numbers.append(line)
	except:
		print "-----------------------Error: Invalid file path or file provided: Bailing out!--------------"
		sys.exit()


	final_url = 'http://saving.com.pk/{amount}/{date}'.format(amount=args.amount, date=args.date)
	print "-------------------Processing: Parsing prize bonds list from provided url %s" % final_url

	html_content = ''
	try:
		# No need to check for responses other than <200>, These guys are too generous to open any link without a 404 :D
		response = requests.get(final_url)
		html_content = response.content
	except:
		print "-------------Error: Invalid data received from provided url: Bailing Out!-----------"
		sys.exit()

	soup = BeautifulSoup(html_content, 'html.parser')


	print "----------------------Processing: Looking for the big prizes first!-----------------"
	try:
		first_prize = (soup.findAll('strong')[6].p.get_text())
		second_prizes = soup.findAll('strong')[7].p.get_text().replace(u'\xa0','').rstrip().split()
		
		import pdb
		pdb.set_trace()
		if first_prize in user_serial_numbers:
			print "Un Real dude!"
		elif set(second_prizes).intersection(set(user_serial_numbers)):
			print "You won the second prize!!!!"
	except:
		print "------------------Bad parsing of the html... Bailing out!-----------------"

	list_numbers = []
	try:
		all_serial_numbers =  soup.article.div.div.find_all('div')[-2].find_all('span')
		if not all_serial_numbers:
			print "-------------------Error: No Data on Link Provided----------------"
			sys.exit()
		for sno in all_serial_numbers:
			list_numbers.append(str(sno.text).strip())

	except:
		print "-------------------Error: Failed to parse data from website: Bailing out!------------"
		sys.exit()

	list_numbers = sorted(list_numbers)

	print "-------------------------Processing: Now Comes the good part!------------------\n ------------Searching for your serial numbers in the list----------"

	draw = set(list_numbers).intersection(set(user_serial_numbers))

	if not draw:
		print "-------------------------Error: Sorry no luck :( ----------------------------------"
		print "--------------------------------Exiting---------------------------------"
		sys.exit()


	print "-----------Processing: What!!!!!!!!!-- You Actually won something bro!---------"
	print "---- Processing: Here is the list of numbers you won %s" % draw


# Entry point
if __name__ == '__main__':
	main()