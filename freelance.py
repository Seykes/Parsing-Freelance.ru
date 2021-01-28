# Парсинг всех специалистов с Freelance.ru
import requests
from bs4 import BeautifulSoup
import os
import csv

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
				html = requests.get(link, params={'page': page})
				users = BeautifulSoup(html.text, 'html.parser').find_all('a', class_='user-card-name')
				for user in users:
					users_links.append(user.get('href'))
		else:
			print('Подключение не установлено, get_users.error')
		print(users_links)
	return users_links


def get_info(users, host):
	data = []
	for user in users:
		html = requests.get(user)
		if html.status_code == 200:
			soup = BeautifulSoup(html.text, 'html.parser')
			foo = []
			f = []
			z = []
			x = []
			y = []
			v = []
			bar = []
			foobar = []
			dialog = []
			try:
				phone = soup.find('p', class_='phone')
				for text in phone:
					f.append(text.text)
			except: pass
			try:
				telegram = soup.find('p', class_='telegram')
				for text in telegram:
					foo.append(text.text)
			except: pass
			try:
				instagram = soup.find('p', class_='instagram')
				for text in instagram:
					z.append(text.text)
			except: pass
			try:
				vkontakte = soup.find('p', class_='vkontakte')
				for text in vkontakte:
					x.append(text.text)
			except: pass
			try:
				whatsapp = soup.find('p', class_='whatsapp')
				for text in whatsapp:
					y.append(text.text)
			except: pass
			try:
				skype = soup.find('p', class_='skype')
				for text in skype:
					v.append(text.text)
			except: pass
			try:
				specs = soup.find('div', class_='specs')
				for text in specs:
					bar.append(text.text)
			except: pass
			try:
				reviews = soup.find('b', class_='cnt')
				foobar.append(reviews.text)
			except: pass
			try:
				dialog.append(host + soup.find('a', class_='g_button btn btn-block btn-default send_mess_btn').get('href'))
			except: pass
			data.append({'phone': f, 'telegram': foo, 'link': user, 'specs': bar, 'reviews': foobar, 'whatsapp': y,
						 'vkontakte': x, 'instagram': z, 'dialog': dialog, 'skype': v})
		else:
			print('Подключение не установлено, get_info.error')
	return data


def save(data):
	with open('freelance.csv', 'w', newline='') as file:
		writer = csv.writer(file, delimiter=';')
		writer.writerow(['Отзывы', 'Ссылка', 'Диалог', 'Телеграмм', 'Телефон', 'Whatsapp', 'ВК', 'Инстаграмм', 'Skype', 'Навыки'])
		for item in data:
			writer.writerow([item['reviews'], item['link'], item['dialog'], item['telegram'], item['phone'],
							 item['whatsapp'], item['vkontakte'], item['instagram'], item['skype'],item['specs']])



def main():
	links = get_links(URL, HOST)
	users = get_users(links)
	data = get_info(users, HOST)
	save(data)


if __name__ == '__main__':
	main()