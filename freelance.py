# Парсинг всех специалистов с Freelance.ru
import requests
from bs4 import BeautifulSoup
import os


PATH_ROOT = os.path.dirname(__file__)
URL = 'https://freelance.ru/freelancers/it-i-programmirovanie'
HOST = 'https://freelance.ru'


def get_links(url, host):  # Сбор всех ссылок на разделы специалистов
	html = requests.get(url)
	soup = BeautifulSoup(html.text, 'html.parser').find('div', class_='specs_nav_block')
	links = []
	for link in soup.find_all('a'):
		links.append(host + link.get('href'))
	return links


# Получение количества страниц с разделов
def get_pages_count(html):
	soup = BeautifulSoup(html.text, 'html.parser')
	foo = soup.find('ul', class_='pagination pagination-lg')
	bar = []
	if foo:
		for a in foo.find_all('a', href=True):
			try:
				foobar = int(a.string)
				bar.append(foobar)
			except:
				continue
		try:
			return bar[-1]
		except:
			return 1
	else:
		return 1


# Получение ссылок на профили всех спецов
def get_users(links):
	foo = 0
	users_links = []
	for link in links:
		html = requests.get(link)
		if html.status_code == 200:
			pages_count = get_pages_count(html)
			foo += 1
			print(f'Парсинг раздела {foo} из {len(links)}... ')
			for page in range(1, pages_count + 1):
				print(f'Парсинг страницы {page} из {pages_count}...')
				html = requests.get(link, params={'page': page})
				users = BeautifulSoup(html.text, 'html.parser').find_all('a', class_='user-card-name')
				for user in users:
					users_links.append(user.get('href'))
		else:
			print('Подключение не установлено, get_users.error')
		print(users_links)
		return users_links


def get_info(users):
	data = []
	for user in users:
		html = requests.get(user)
		if html.status_code == 200:
			soup = BeautifulSoup(html.text, 'html.parser')
			try:
				data.append({
						'phone': soup.find('p', class_='phone').get_text()})
			except: pass
			try:
				data.append({
						'telegram': soup.find('p', class_='telegram').get_text()})
			except: pass
		else:
			print('Подключение не установлено, get_info.error')
	return data


def main():
	links = get_links(URL, HOST)
	users = get_users(links)
	data = get_info(users)
	print(data)


if __name__ == '__main__':
	main()