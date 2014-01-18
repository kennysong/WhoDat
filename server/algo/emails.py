from domains import get_domains
from name_permut import helperFunction

def main():
  #name = 'Scott Weiss'
  #name = 'Ron Amadeo'
  name = 'Michael Sippey'
  #url = 'http://scott.a16z.com/2014/01/17/success-at-work-failure-at-home/'
  #url = 'http://arstechnica.com/security/2014/01/malware-vendors-buy-chrome-extensions-to-send-adware-filled-updates/?'
  url = 'http://techcrunch.com/2014/01/17/michael-sippey-leaving-twitter/'

  print(get_emails(name, url))


def get_emails(name, url):
  emails = []

  usernames = helperFunction(name)
  print('Usernames: ' + str(usernames))

  domains = get_domains(name, url)
  print('Domains: ' + str(domains))

  for domain in domains:
    email = 'me@' + domain
    emails.append(email)
  

  for domain in domains:
    for username in usernames:
      email = username + '@' + domain
      emails.append(email)

  return emails


if __name__ == '__main__':
  main()
