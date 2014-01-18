import os
import jinja2
from flask import Flask, render_template, redirect, request, jsonify
from flask.ext.pymongo import PyMongo
from validate_email import validate_email
import smtplib
from flask import current_app
# from flanker.addresslib import address

app = Flask(__name__)
app.config.update(
	DEBUG = True,
)

def is_valid(email):
	# parsed_email = address.validate_address(email)
	# if (parsed_email is None):
	# 	return False
	# return True
	return validate_email(email,check_mx=True,verify=True)

def is_valid_manual(email):
	"""Returns:
		-1 --- Cannot verify
		0  --- Invalid Email
		1  --- Valid Email
	"""

	maildomain = email.split("@")[1]
	nsToken = "mail exchanger = "
	mailservers = {}
	plines = os.popen("nslookup -type=MX "+maildomain).readlines()
	for pline in plines:
		if nsToken in pline:
			x = (pline.split(nsToken)[1].strip()).split(' ')
			number = None
			try:
				number = int(x[0])
			except:
				continue
			x.remove(x[0])
			x = "".join(x)
			mailservers[number] = x

	if len(mailservers.keys()) == 0:
		return 1
	minimum = min(mailservers.keys())
	mailserver = mailservers[minimum]

	s = smtplib.SMTP(mailserver)
	rep1= s.ehlo()
	if rep1[0]==250 : #250 denotes OK reply
		rep2=s.mail("test@rediff.com")
		if rep2[0] == 250:
			rep3 = s.rcpt(email)
			if rep3[0] == 250:
				if validate_email(email,check_mx=True,verify=True):
					return 0
				else:
					return 1
			elif rep3[0] == 550: #email invalid
				return 1
	return .5

@app.route('/', methods=['GET','POST'])
def home_page():
	# online_users = mongo.db.users.find({'': True})
	# get: {
	# 	name: "Bob Smith",
	# 	url: "http://google.com"
	# }
	if request.method == 'POST':
		name = request.form['name']
		# validate_email(email,check_mx=True,verify=True)
		# https://github.com/mailgun/flanker
		valid = is_valid_manual(name.replace(' ','.') + "@gmail.com")
		message = {-1 : "Unable to verify email", 0 : "Invalid email", 1 : "Valid Email"}
		# return message[valid]
		return jsonify(email=name.replace(' ','.')+"@gmail.com",message=message[valid])
	else:
		return render_template('index.html')

if __name__ == '__main__':
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port,debug=True)