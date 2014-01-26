from fuzzywuzzy import fuzz
from alch_keys import get_alch_keys
from linkedin import get_companies
from find_domain import find_site
import re

MAGIC = 70

def main():
  #name = 'Scott Weiss'
  #name = 'Ron Amadeo'
  name = 'Michael Sippey'
  #url = 'http://scott.a16z.com/2014/01/17/success-at-work-failure-at-home/'
  #url = 'http://arstechnica.com/security/2014/01/malware-vendors-buy-chrome-extensions-to-send-adware-filled-updates/?'
  url = 'http://techcrunch.com/2014/01/17/michael-sippey-leaving-twitter/'

  domains = get_domains(name, url)
  print('')
  print('Domain keywords: ' + str(domains))

def get_domains(name, url):
  good_domains = []
  good_domains += comp_link_alch(name, url)
  
  better_domains = []

  #personal
  better_domains += talk_to_google(name)
  really_better = []

  #from current url
  trimmed = trim_url(url)
  if trimmed:
    really_better.append(trimmed)

  #send domains to google to get better list of possible domains
  for domain in good_domains:
    better_domains += talk_to_google(domain)
  if (len(better_domains) > 2):
    for i in range(0,2):
      really_better.append(better_domains[i])
  else:
    really_better += better_domains
  
  really_better.append('gmail.com')

  return really_better

def talk_to_google(key):
  results = []
  sites = find_site(key)
  for site in sites:
    trimmed = trim_url(site)
    if trimmed and trimmed not in results:
      results.append(trimmed)
  return results

def comp_link_alch(name, url):
  #compare keywords from alchemy and companies from linkedin scraping using fuzzywuzzy
  good_domains = []
  print('-------getting companies')
  companies = get_companies(name)
  print('companies: ' + str(companies))

  if url:
    print('-------getting alch keys')
    alch_keys = list(get_alch_keys(url))

  if not companies and alch_keys:
    print('-------no companies from linkedin')
    good_domains += list(alch_keys)
  elif companies and not alch_keys:
    print('-------no alchemy keywords')
    good_domains += companies
  else:
    print('-------alchemy: ' + str(len(alch_keys)))
    print('-------companies: ' + str(len(companies)))
    for alch in alch_keys:
      for company in companies:
        similarity = fuzz.ratio(alch, company)
        print(alch + ', ' + company +  ': ' + str(similarity))
        if similarity > MAGIC:
          print('-------Magic! Found a match, added linkedin company')
          good_domains.append(company)
    if not good_domains:
      print('--------no matches found from linkedin and alchemy')
      good_domains = companies + list(alch_keys)

  return flatten(good_domains)

def flatten(lst):
  if not isinstance(lst, list):
    return lst
  compiled = []
  for i in lst:
    flat = flatten(i)
    if isinstance(flat, list):
      compiled += flat
    else:
      compiled.append(flat)
  return compiled

def trim_url(url):
  match = re.search(r'https?:\/\/(.*\.)?((\w|-)*\.(\w|-)*)\/', url)

  if match:
    result = match.group(2)
    return result

if __name__ == '__main__':
  main()
