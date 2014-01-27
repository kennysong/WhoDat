from alchemyapi import AlchemyAPI
import re

NAMES_FILE = 'yob2012.txt'

def get_alch_keys(url):
	"""Returns:
		list: possible key words from alchemy api
					based on the text on the page at the given url
		"""
	# Create the AlchemyAPI Object
	print('-----Create AlchemyAPI')
	alchemy_obj = AlchemyAPI()

	alch_keys = set()
	print('-----get concepts')
	alch_keys |= get_concepts(url, alchemy_obj)
	print('-----get keywords')
	alch_keys |= get_keywords(url, alchemy_obj)
	print('-----get entities')
	alch_keys |= get_entities(url, alchemy_obj)

	return list(alch_keys)

def get_concepts(url, alchemy_obj):
	response = alchemy_obj.concepts('url', url)
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

def get_keywords(url, alchemy_obj):
	response = alchemy_obj.keywords('url', url, { 'sentiment':1 })
	keywords = set()
	if response['status'] == 'OK':
		for keyword in response['keywords']:
			key_txt = keyword['text'].encode('utf-8')
			if key_txt.istitle() and not is_name(key_txt):
				#keywords.add(normalize(key_txt))
				keywords.add(key_txt)
	else:
		print('Error in keyword extaction call: ', response['statusInfo'])
	return keywords

def get_entities(url, alchemy_obj):
	response = alchemy_obj.entities('url', url, { 'sentiment':1 })
	entities = set()
	if response['status'] == 'OK':
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

def main():
	url = 'http://www.nytimes.com/2014/01/19/us/politics/film-gives-a-peek-at-the-romney-who-never-quite-won-over-voters.html?hp'
	alch_keys = get_alch_keys(url)

if __name__ == '__main__':
	main()