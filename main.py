import requests
from bs4 import BeautifulSoup
import lxml
from fake_headers import Headers
import time

response = requests.get('https://habr.com/ru/articles/', headers=Headers(browser='chrome',os='win').generate())

soup = BeautifulSoup(response.text, features='lxml')
article_list = soup.find_all('div', class_='tm-articles-list')

keywords = ['дизайн', 'фото', 'web', 'python']
data_list = []
dates = []
articles = []
links = []
texts= []

for article in article_list:

    article_time = article.find_all('time')
    for time in article_time:
        dates.append(time['datetime'][:10])

    article_title = article.find_all('a', class_='tm-title__link')
    for article_item in article_title:
        articles.append(article_item.text)

    article_link = article.find_all('a', class_='tm-title__link')
    for link in article_link:
        links.append('https://habr.com' + link['href'])

    article_text = article.find_all('div', \
            class_='article-formatted-body article-formatted-body article-formatted-body_version-2')
    for text in article_text:
        texts.append(text.text.strip())

zip_data_list = zip(dates, articles, links, texts)
keys = ['date', 'title', 'link', 'text']
data_list = [dict(zip(keys, values)) for values in zip_data_list]
sorted_list = []
for data in data_list:
    for elem in keywords:
        if elem in data['title'].lower():
            print(f'<{data['date']}> - <{data['title']}> - <{data['link']}>')
            sorted_list.append(data)
            break

if not sorted_list:
    print(f'На данный момент статей по запросу: {keywords} - нет')

