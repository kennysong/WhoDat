import requests
import lxml.html
import re
from lxml.cssselect import CSSSelector


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
    if (sel_null(tree)):
        print 'Null results'
        return companies
    
    # Get profile links on results page
    search = sel_a(tree)
    links = [result.get('href') for result in search]


    # Go to each profile page of results
    for link in links:
    #for link in links[:3]:
        print 'Getting: ' + link
        html = requests.get(link).text
        tree = lxml.html.fromstring(html)

        sel_job = CSSSelector('.headline-title, .title')
        search = sel_job(tree)
        if search == []:
            continue
        
        job = search[0].text
        company = job.split(' at ')[-1]
        companies.append(company)
        
    # Remove whitespace, things with only punctuation
    companies = [company.strip(' \t\n\r') for company in companies]
    companies = [company for company in companies if re.sub('\W', '', company) != '']
    

    return companies
