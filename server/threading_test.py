from app import is_valid_manual, is_valid
import validate_email_new
import threading
import time
import os
import logging
import re
import smtplib

MX = re.compile(r'^.*\s+mail exchanger = (?P<priority>\d+) (?P<host>\S+)\s*$')

def main():
	# emails = ['jared@gmail.com', 'zoneraich@gmail.com', 'jaredzoneraich@gmail.com', 'jared.zoneraich@gmail.com', 'jzoneraich@gmail.com', 'j.zoneraich@gmail.com', 'jaredz@gmail.com', 'jared.z@gmail.com', 'jz@gmail.com', 'j.z@gmail.com', 'zoneraichjared@gmail.com', 'zoneraich.jared@gmail.com', 'zoneraichj@gmail.com', 'zoneraich.j@gmail.com', 'zjared@gmail.com', 'z.jared@gmail.com', 'zj@gmail.com', 'z.j@gmail.com', 'jszoneraich@gmail.com', 'js.zoneraich@gmail.com', 'jaredszoneraich@gmail.com', 'jared.s.zoneraich@gmail.com', 'jaredsethzoneraich@gmail.com', 'jared.seth.zoneraich@gmail.com', 'jared-zoneraich@gmail.com', 'j-zoneraich@gmail.com', 'jared-z@gmail.com', 'j-z@gmail.com', 'zoneraich-jared@gmail.com', 'zoneraich-j@gmail.com', 'z-jared@gmail.com', 'z-j@gmail.com', 'js-zoneraich@gmail.com', 'jared-s-zoneraich@gmail.com', 'jared-seth-zoneraich@gmail.com', 'jared_zoneraich@gmail.com', 'j_zoneraich@gmail.com', 'jared_z@gmail.com', 'j_z@gmail.com', 'zoneraich_jared@gmail.com', 'zoneraich_j@gmail.com', 'z_jared@gmail.com', 'z_j@gmail.com', 'js_zoneraich@gmail.com', 'jared_s_zoneraich@gmail.com', 'jared_seth_zoneraich@gmail.com']
	emails = ['jared@gmail.com', 'zoneraich@gmail.com', 'jaredzoneraich@gmail.com']

	# print validate_email_new.validate_email("jszonearaich@gmail.com")
	amount = len(emails)

	results_list = ["Jared"] * amount
	for i in range(0,amount):
		try:
			threading.Thread(target=is_valid_manual, args=(emails[i], results_list, i)).start()
		except Exception, errtxt:
			print errtxt
	
	while threading.active_count() > 1:
		print threading.active_count()
		continue

	# time.sleep(5)

	print results_list

if __name__ == "__main__":
	main()