# -*- coding: utf-8 -*-
import os
import glob
import random
import sqlite3
conn = sqlite3.connect('fitness.sqlite')
c = conn.cursor()


# РАБОТА С ПОЛЬЗОВАТЕЛЯМИ
#Создание таблицы
c.execute("CREATE TABLE IF NOT EXISTS users (user_id int primary key, surname varchar, name varchar, gruppa varchar)")
conn.commit() #отправка данных в базу

#добавить пользователя в базу
def add_user(id, surname, name, gruppa):
    c.execute("INSERT INTO users (user_id, surname, name, gruppa) VALUES (?, ?, ?, ?)",(id, surname, name, gruppa))
    conn.commit()

# список всех пользователей
def list_all():
    c.execute('SELECT * FROM users')
    return c.fetchall()

# список пользователей по id
def list_them(ids):
    users = []
    for id in ids:
        c.execute('SELECT surname, name, gruppa FROM users WHERE user_id={}'.format(id))
        user = c.fetchone()
        users.append(user)
    return users

# изменить данные в нужном столбце
def update_name(surname, name, id):
    c.execute('UPDATE users SET surname=? WHERE user_id=?',(surname, id))
    c.execute('UPDATE users SET name=? WHERE user_id=?',(name, id))
    conn.commit()

def del_user(id):
    c.execute('DELETE FROM users WHERE user_id={}'.format(id))
    conn.commit()


# РАБОТА С РАСПИСАНИЕМ
c.execute("CREATE TABLE IF NOT EXISTS timetable (lesson_id int, lesson varchar, day varchar, time varchar, g_size tinyint, left tinyint)")
conn.commit() #отправка данных в базу

# список всех занятий с оставшимися местами
def list_timetable():
    c.execute('SELECT lesson, day, time, left FROM timetable')
    return c.fetchall()

# создать занятие
def add_lesson(lesson, day, time, g_size):
    lesson_ids = [id[0] for id in c.execute('SELECT lesson_id FROM timetable').fetchall()]
    #print(lesson_ids)
    lesson_id = 10
    while lesson_id in lesson_ids: # если такой уже есть
        lesson_id = random.randint(10,99) # подбираем новый id -- используем буквы, т.к. нельзя создать таблицу с числом в имени
    #print('new', lesson_id)
    c.execute("INSERT INTO timetable (lesson_id, lesson, day, time, g_size, left) VALUES (?, ?, ?, ?, ?, ?)",(lesson_id, lesson, day, time, g_size, g_size))

    # создаём табличку для занятия
    c.execute("CREATE TABLE IF NOT EXISTS z{} (user_id int primary key, surname varchar, name varchar, gruppa varchar)".format(lesson_id))
    conn.commit()


# записать пользователя на занятие
def add_to_lesson (lesson_id, user_id):
    # сколько людей может записаться на занятие
    g_size = c.execute('SELECT g_size FROM timetable WHERE lesson_id={}'.format(lesson_id)).fetchone()[0]
    print(g_size)
    # сколько уже записались
    n_people = c.execute('SELECT COUNT(*) FROM z{}'.format(lesson_id)).fetchone()[0] # выдаёт кортеж
    print(n_people)
    left = g_size - n_people
    print(left)
    if left:
        #print(True)
        user_data = c.execute('SELECT surname, name, gruppa FROM users WHERE user_id={}'.format(user_id)).fetchone()
        print(user_data)
        # записали человека
        c.execute("INSERT INTO z{} VALUES (?, ?, ?, ?)".format(lesson_id),(user_id, user_data[0], user_data[1], user_data[2]))
        # уменьшили количество свободных мест на зантие
        c.execute('UPDATE timetable SET left=? WHERE lesson_id=?',(left-1, lesson_id))

        conn.commit()
    else:
        raise Exception('Мест больше нет!')

# id всех записавшихся
def list_lesson(lesson_id):
    user_ids = user_ids = [id[0] for id in c.execute('SELECT user_id FROM z{}'.format(lesson_id)).fetchall()]
    return user_ids

# отменить запись на занятие
def del_from_lesson(lesson_id, user_id):
    # записавшиеся
    user_ids = list_lesson(lesson_id)
    #print(user_ids)
    if user_id in user_ids:
        c.execute('DELETE FROM z{} WHERE user_id={}'.format(lesson_id, user_id))
        # увеличили количество свободных мест на зантие
        left = c.execute('SELECT left FROM timetable WHERE lesson_id={}'.format(lesson_id)).fetchone()[0]
        c.execute('UPDATE timetable SET left=? WHERE lesson_id=?',(left+1, lesson_id))
        conn.commit()
    else:
        raise Exception('Нету таких!')


# отменить занятие
def del_lesson(lesson_id):
    user_ids = list_lesson(lesson_id) # список записавшихся
    c.execute('DELETE FROM timetable WHERE lesson_id={}'.format(lesson_id)) # удаляем из расписания
    c.execute('DROP TABLE z{}'.format(lesson_id)) # удаляем занятие
    conn.commit()
    return user_ids



#add_user(21, 'Сафарян', 'Анна', '15ФПЛ')
#add_user(22, 'Егорова', 'Алина', '15ФПЛ')
#add_user(23, 'Николаев', 'Кирилл', '15ФПЛ')

#update_name('Сафарян', 'Аня', 21)

'''
users = list_all()
print(len(users)) # список
for user in users:
    print(type(user), user) # кортежи
'''

#ids = [21, 23]
#users = list_them(ids)
#print(users)

'''
del_user(23)
users = list_all()
print(len(users)) # список
for user in users:
    print(type(user), user) # кортежи
'''

#add_lesson('Пилатес', 'Пн', '17-00', 2)
#add_lesson('Круговая тренировка', 'Вт', '17-00', 2)

#timetable = list_timetable()
#print(*timetable, sep='\n')

'''
add_to_lesson(10,22)
add_to_lesson(10,23)
try:
    add_to_lesson(10,21)
except:
    print("Места кончились :(")
'''
#print(list_them(list_lesson(10)))


'''
del_from_lesson(10, 23)
try:
    del_from_lesson(10, 21)
except:
    print('А вы и не записывались!')
'''

#print(del_lesson(40))
#print(del_lesson(21))



# закрываем соединение с базой
c.close()
conn.close()
