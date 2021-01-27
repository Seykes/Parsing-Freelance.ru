import requests
from bs4 import BeautifulSoup
import os


PATH_ROOT = os.path.dirname(__file__)
URL = 'https://freelance.ru/freelancers/it-i-programmirovanie'
HOST = 'https://freelance.ru'
print(PATH_ROOT)


def get_links(url, host):
	html = requests.get(url)
	soup = BeautifulSoup(html.text, 'html.parser').find('div', class_='specs_nav_block')
	links = []
	for link in soup.find_all('a'):
		links.append(host + link.get('href'))
	return links


links = get_links(URL, HOST)
pages_count = []


def get_pages_count(links):
	for link in links[2:7]:
		html = requests.get(link)
		soup = BeautifulSoup(html.text, 'html.parser')
		foo = soup.find('ul', class_='pagination pagination-lg')
		bar = []
		try:
			for a in foo.find_all('a', href=True):
				if a:
					try:
						foobar = int(a.string)
					except:
						continue
					print(foobar)
		except:
			continue


get_pages_count(links)
print(pages_count)


def get_users(links, host):
	for link in links:
		html = requests.get(link)
		users = BeautifulSoup(html.text, 'html.parser').find_all('a', class_='user-card-name')
		users_links = []
		for user in users:
			users_links.append(user.get('href'))
		return users_links


users_links = get_users(links, HOST)