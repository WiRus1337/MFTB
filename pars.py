import sqlite3
import requests
from bs4 import BeautifulSoup
import csv
import json


def test():
    print("test")

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
    sql = '''CREATE TABLE if not exists {} (
    	"col1"	TEXT UNIQUE,
    	"col2"	TEXT,
    	"col3"	TEXT,
    	"col4"	TEXT
    )'''.format(tablename)
    cursor.execute(sql)
    conn.commit()

def write_sqlite(dbname, tablename, data):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    sql = '''insert into {} values({},'{}','{}','{}')'''.format(tablename, data['id'], data['title'], data['price'],
                                                                data['url'])
    cursor.execute(sql)
    # cursor.execute('insert into {} values(?,?,?,?)', (data['id'], data['title'], data['price'], data['url']))
    conn.commit()
    conn.close()


def sql_delete_all_rows(dbname, tablename):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    sql = '''delete from {}'''.format(tablename)
    cursor.execute(sql)
    conn.commit()
    conn.close()


def write_csv(data):
    with open('avito.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((data['id'],
                         data['title'],
                         data['price'],
                         data['url']))


# def write_JSON(data):
#     with open('data.json', 'r') as fr:
#         file = json.load(fr)
#     with open('data.json', 'w') as f:
#         target = file[0]
#         target.append(data)
#         json.dump(file, f, ensure_ascii=False,indent=4)
#         # file = json.load(outfile)

def write_to_json(user_info):
    with open('data.json', 'r', encoding='utf-8') as jfr:
        jf_file = json.load(jfr)
    with open('data.json', 'w', encoding='utf-8') as jf:
        jf_target = jf_file[0]
        jf_target.append(user_info)
        json.dump(jf_file, jf, indent=4, ensure_ascii=False, )


def get_page_data(html):
    i = 0
    soup = BeautifulSoup(html, 'lxml')
    divs = soup.find('div', class_='catalog-list')
    ads = divs.find_all('div', class_='item_table')

    filt = ('core', 'пк', 'комп', 'ryzen', 'ядер', 'системн', 'ферм', 'pc', 'игровой', 'i3', 'i5', 'i7')
    for ad in ads:
        try:
            id = ad.get('data-item-id')
        except:
            id = ''
        try:
            div = ad.find('div', class_='description').find('h3')
            s = div.text.lower()
            # TODO пересмотреть фильтрацию, т.к. некоторые результаты не верно фильтруются

            # print(s, end='')
            # for f in filt:
            #     if s.find(f) == -1:
            #         pass
            #     elif s.find(f) != -1:
            #         print('"{}"'.format(f), end=' ')
            # print('\n')
            # # print('\n end')

            flag = False
            for f in filt:
                if s.find(f) != -1:
                    flag += True
                    continue
                else:
                    pass
            if flag:
                continue
            else:
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

        write_sqlite('test.db', 'test', data)
        i += 1
        # write_to_json(data)
    print('Произведено {} записей\n'.format(i))
def sql_to_str():



def main():

    """https://www.avito.ru/krasnodar?s_trg=3&q=%D0%BA%D1%80%D0%B5%D1%81%D0%BB%D0%BE+samurai"""
    # url = "https://avito.ru/moskva/telefony?p=1&q=htc"
    base_url = "https://avito.ru/krasnodar?"
    page_part = "p="
    query_par = "&q" + "=geforce+1060+6gb"
    check_table('test.db', 'test')
    total_pages = get_total_pages(get_html(base_url + query_par))
    sql_delete_all_rows('test.db', 'test')
    for i in range(1, total_pages):
        print('страница №{}'.format(i))
        url_gen = '{}{}{}{}'.format(base_url, page_part, i, query_par)
        html = get_html(url_gen)
        get_page_data(html)
    # запись в БД завершена, можно переходить к выводу информации в каком то виде


if __name__ == '__main__':
    main()
