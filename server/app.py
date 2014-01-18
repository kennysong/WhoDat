import os
import jinja2
from flask import Flask, render_template, redirect, request, jsonify
from flask.ext.pymongo import PyMongo
from validate_email import validate_email
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
		return is_valid(name.replace(' ','.')+"@gmail.com")
		return jsonify(email=name.replace(' ','.')+"@gmail.com")
	else:
		return "Who Dat? - GET"

if __name__ == '__main__':
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port,debug=True)