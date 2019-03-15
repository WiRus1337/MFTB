# TODO пересмотреть фильтрацию, т.к. некоторые результаты не верно фильтруются
# TODO реализовать фильтрацию отдельной функцией
# TODO

import sqlite3
import requests
from bs4 import BeautifulSoup
# import csv
# import json

db_name = 'avito.db'
table_name = 't_all_divs'
фильтры = ('core', 'пк', 'комп', 'ryzen', 'ядер', 'системн', 'ферм', 'pc', 'игровой', 'i3', 'i5', 'i7')


def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('div', class_='pagination-pages clearfix')
    pages = divs.find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)


def check_table(dbname, tablename):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    if tablename == table_name:
        sql = '''CREATE TABLE if not exists {} (
        "id"    TEXT,
        "title"	TEXT,
        "price"	TEXT,
        "url"	TEXT
        )'''.format(tablename)
    if tablename == 'test':
        sql = '''CREATE TABLE if not exists {} (
        "id"    TEXT,
        "title"	TEXT,
        "price"	TEXT,
        "url"	TEXT,
        shown   TEXT
        )
        '''.format(tablename)
    cursor.execute(sql)
    conn.commit()


def write_sqlite(db_name, table_name, data):
    # check_table(db_name, table_name)
    # check_table(db_name, 'test')
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    sql = '''insert into {} values({},'{}','{}','{}')'''.format(table_name, data['id'], data['title'], data['price'],
                                                                data['url'])
    cursor.execute(sql)
    # cursor.execute('insert into {} values(?,?,?,?)', (data['id'], data['title'], data['price'], data['url']))
    conn.commit()
    conn.close()


def sql_delete_all_rows(db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    sql = '''delete from {}'''.format(table_name)
    cursor.execute(sql)
    conn.commit()
    conn.close()


def get_page_data(html):
    i = 0
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
            title = div.text.strip()
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
        data = {'id': id,
                'title': title,
                'price': price,
                'url': url}
        # print(data)
        # write_csv(data)
        write_sqlite('avito.db', 't_all_divs', data)
        i += 1
        # write_to_json(data)
    print('Произведено {} записей\n'.format(i))
    


# результат парсинга переносим в справочник объявлений
def temp_to_catalog_divs(db_name, temp_table, res_table):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    sql = '''
    insert into {1} (id, title, price, url ) SELECT * from {0} a where a.id not in (select t.id from {1} t)
    '''.format(temp_table, res_table)
    cursor.execute(sql)
    conn.commit()
    conn.close()


# фильтруем резултат
# def filtering():
def фильтрование(запрос, фильтры):  # запрос, имя_полного_списка, фильтры                   фильтрование(фильтры = "пк")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(запрос)
    rows = cursor.fetchall()
    for row in rows:
        (id, title, price, url, shown) = tuple(row)
        trigger = 0
        if shown == 'false':
            for фильтр in фильтры:
                if title.lower().find(фильтр) != -1:
                    trigger += 1
            if trigger == 0:
                return title


    conn.commit()
    conn.close()


def main():
    """https://www.avito.ru/krasnodar?s_trg=3&q=%D0%BA%D1%80%D0%B5%D1%81%D0%BB%D0%BE+samurai"""
    base_url = "https://avito.ru/krasnodar?"
    page_part = "p="
    query_par = "&q" + "=geforce+1060"
    check_table(db_name, table_name)
    check_table(db_name, 'test')
    total_pages = get_total_pages(get_html(base_url + query_par))
    sql_delete_all_rows(db_name, table_name)
    print('Всего найдено страниц {}'.format(total_pages))
    x = int(input('Сколько проверяем страниц? '))
    for i in range(1, x + 1):
        print('страница №  {}'.format(i))
        url_gen = '{}{}{}{}'.format(base_url, page_part, i, query_par)
        print('{}'.format(url_gen))
        html = get_html(url_gen)
        get_page_data(html)
    temp_to_catalog_divs(db_name, table_name, 'test')
    запрос = 'select * from {}'.format('test')
    print( фильтрование(запрос, фильтры))
    # filtering()
    # запись в БД завершена, можно переходить к выводу информации в каком то виде


if __name__ == '__main__':
    main()
