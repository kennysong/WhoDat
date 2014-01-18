from fuzzywuzzy import fuzz
from alch_keys import get_alch_keys
from linkedin import get_companies
from find_domain import find_site

MAGIC = 70

def main():
  name = 'Scott Weiss'
  url = 'http://scott.a16z.com/2014/01/17/success-at-work-failure-at-home/'
  print(get_domains(name, url))

def get_domains(name, url):
  #compare keywords from alchemy and companies from linkedin scraping using fuzzywuzzy
  print('-------getting alch keys')
  alch_keys = get_alch_keys(url)
  print('-------getting companies')
  companies = get_companies(name)
  good_domains = []

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
        if similarity > MAGIC:
          print('-------Magic! Found a match, added linkedin company')
          good_domains.append(company)

  if not good_domains:
    print('--------no matches found from linkedin and alchemy')
    good_domains = companies.extend(alch_keys)

if __name__ == '__main__':
  main()
  

