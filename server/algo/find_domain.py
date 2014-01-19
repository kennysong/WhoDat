import requests

def find_site(name):
	url = "http://google.com/search?q=" + name
	r = requests.get(url=url)

	links = []
	res = r.text
	res_list = res.split("&amp;")
	for link in res_list:
		if 'href="/url?q=' in link:
			link = link.split('href="/url?q=')[1]
			if 'googleusercontent' not in link:
				links.append(link)
	good_links = []
	for link in links:
		if not (link[-1:] == "/" and link.count("/") > 3) and not (link[-1:] != "/" and link.count("/") > 2):
			good_links.append(link)
	return remove_duplicates(good_links)

def has_results(email):
	url = "https://www.google.com/search?q=" + '"' + email + '"'
	r = requests.get(url=url)

	if ("Your search - <em>&quot;" + email + "&quot;</em> - did not match any documents.") in r.text or \
		("Your search - <b>" + '"' + email + '"' + "</b> - did not match any documents.") in r.text or \
		("No results found for <b>&quot;" + email + "&quot;</b>.") in r.text or \
		("No results found for <b>" + '"' + email + '"' + "</b>") in r.text:
		return False
	return True

def remove_duplicates(original_list):
    seen = set()
    seen_add = seen.add
    return [ x for x in original_list if x not in seen and not seen_add(x)]
	
def main():
	print find_site("Marco Rubio")
	print has_results("jared@getwhodat.com")

if __name__ == "__main__":
	main()