import requests
import lxml.html
from lxml.cssselect import CSSSelector
import re

def get_companies(name):
    """Returns list of companies from LinkedIn"""
    companies = []
    first = name.split()[0]
    last = name.split()[-1]
    url = "https://www.linkedin.com/pub/dir/?first=%s&last=%s"%(first,last)

    # Get page from searching for first last name
    html = requests.get(url).text
    tree = lxml.html.fromstring(html)
    sel_a = CSSSelector('h2 strong a')

    # Check if page is empty
    sel_null = CSSSelector('.null-results')
    if (not sel_null(tree)):
        return companies

    # Determine if page is search results or profile page (ie. only one result)
    sel_title = CSSSelector('title')
    if ('profiles' in sel_title(tree)[0].text):
        # If page shows results
        
        # Get profile links on results page
        search = sel_a(tree)
        links = [result.get('href') for result in search]


        # Go to each profile page of results
        for link in links:
            print 'Getting: ' + link
            html = requests.get(link).text

            sel_job = CSSSelector('.headline-title, .title')
            search = sel_job(tree)
            job = search[0].text
            company = headline.split(' at ')[-1]
            companies.append(company) 
            
        
    else:
        # If page shows a profile
        sel_job = CSSSelector('.headline-title, .title')
        search = sel_job(tree)
        job = search[0].text
        company = headline.split(' at ')[-1]
        companies.append(company) 

    return companies
        
            
            
    
    
