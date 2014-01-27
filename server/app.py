import os
import jinja2
from flask import Flask, render_template, redirect, request, jsonify
import smtplib
import sendgrid
from flask import current_app
from algo.emails import get_possible_emails
from algo.find_domain import has_results
import threading
import datetime as dt
import requests
import email_checking

app = Flask(__name__)
app.config.update(
	DEBUG = True,
)

@app.route('/sendgrid', methods=['POST'])
def sendgrid_page():
	if request.method == 'POST':
		to = request.form['to']
		frm = request.form['from']
		text = request.form['message']

		# make a secure connection to SendGrid
		s = sendgrid.Sendgrid('WhoDat', 'MailScopeSucks', secure=True)

		# make a message object
		message = sendgrid.Message(frm, "Hello!", text)
		# add a recipient
		message.add_to(to)

		# use the Web API to send your message
		s.web.send(message)

@app.route('/test')
def test():
	# GET: 
	# 	{
	# 		url : http://google.com,
	#	 	name : Jared Zoneraich,
	# 		email : jared@getwhodat.com
	# 	}

	# get arguments
	url = request.args.get('url')
	name = request.args.get('name')
	if ' ' not in name:
		return str({'error' : 'Only one word provided'})
	
	# Get email permutations
	emails = get_possible_emails(name, url)
	amount = len(emails)
	if amount == 0:
		return "No possible emails"
	
	# verify emails exist
	results_list = [None] * amount
	for i in range(0,amount):
		try:
			threading.Thread(target=email_checking.is_valid, args=(emails[i], results_list, i)).start()
		except Exception, errtxt:
			print errtxt
	
	# Threading
	last = threading.active_count() 
	started = dt.datetime.now()
	delta = dt.timedelta(seconds=25)
	while threading.active_count() > 1:
		if threading.active_count() != last:
			started = dt.datetime.now()
			last = threading.active_count()
			print last
		if dt.datetime.now() - started >= delta:
			print 'manual timeout'
			break
	
	# When all threads finish or timeout
	valid_emails = []
	for i in range(0,amount):
		if (results_list[i]) or (results_list[i] is None and has_results(emails[i])):
			valid_emails.append(emails[i])
	
	# Send email to user with results b/c request probably timed out
	to =  request.args.get('email')
	print to
	frm = "us@getwhodat.com"
	text = ""
	for em in valid_emails:
		text += em + ", "

	s = sendgrid.Sendgrid('WhoDat', 'MailScopeSucks', secure=True)
	message = sendgrid.Message(frm, name + "'s email", text)
	message.add_to(to)
	s.web.send(message)

	# If request did not time out, return results
	return str({'emails':valid_emails})

@app.route('/', methods=['GET','POST'])
def home_page():
	# get: {
	# 	name: "Bob Smith",
	# 	url: "http://google.com"
	# }
	print request.method
	if request.method == 'POST':
		#name = request.form['name']
		# validate_email(email,check_mx=True,verify=True)
		# https://github.com/mailgun/flanker
		#valid = email_checking.is_valid(name.replace(' ','.') + "@gmail.com")
		#message = {-1 : "Unable to verify email", 0 : "Invalid email", 1 : "Valid Email"}
		# return message[valid]
		#return jsonify(email=name.replace(' ','.')+"@gmail.com",message=message[valid])

		name = request.form['name']
		if ' ' not in name:
			return str({'error' : 'Only one word provided'})
		url = request.form['url']
		print name
		print url
		emails = get_possible_emails(name, url)
                print("emails: " + str(emails))
		# print('Emails: ' + str(emails))
		# online_users = mongo.db.users.find({'name': name, 'tags' : alchemy_tags})
		#valid = email_checking.is_valid(name.replace(' ','.') + "@fivehour.com")
		amount = len(emails)
		results_list = ["_"] * amount
		for i in range(0,amount):
			try:
				threading.Thread(target=email_checking.is_valid, args=(emails[i], results_list, i)).start()
			except Exception, errtxt:
				print errtxt
		
		last = threading.active_count() 
		started = dt.datetime.now()
		delta = dt.timedelta(seconds=25)
		while threading.active_count() > 1:
			if threading.active_count() != last:
				started = dt.datetime.now()
				last = threading.active_count()
				print last
			if dt.datetime.now() - started >= delta:
				print 'manual timeout'
				break
			continue
		
		valid_emails = []
		for i in range(0,amount):
			if (results_list[i]) or (results_list[i] is None and has_results(emails[i])):
				valid_emails.append(emails[i])
		return str({'emails':valid_emails})
	else:
		return render_template('index.html')

if __name__ == '__main__':
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port,debug=True)
