from alchemyapi import AlchemyAPI

NAMES_FILE = 'yob2012.txt'

def main():
  #url = 'http://sploid.gizmodo.com/how-ilm-created-hong-kong-with-special-effects-just-to-1503938272/@caseychan'
  url = 'http://www.theverge.com/2014/1/17/5316980/president-obama-nsa-signals-intelligence-reform-report-card'
  #url = 'http://techcrunch.com/2014/01/17/facesubstitute-is-the-coolest-and-creepiest-thing-youll-see-this-week/'
  domains = get_domains(url)

def get_domains(url):
  #Create the AlchemyAPI Object
  alch = AlchemyAPI()

  domains = set()
  domains |= get_concepts(url, alch)
  domains |= get_keywords(url, alch)
  domains |= get_entities(url, alch)
  print(domains)

  return domains

def get_concepts(url, alch):
  response = alch.concepts('url', url)
  if response['status'] == 'OK':
    concepts = set()
    for concept in response['concepts']:
      con_txt = concept['text'].encode('utf-8')
      if con_txt.istitle() and not is_name(con_txt):
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
        entities.add(ent_txt)
  else:
    print('Error in entity extraction call: ', response['statusInfo'])
  return entities

def is_name(txt):
  #determine if string is a name by checking to see if the first word
  #is in the file with the list of most popular names
  txt_split = txt.split(' ')
  return txt_split[0] in open(NAMES_FILE).read()

if __name__ == '__main__':
  main()
