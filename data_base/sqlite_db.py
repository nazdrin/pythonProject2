import sqlite3 as sq
import json
#egyjgkyukk
def sql_start(): #создание базы данных и таблиц
    global base
    global cur
    base = sq.connect('users.db')
    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS {} (id_user PRIMARY KEY, code_chain, user_first_name )'.format('users'))
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS {} (code_chain PRIMARY KEY, name_chain, manager)'.format('pharma'))
    base.commit()
    base.execute('CREATE TABLE IF NOT EXISTS {} (number_request, id_user, id_message, text_request, status, code_chain, name_chain, time_message)'
                 .format('requests'))
    base.commit()
def sql_check_code (code_chain):# запрос наименовния сети по коду сети
    name_chain = cur.execute('SELECT name_chain FROM pharma WHERE code_chain == ?', (code_chain,)).fetchone()
    return name_chain

def sql_select(id_user): #запрос кода сети и наименования сети по ИД пользователя
    code_chain = cur.execute('SELECT code_chain FROM users WHERE id_user == ?', (id_user,)).fetchone()
    code_chain = code_chain[0]
    name_chain = sql_check_code(code_chain)
   # name_chain = cur.execute('SELECT name_chain FROM pharma WHERE code_chain == ?', (code_chain,)).fetchone()
    name_chain = name_chain[0]
    return code_chain, name_chain

def sql_select_name(code_chain, id_user, first_name):#запрос наименования сети по коду сети, запись данных пользователя
    name_chain = sql_check_code(code_chain)
    #name_chain = cur.execute('SELECT name_chain FROM pharma WHERE code_chain == ?', (code_chain,)).fetchone()
    name_chain = name_chain[0]
    cur.execute('INSERT INTO users VALUES (?, ?, ?)', (id_user, code_chain, first_name))
    base.commit()
    return name_chain

def sql_insert_message(number_request, id_user, id_message, text_request, status, code_chain, name_chain, time_message):
    cur.execute('INSERT INTO requests VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (number_request, id_user, id_message, text_request, status, code_chain, name_chain, time_message))
    base.commit()





def sql_change_status_message(id_message):#изменение статуса сообщения
    cur.execute('UPDATE requests SET status == ? WHERE id_message == ?', ('Ответ предоставлен', id_message))
    base.commit()

def sql_report ():#запрос данных для отчёта по неотвеченным
    report = cur.execute('SELECT number_request, id_message, code_chain, name_chain, time_message FROM requests WHERE status == ?',
                         ('Отправлено',)).fetchall()
    return report

def sql_insert_new_chain(code_chain, name_chain, manager):# Ввод данных по новой сети
    cur.execute('INSERT INTO pharma VALUES (?, ?, ?)', (code_chain, name_chain, manager))
    base.commit()

def sql_change_status_request(number_request):# изменение статуса запроса
    report = cur.execute('SELECT code_chain FROM requests WHERE number_request == ?', (number_request,)).fetchall()
    cur.execute('UPDATE requests SET status == ? WHERE number_request == ?', ('Ответ предоставлен', number_request))
    base.commit()
    return report

def sql_change_status_all():# изменение всех статусов
    cur.execute('UPDATE requests SET status == ? WHERE status == ?', ('Ответ предоставлен', 'Отправлено'))
    base.commit()

def number_json ():# изменение номера запроса
    with open('number.txt') as json_file:
        number_request = json.load(json_file)
        number_request += 1
    with open('number.txt', 'w') as outfile:
        json.dump(number_request, outfile)
    return number_request
def sql_new_user(id_user, code_chain, users_name):
    cur.execute('INSERT INTO users VALUES (?, ?, ?)', (id_user, code_chain, users_name))
    base.commit()



