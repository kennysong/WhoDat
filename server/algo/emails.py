from domains import get_domains
from names import get_names

def main():
  
def get_emails(name, url):
  #name = 'Scott Weiss'
  #name = 'Ron Amadeo'
  name = 'Michael Sippey'
  #url = 'http://scott.a16z.com/2014/01/17/success-at-work-failure-at-home/'
  #url = 'http://arstechnica.com/security/2014/01/malware-vendors-buy-chrome-extensions-to-send-adware-filled-updates/?'
  url = 'http://techcrunch.com/2014/01/17/michael-sippey-leaving-twitter/'

  #add url
  good_domains.append(trim_url(url))

  #add gmail
  good_domains.append('gmail.com')


def trim_url(url):
  match = re.search(r'https?:\/\/(.*\..*?)\/', url)
  result = match.group(1)
  print('---------URL: ' + str(result))

  return result
  



if __name__ == '__main__':
  main()
