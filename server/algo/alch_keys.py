from alchemyapi import AlchemyAPI
import re
import requests
from fuzzywuzzy import fuzz

NAMES_FILE = 'yob2012.txt'
CRUNCHBASE_API_KEY = 'gmtp8kq3tcpgtfmyqyq4av5e'


def main():
  #url = 'http://sploid.gizmodo.com/how-ilm-created-hong-kong-with-special-effects-just-to-1503938272/@caseychan'
  #url = 'http://www.theverge.com/2014/1/17/5316980/president-obama-nsa-signals-intelligence-reform-report-card'
  #url = 'http://techcrunch.com/2014/01/17/facesubstitute-is-the-coolest-and-creepiest-thing-youll-see-this-week/'
  url = 'http://www.nytimes.com/2014/01/19/us/politics/film-gives-a-peek-at-the-romney-who-never-quite-won-over-voters.html?hp'
  alch_keys = get_alch_keys(url)
  for i in alch_keys:
    print i, (verify_companies_with_crunchbase(i))


def verify_companies_with_crunchbase(name):
  url = "http://crunchbase.com/v/1/search.js"
  data = {"query" : name}
  r = requests.get(url=url, data=data)
  results = r.json()
  if len(name) > 4:
    if len(results["results"]) > 0 and results['results'][0]["namespace"] == "company" and "name" in results['results'][0].keys() and fuzz.ratio(results['results'][0]["name"], name) >= 70:
      return True
  else:
    if len(results["results"]) > 0 and results['results'][0]["namespace"] == "company" and "name" in results['results'][0].keys():
      return True
  return False

#returns a set of possible key words from alchemy api based on the text on the page at the given url
def get_alch_keys(url):
  #Create the AlchemyAPI Object
  print('-----Create AlchemyAPI')
  alch = AlchemyAPI()

  alch_keys = set()
  print('-----get concepts')
  alch_keys |= get_concepts(url, alch)
  print('-----get keywords')
  alch_keys |= get_keywords(url, alch)
  print('-----get entities')
  alch_keys |= get_entities(url, alch)

  good_alch_keys = set()
  for i in alch_keys:
    if verify_companies_with_crunchbase(i):
      good_alch_keys.add(i)
  return good_alch_keys

def get_concepts(url, alch):
  response = alch.concepts('url', url)
  concepts = set()
  if response['status'] == 'OK':
    for concept in response['concepts']:
      con_txt = concept['text'].encode('utf-8')
      if con_txt.istitle() and not is_name(con_txt):
        #concepts.add(normalize(con_txt))
        concepts.add(con_txt)
  else:
    print('Error in concept tagging call: ', response['statusInfo'])
  return concepts

def get_keywords(url, alch):
  response = alch.keywords('url', url, { 'sentiment':1 })
  if response['status'] == 'OK':
    keywords = set()
    for keyword in response['keywords']:
      key_txt = keyword['text'].encode('utf-8')
      if key_txt.istitle() and not is_name(key_txt):
        #keywords.add(normalize(key_txt))
        keywords.add(key_txt)
  else:
    print('Error in keyword extaction call: ', response['statusInfo'])
  return keywords

def get_entities(url, alch):
  response = alch.entities('url', url, { 'sentiment':1 })
  if response['status'] == 'OK':
    entities = set()
    for entity in response['entities']:
      ent_txt = entity['text'].encode('utf-8')
      if ent_txt.istitle() and not is_name(ent_txt):
        #entities.add(normalize(ent_txt))
        entities.add(ent_txt)
  else:
    print('Error in entity extraction call: ', response['statusInfo'])
  return entities

def is_name(str):
  has_prefix = False
  has_first_name = False
  str_split = str.split(' ')
  first_word = str_split[0]
  #if the first word in the string is a name prefix the text is a name
  match = re.search(r'(m|M)r?s?\.?', first_word)
  if match:
    has_prefix = True
  #if first word in the string is in one of the names in the names files of popular names
  #the string is a name
  else:
    has_first_name = first_word in open(NAMES_FILE).read()
  return has_prefix or has_first_name

def normalize(str):
  return str.lower().replace(' ','').replace('.','')

if __name__ == '__main__':
  main()
