# TODO при записи, выполнять проверку на наличие такой записи,
#  если записи нет, то INSERT,
#  если запись есть, проверяем есть ли изменения,
#           если изменений нет, то ничего не меняем,
#           если изменениея есть, то INSERT






# import sqlite3
#
# con = sqlite3.connect('users.db')
# with con:
#     cur = con.cursor()
#     cur.execute('SELECT * FROM names')
#     data = cur.fetchone()
#     print data[0]
# con.close()


import sqlite3

from datetime import time

db_name = 'avito.db'
table_name = 't_all_divs'
t_users_config = 'users_config'

def get_user_config(query):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    sql = "select * from '{}' where query_id = {}".format(t_users_config, int(query))
    cursor.execute(sql)
    conn.commit()
    rows = cursor.fetchall()
    return rows


def check_table(db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    sql = '''CREATE TABLE if not exists {} (
        "id"    TEXT,
        "title"	TEXT,
        "price"	TEXT,
        "url"	TEXT,
        "status"    TEXT,
        "changes"   TEXT,
        "datetime"  TEXT
        )'''.format(table_name)
    cursor.execute(sql)
    conn.commit()


def check_data(db_name, table_name, data):
    changes = ''
    check_table(db_name, table_name)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    sql = "select * from {} where id = {}".format(table_name, data['id'])
    cursor.execute(sql)
    conn.commit()
    rows = cursor.fetchall()
    if len(rows) != 0:
        if rows[len(rows)-1][1] != data['title']:
            changes = changes + ' title '
        if rows[len(rows)-1][2] != data['price']:
            changes = changes + ' price '
    elif len(rows) == 0:
        write_sqlite(db_name, table_name, data, changes=changes, status='new')
    print(changes)
    data['changes'] = changes
    if changes != '':
        write_sqlite(db_name, table_name, data, changes=changes, status='changes')
        print('запись в бд')


def write_sqlite(db_name, table_name, data, status, changes):
    import datetime

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    sql = f'''insert into {table_name} values (  {data['id']},
                                                '{data['title']}',
                                                '{data['price']}',
                                                '{data['url']}',
                                                '{status}',
                                                '{changes}',
                                                '{str(datetime.datetime.now())}')'''
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

