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
            s = div.text.lower()

            # print(s, end='')
            # for f in filt:
            #     if s.find(f) == -1:
            #         pass
            #     elif s.find(f) != -1:
            #         print('"{}"'.format(f), end=' ')
            # print('\n')
            # # print('\n end')

            # flag = False
            # for f in filt:
            #     if s.find(f) != -1:
            #         flag += True
            #         continue
            #     else:
            #         pass
            # if flag:
            #     continue
            # else:
            title = re.sub("'", '', '{}'.format(div.text.strip()))
        except:
            title = ''
        try:
            div = ad.find('div', class_='description').find('h3')
            url = "https://avito.ru" + div.find('a').get('href')
        except:
            url = ''
        try:
            price = ad.find('div', class_='about').text.strip()
        except:
            price = ''
        data[i] = {'id': id,
                'title': title,
                'price': price,
                'url': url}
        # print(data)
        # write_csv(data)

        i += 1
        # write_to_json(data)
    return data
    print('Произведено {} записей\n'.format(i))