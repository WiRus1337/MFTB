# TODO пересмотреть фильтрацию, т.к. некоторые результаты не верно фильтруются
# TODO реализовать фильтрацию отдельной функцией
# TODO
import time
import re
import prsr
import db

db_name = 'avito.db'
table_name = 't_all_divs'
фильтры = ('core', 'пк', 'комп', 'ryzen', 'ядер', 'системн', 'ферм', 'pc', 'игровой', 'i3', 'i5', 'i7')


def main_():
    """https://www.avito.ru/krasnodar?s_trg=3&q=%D0%BA%D1%80%D0%B5%D1%81%D0%BB%D0%BE+samurai"""
    # описываем параметры запроса
    base_url = "https://avito.ru/krasnodar?"
    page_part = "p="
    query_par = "&q=" + "geforce+1060+6gb"

    db.check_table(db_name)  # создаем таблицы, если их нет
    total_pages = prsr.get_total_pages(prsr.get_html(base_url + query_par))  # определяем количество страниц
    db.sql_delete_all_rows(db_name, table_name)  # очищаем таблицу
    print('Всего найдено страниц {}'.format(total_pages))
    x = int(input('Сколько проверяем страниц? '))
    for i in range(1, x + 1):  # перебираем указаное количество страниц
        print('страница №  {}'.format(i))
        url_gen = '{}{}{}{}'.format(base_url, page_part, i, query_par)  # формируем запрос
        print('{}'.format(url_gen))
        html = prsr.get_html(url_gen)  # получаем HTML страницы
        # парсим HTML  и записываем в БД
        data = prsr.get_page_data(html)
        # print(data)
        for line in data:
            print(data[line])
            db.write_sqlite(db_name='avito.db', table_name='t_all_divs', data=data[line])

    db.temp_to_catalog_divs(db_name, table_name, 'test')  #
    запрос = 'select * from {}'.format('test')
    # print( db.фильтрование(запрос, фильтры))
    # filtering()
    # запись в БД завершена, можно переходить к выводу информации в каком то виде


def main():
    query = input('Введите номер запроса ')
    if re.findall(r'\d*', query)[0] != '':
        # получаем параметры поиска из БД
        config = db.get_user_config(query)
        c_query_id = int(config[0][0])
        c_search_query = re.sub(' ', '+', '{}'.format(config[0][1]))
        c_user_id = int(config[0][2])
        if config[0][3] is not None:
            c_filter = re.split(',', config[0][3])
        else:
            c_filter = ''
    elif re.findall(r'\d*', query)[0] == '':
        print('query is empty')
        exit()




if __name__ == '__main__':
    main()
