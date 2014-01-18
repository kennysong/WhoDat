from fuzzywuzzy import fuzz
from alch_keys import get_alch_keys
from linkedin import get_companies
from find_domain import find_site
import re

MAGIC = 70

def main():
  domains = get_domains(name, url)
  print('')
  print('Domain keywords: ' + str(domains))

def get_domains(name, url):
  good_domains = []

  #personal
  good_domains.append(name)

  good_domains += comp_link_alch(name, url)
  
  better_domains = []

  #send domains to google
  for domain in good_domains:
    better_domains += find_site(domain)

  return better_domains

def comp_link_alch(name, url):
  #compare keywords from alchemy and companies from linkedin scraping using fuzzywuzzy
  good_domains = []
  print('-------getting companies')
  companies = get_companies(name)

  if url:
    print('-------getting alch keys')
    alch_keys = get_alch_keys(url)

  if not companies and alch_keys:
    print('-------no companies from linkedin')
    good_domains.append(alch_keys)
  elif companies and not alch_keys:
    print('-------no alchemy keywords')
    good_domains.append(companies)
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

  return good_domains

if __name__ == '__main__':
  main()
