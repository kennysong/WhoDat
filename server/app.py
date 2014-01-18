import os
import jinja2
from flask import Flask, render_template, redirect, request, jsonify
from flask.ext.pymongo import PyMongo
from validate_email_new import validate_email
import smtplib
from flask import current_app
from algo.emails import get_emails

app = Flask(__name__)
app.config.update(
	DEBUG = True,
)
# mongo = PyMongo(app)

def is_valid(email):
	return validate_email(email,check_mx=True,verify=True)

def is_valid_manual(email):
	"""Returns:
		None  --- Cannot verify
		False --- Invalid Email
		True  --- Valid Email
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
		return False
	minimum = min(mailservers.keys())
	mailserver = mailservers[minimum]

	s = smtplib.SMTP(mailserver)
	rep1 = s.ehlo()
	if rep1[0]==250 : #250 denotes OK reply
		rep2 = s.mail("test@rediff.com")
		if rep2[0] == 250:
			rep3 = s.rcpt(email)
			if rep3[0] == 250:
				if validate_email("ednvoebgtfeb@" + maildomain,check_mx=True,verify=True):
					return None
				else:
					return True
			elif rep3[0] == 550: #email invalid
				return False
	return False

@app.route('/', methods=['GET','POST'])
def home_page():
	# get: {
	# 	name: "Bob Smith",
	# 	url: "http://google.com"
	# }
	if request.method == 'POST':
		#name = request.form['name']
		# validate_email(email,check_mx=True,verify=True)
		# https://github.com/mailgun/flanker
		#valid = is_valid_manual(name.replace(' ','.') + "@gmail.com")
		#message = {-1 : "Unable to verify email", 0 : "Invalid email", 1 : "Valid Email"}
		# return message[valid]
		#return jsonify(email=name.replace(' ','.')+"@gmail.com",message=message[valid])

		name = request.form['name']
                url = request.form['url']
                emails = get_emails(name, url)
                print('Emails: ' + str(emails))
		# online_users = mongo.db.users.find({'name': name, 'tags' : alchemy_tags})
		#valid = is_valid_manual(name.replace(' ','.') + "@fivehour.com")
                valid_emails = []
                for email in emails:
                  x = is_valid_manual(email)
                  print(email + '::' + str(x))
                  if x or x is None:
                    valid_emails.append(email)
                                    
		#message = {-1 : "Unable to verify email", 0 : "Invalid email", 1 : "Valid Email"}
		# return message[valid]
		#return jsonify(emails=valid_emails, message=message[valid])
		return {'emails':valid_emails}
	else:
		return render_template('index.html')

if __name__ == '__main__':
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port,debug=True)
