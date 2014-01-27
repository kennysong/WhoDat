from domains import get_domains, talk_to_google
from name_permut import get_all_username_permutations

def main():
	name = 'Scott Weiss'
	#name = 'Ron Amadeo'
	#name = 'Michael Sippey'
	url = 'http://scott.a16z.com/2014/01/17/success-at-work-failure-at-home/'
	#url = 'http://arstechnica.com/security/2014/01/malware-vendors-buy-chrome-extensions-to-send-adware-filled-updates/?'
	#url = 'http://techcrunch.com/2014/01/17/michael-sippey-leaving-twitter/'

	print(get_possible_emails(name, url))


def get_possible_emails(name, url):
	emails = []

	usernames = get_all_username_permutations(name)
	print('Usernames: ' + str(usernames))

	domains = get_domains(name, url)
	print('Domains: ' + str(domains))

	# personal site
	personal_sites = talk_to_google(name)
	for site in personal_sites:
		email = 'me@' + site
		emails.append(email)
	
	# all permutations
	for domain in domains:
		for username in usernames:
			email = username + '@' + domain
			emails.append(email)

	return remove_duplicates(emails)


if __name__ == '__main__':
	main()
