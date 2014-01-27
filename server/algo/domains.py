from fuzzywuzzy import fuzz
from alch_keys import get_alch_keys
from linkedin import get_companies
from find_domain import find_site
from find_domain import remove_duplicates
import re

FUZZY_SEARCH_ACCURACY = 70 # accuracy needed, out of 100


def get_domains(name, url):
	# Called by: get_possible_emails() in emails.py
	keywords = []
	keywords += get_keywords_from_url_and_linkedin(name, url)
	
	domains = []

	# from current url
	trimmed = trim_url(url)
	if trimmed:
		domains.append(trimmed)

	# keywords --> urls
	urls = []
	for word in keywords:
		urls += talk_to_google(word)
	
	# limit to 2
	if (len(urls) > 2):
		for i in range(0,2):
			domains.append(urls[i])
	else:
		domains += urls

	# gmail
	domains.append('gmail.com')

	return remove_duplicates(domains)

def talk_to_google(key):
	# perform a google search and return all results that are root domain (ex: http://google.com/, NOT http://google.com/user)
	sites = find_site(key)

	results = []
	for site in sites:
		trimmed = trim_url(site)
		if trimmed and trimmed not in results:
			results.append(trimmed)
	return results

def get_keywords_from_url_and_linkedin(name, url):
	#compare keywords from alchemy and companies from scraping linkedin using fuzzywuzzy
	domains = []
	
	# scrape linkedin for companies
	print('-------getting companies')
	companies = get_companies(name)
	print('companies: ' + str(companies))

	if url:
		# perform semantic analysis on url, return keys
		print('-------getting alch keys')
		alch_keys = list(get_alch_keys(url))

	if not companies and alch_keys:
		print('-------no companies from linkedin')
		domains += list(alch_keys)
	elif companies and not alch_keys:
		print('-------no alchemy keywords')
		domains += companies
	else:
		print('-------alchemy: ' + str(len(alch_keys)))
		print('-------companies: ' + str(len(companies)))
		for alch in alch_keys:
			for company in companies:
				similarity = fuzz.ratio(alch, company)
				print(alch + ', ' + company +  ': ' + str(similarity))
				if similarity > FUZZY_SEARCH_ACCURACY:
					print('-------Magic! Found a match, added linkedin company')
					domains.append(company)
		if not domains:
			print('--------no matches found from linkedin and alchemy')
			domains = companies + list(alch_keys)

	return flatten(domains)

def flatten(lst):
	"""Flatten a list.
		ex: [[1,2,[3]],6] --> [1,2,3,6]
	"""
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

def main():
	name = 'Michael Sippey'
	url = 'http://techcrunch.com/2014/01/17/michael-sippey-leaving-twitter/'

	domains = get_domains(name, url)
	print('')
	print('Domain keywords: ' + str(domains))

if __name__ == '__main__':
	main()
