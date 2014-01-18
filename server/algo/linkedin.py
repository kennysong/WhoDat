import requests
import lxml.html
from lxml.cssselect import CSSSelector

## todo: Make search more robust by going to each individual profile page

def get_companies(name):
	"""Returns list of companies from LinkedIn"""
	first = name.split()[0]
	last = name.split()[-1]
	url = "https://www.linkedin.com/pub/dir/?first=%s&last=%s"%(first,last)

	html = requests.get(url).text
	tree = lxml.html.fromstring(html)
	sel = CSSSelector('.vcard-basic dd, .title')

	search = sel(tree)
	jobs = [result.text for result in search]

	companies = [job.split(' at ')[-1].lower().strip() for job in jobs]

	return companies
	
