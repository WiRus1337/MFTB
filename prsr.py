import requests
from bs4 import BeautifulSoup
import re

def config():

    pass

def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('div', class_='pagination-pages clearfix')
    pages = divs.find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)


def get_page_data(html):
    i = 0
    data = {}
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('div', class_='catalog-list')
    ads = divs.find_all('div', class_='item_table')

    for ad in ads:
        try:
            id = ad.get('data-item-id')
        except:
            id = ''
        try:
            div = ad.find('div', class_='description').find('h3')
            title = re.sub("'", '', '{}'.format(div.text.strip()))
        except:
            title = ''
        try:
            div = ad.find('div', class_='description').find('h3')
            url = "https://avito.ru" + div.find('a').get('href')
        except:
            url = ''
        try:
            price = ad.find('span', itemprop="price").text.strip()
        except:
            price = ''
        data[i] = {'id': id,
                'title': title,
                'price': price,
                'url': url}
        i += 1
    return data
    print('Произведено {} записей\n'.format(i))