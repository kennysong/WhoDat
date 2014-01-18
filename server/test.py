import os
import smtplib
from validate_email import validate_email

def is_valid_manual(email):
    maildomain = email.split("@")[1]
    nsToken = "mail exchanger = "
    mailservers = {}
    # print ("Checking for MX Mailservers...")
    plines = os.popen("nslookup -type=MX "+maildomain).readlines()
    for pline in plines:
        if nsToken in pline:
            x = (pline.split(nsToken)[1].strip()).split(' ')
            try:
                number = int(x[0])
            except:
                continue
            x.remove(x[0])
            x = "".join(x)
            mailservers[number] = x

    if len(mailservers.keys()) == 0:
        # print ("Unable to get MX address for", mailservers)
        return 1
    minimum = min(mailservers.keys())
    mailserver = mailservers[minimum]

    # print ("Found mailserver MX:", mailserver)
    # import pdb; pdb.set_trace()

    # print ("Checking email address:",email)

    s = smtplib.SMTP(mailserver)
    rep1= s.ehlo()
    if rep1[0]==250 : #250 denotes OK reply
        rep2=s.mail("test@rediff.com")
        if rep2[0] == 250:
            rep3 = s.rcpt(email)
            if rep3[0] == 250:
                if validate_email(email,check_mx=True,verify=True):
                    # print (email," is valid")
                else:
                    return 1
            elif rep3[0] == 550: #email invalid
                # print "hi5"
                return 1
    return .5

def main():
    # print is_valid_manual('js1zoneraich@fivehour.com')

if __name__ == '__main__':
    main()