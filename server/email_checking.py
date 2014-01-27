from validate_email import validate_email
import os
import smtplib

def is_valid_auto(email):
	return validate_email(email,check_mx=True,verify=True)

def is_valid_helper(email):
	"""Returns:
		None  --- Cannot verify
		False --- Invalid Email
		True  --- Valid Email
	"""

	if email == 'me@twitter.com' or email == 'me@gmail.com':
		return False
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

	try:
		s = smtplib.SMTP(mailserver)
		rep1 = s.ehlo()
		if rep1[0]==250 : #250 denotes OK reply
			rep2 = s.mail("test@rediff.com")
			if rep2[0] == 250:
				rep3 = s.rcpt(email)
				if rep3[0] == 250:
					if email == ("ednvoebgtfeb@" + maildomain) or is_valid_helper("ednvoebgtfeb@" + maildomain):
						return None
					else:
						return True
				elif rep3[0] == 550: #email invalid
					return False
		return False
	except smtplib.SMTPServerDisconnected:  # Server not permits verify user
		return None
	except smtplib.SMTPConnectError:
		return None
	except Exception, err:
		print err
		return None

def is_valid(email, results_list, index):
	try:
		results_list[index] = is_valid_helper(email)
	except Exception, e:
		print e