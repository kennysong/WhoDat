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

def remove_duplicates(original_list):
    seen = set()
    seen_add = seen.add
    return [ x for x in original_list if x not in seen and not seen_add(x)]
	
def main():
	print find_site("Barack Obama")

if __name__ == "__main__":
	main()