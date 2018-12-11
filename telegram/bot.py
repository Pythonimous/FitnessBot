# -*- coding: utf8 -*-

import datetime
import random
import db
from telegram.ext import Filters
from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram.ext import Updater
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import ReplyKeyboardMarkup, KeyboardButton


token='764336853:AAHHE0kNv9m95kUnCt5xmsX2w2av9LwTnaw'

class Bot():

    def __init__(self, token):
        self.chats = {} # chat_id: [user_id, username]
        self.users = {} # user_id: [chat_id, username]
        self.teachers = {} # chat_id: user_id
        self.teacher_key = 'key'


        StartHandler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                'id':[MessageHandler(Filters.text, self.check_id)], # генерация и сопоставление по id
                'name':[MessageHandler(Filters.text, self.name)] # запоминание инфы о пользователе
            },
            fallbacks=[CommandHandler('stop', self.stop_login)]
        )

        MainHandler = ConversationHandler(
            entry_points=[MessageHandler(Filters.text, self.handle_message)],

            states={
                'create': [MessageHandler(Filters.text, self.create_lesson)], #создать занятие
                'cancel': [CallbackQueryHandler(self.cancel_lesson)], # отменить занятие
                'enrol': [CallbackQueryHandler(self.enrol_for_lesson)], # записаться на занятие
                'canrol': [CallbackQueryHandler(self.cancel_enrolment)], # отменить запись
                'list': [CallbackQueryHandler(self.list_lesson)] # просмотреть список на занятие
            },
            fallbacks=[CommandHandler('stop', self.stop)]
        )

        self.updater = Updater(token=token)  # заводим апдейтер
        self.updater.dispatcher.add_handler(CommandHandler('help', self.help))
        self.updater.dispatcher.add_handler(CommandHandler('exit', self.exit))
        self.updater.dispatcher.add_handler(StartHandler)
        self.updater.dispatcher.add_handler(MainHandler)


    teacher_markup = [[KeyboardButton('Расписание'), KeyboardButton('Сброс расписания'), KeyboardButton('Список')],
                   [KeyboardButton('Создать занятие'), KeyboardButton('Отменить занятие')]]
    teacher_menu = ReplyKeyboardMarkup(teacher_markup, resize_keyboard=True, one_time_keyboard=True)

    student_markup = [[KeyboardButton('Расписание'), KeyboardButton('Мои занятия'), KeyboardButton('Список')],
                   [KeyboardButton('Записаться'), KeyboardButton('Отписаться')]]
    student_menu = ReplyKeyboardMarkup(student_markup, resize_keyboard=True, one_time_keyboard=True)


    def stop(self, bot, update):
        if update.message.chat_id in self.teachers:
            menu = self.teacher_menu
        else:
            menu = self.student_menu
        bot.sendMessage(chat_id=update.message.chat_id, text='Действие отменено. Что бы Вы хотели сделать ещё?', reply_markup=menu)
        return ConversationHandler.END

    def stop_login(self, bot, update):
        chat_id = update.message.chat_id
        if chat_id in self.chats: # если успели присвоить id
            user_id = self.chats[chat_id][0]
            del(self.chats[update.message.chat_id]) # удаляем пользователя из чатов
            del(self.users[user_id])
        update.message.reply_text('Регистрация отменена. Обратите внимание, что она необходима для продолжения работы. Введите команду /start, чтобы начать регистрацию.')
        return ConversationHandler.END

    #TODO: опасно в общий доступ: можно разлогиниться, залогиниться под чужим именем и отписаться, а потом вернуться под своё. Разрешить разлогин только мне, Цветочку и Киру на потестить?
    def exit(self, bot, update):
        chat_id = update.message.chat_id
        user_id = self.chats[chat_id][0]
        del(self.chats[chat_id]) # удаляем пользователя из чатов
        del(self.users[user_id])
        if chat_id in self.teachers: # если был преподом
            del(self.teachers[chat_id]) # удаляем из преподов
        bot.sendMessage(chat_id=update.message.chat_id, text='Вы разлогинились. Введите команду /start, чтобы залогиниться и начать работу.')


    def help(self, bot, update):
        help_info = '''
    Чтобы начать работу, введите команду /start и пройдите разовую авторизацию, следуя инструкции. Меню можно открыть, снова введя команду /start или нажав на кнопку клавиатуры в поле ввода (если её нет, попробуйте переключиться на смайлы и обратно). Чтобы остановить операцию и вернуться к меню, введите команду /stop. Чтобы ещё раз посмотреть эту инструкцию, введите команду /help.
    Четырёхзначный код, полученный при первой авторизации — это Ваш уникальный id, номер в системе. Запомните его или запишите, чтобы авторизоваться при входе с другого аккаунта или при подключении к боту в ВКонтакте.\n
*Общие команды:*
        — _Расписание:_\tпросмотр расписания и свободных мест
        — _Список:_\tпросмотр списка студентов, записавшихся на занятие\n
*Студентам:*
        — _Записаться:_\tзапись на занятие (доступны только занятия, на которые остались места)
        — _Отписаться:_\tотмена записи на занятие
        — _Мои занятия:_\tпросмотр занятий, на которые записан(а)\n
*Преподавателям:*
        — _Создать занятие:_\tназначить занятие и открыть запись на него
        — _Отменить занятие:_\tотменить занятие и оповестить об этом записавшихся студентов
        — _Сброс расписания:_\tочистить расписание на прошедшую неделю и списки записавшихся (необходимо делать каждую неделю перед созданием расписания на следующую)\n
        Ключ доступа, необходимый для авторизации в качестве преподавателя, можно узнать на кафедре.'''
        bot.sendMessage(chat_id=update.message.chat_id, text=help_info, parse_mode='Markdown')

    def start(self, bot, update):
        if update.message.chat_id in self.chats: # чат не новый
            print('users\t', self.users)
            print('chats\t', self.chats)
            print('users in base\t', [user for user in db.list_all()])

            if update.message.chat_id in self.teachers:
                menu = self.teacher_menu
            else:
                menu = self.student_menu
            bot.sendMessage(chat_id=update.message.chat_id, text='Здравствуйте, {} ({})! Что бы Вы хотели сделать?'.format(self.chats[update.message.chat_id][1], self.chats[update.message.chat_id][0]), reply_markup=menu)
            return ConversationHandler.END
        else:
            update.message.reply_text('Здравствуйте! Похоже, Вы у нас впервые. Я присвою Вам id — пожалуйста, запомните его, чтобы мой брат в ВК мог узнать Вас. Или он Вам уже присвоен? Введите свой id или отправьте любое сообщение, чтобы получить его.')
            return 'id'

    def check_id(self, bot, update):
        answer = update.message.text
        if answer.isdigit(): # если ввели код
            user_id = int(answer)
            print(user_id)
            user = db.list_them([user_id])[0]
            print(user)
            if user: # если вернулся не None
                self.users[user_id] = [update.message.chat_id, user[1]]
                self.chats[update.message.chat_id] = [user_id, user[1]]
                if db.get_status(user_id) == 'teacher':
                    self.teachers[update.message.chat_id] = user_id
                print('users\t', self.users)
                print('chats\t', self.chats)
                print('teachers\t', self.teachers)
                if update.message.chat_id in self.teachers:
                    menu = self.teacher_menu
                else:
                    menu = self.student_menu
                bot.sendMessage(chat_id=update.message.chat_id, text='Здравствуйте, {} ({})! Что бы Вы хотели сделать?'.format(self.chats[update.message.chat_id][1], self.chats[update.message.chat_id][0]), reply_markup=menu)
                return ConversationHandler.END
            else: # id не нашлось в базе
                bot.sendMessage(chat_id=update.message.chat_id, text='К сожалению, такого id в нашей базе нет. Попробуйте снова или отправьте любое текстовое сообщение, чтобы зарегистрироваться.')
                return 'id'
        else: # совсем новенький
            user_ids = [user[0] for user in db.list_all()] # кто есть в базе
            print('users in base\t', user_ids)
            user_id = random.randint(1000, 9999) # четырёхзначное число
            while user_id in user_ids:
                user_id = random.randint(1000, 9999)
            self.chats[update.message.chat_id] = [user_id]
            self.users[user_id] = [update.message.chat_id]
            update.message.reply_text('{}'.format(user_id))
            bot.sendMessage(chat_id= update.message.chat_id, text='Тогда представьтесь, пожалуйста.\n*Если Вы студент:* введите фамилию, имя и группу через запятую в формате "Фамилия, Имя, группа".\n_Пример: Иванов, Иван, 15ФПЛ_\n*Если Вы преподаватель:* введите фамилию, имя и ключ доступа через запятую в формате "Фамилия, Имя Отчество, ключ доступа".\n_Пример: Иванов, Иван Иванович, key_\n\n*Внимательно проверяйте все данные! В текущей версии пока нет возможности их исправить.*', parse_mode='Markdown')
            return 'name'

    def name(self, bot, update):
        user_data = update.message.text.replace(', ',',').split(',')
        if len(user_data) == 3: # введены все данные
            surname, name, gruppa = user_data
            user_id = self.chats[update.message.chat_id][0]
            self.users[user_id].append(name)
            self.chats[update.message.chat_id].append(name)

            if gruppa == self.teacher_key: # препод
                db.add_teacher(user_id, surname, name)
                self.teachers[update.message.chat_id] = user_id
                menu = self.teacher_menu
            else:
                db.add_student(user_id, surname, name, gruppa)
                menu = self.student_menu
            bot.sendMessage(chat_id=update.message.chat_id, text='Отлично, {} ({})! Что бы Вы хотели сделать?'.format(self.chats[update.message.chat_id][1], self.chats[update.message.chat_id][0]), reply_markup=menu)
            return ConversationHandler.END
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text='Неправильные данные!\n*Если Вы студент:* введите фамилию, имя и группу через запятую в формате "Фамилия, Имя, группа".\n_Пример: Иванов, Иван, 15ФПЛ_\n*Если Вы преподаватель:* введите фамилию, имя и ключ доступа через запятую в формате "Фамилия, Имя Отчество, ключ доступа".\n_Пример: Иванов, Иван Иванович, key_', parse_mode='Markdown')
            return 'name'



    def handle_message(self, bot, update):
        print("Received", update.message, '\n')
        print(update)

        if update.message.chat_id not in self.chats: # пользователь ещё не зарегался
            bot.sendMessage(chat_id=update.message.chat_id, text='Введите команду /start, чтобы начать работу.')
            return ConversationHandler.END
        else:
            timetable_list = db.list_timetable()
            timetable_markup = [[InlineKeyboardButton('{}, {} {}\nМест: {}'.format(lesson[0].capitalize(), lesson[1], lesson[2], lesson[3]), callback_data=lesson[4])] for lesson in timetable_list]
            timetable = InlineKeyboardMarkup(timetable_markup)

            open_list = db.list_open()
            open_markup = [[InlineKeyboardButton('{}, {} {}\nМест: {}'.format(lesson[0].capitalize(), lesson[1], lesson[2], lesson[3]), callback_data=lesson[4])] for lesson in open_list]
            open_timetable = InlineKeyboardMarkup(open_markup)


            if update.message.text.lower() == 'расписание':
                print(timetable_list)
                lessons = '*Расписание:*'
                if timetable_list: # если есть занятия
                    for les in timetable_list: # добавляем строчки с уроками
                        lesson = '\n`— {}, {} {}. Осталось мест: {}`'.format(les[0].capitalize(), les[1], les[2], les[3])
                        #print(lesson)
                        lessons = lessons+lesson
                else:
                    lessons = 'Пока на эту неделю не назначено ни одного занятия.'
                print(lessons)
                bot.sendMessage(chat_id=update.message.chat_id, parse_mode='Markdown', text=lessons)
                #TODO: сделать разметку
                return ConversationHandler.END


            elif update.message.text.lower() == 'создать занятие':
                if update.message.chat_id in self.teachers:
                    bot.sendMessage(chat_id=update.message.chat_id, text='Введите занятие в формате "Занятие, день недели, время, количество мест"\n_Пример: Силовая тренировка, понедельник, 17-00, 20_', parse_mode='Markdown')
                    return 'create'
                    #TODO: проверять, есть ли на это время уже занятия
                else:
                    bot.sendMessage(chat_id=update.message.chat_id, text='Только преподаватели могут создавать занятие.')
                    return ConversationHandler.END


            elif update.message.text.lower() == 'отменить занятие':
                if update.message.chat_id in self.teachers:
                    if timetable_list: # если уже есть занятия
                        bot.sendMessage(chat_id=update.message.chat_id, text='Какое занятие Вы хотите отменить?', reply_markup=timetable)
                        return 'cancel'
                    else:
                        bot.sendMessage(chat_id=update.message.chat_id, text='Пока что на эту неделю не назначено ни одного занятия.')
                        return ConversationHandler.END
                else:
                    bot.sendMessage(chat_id=update.message.chat_id, text='Только преподаватели могут отменять занятие.')
                    return ConversationHandler.END


            elif update.message.text.lower() == 'сброс расписания':
                if update.message.chat_id in self.teachers:
                    if timetable_list: # если уже есть занятия
                        db.reset_timetable()
                        bot.sendMessage(chat_id=update.message.chat_id, text='Расписание было сброшено.')
                        return ConversationHandler.END
                    else:
                        bot.sendMessage(chat_id=update.message.chat_id, text='Пока что на эту неделю не назначено ни одного занятия.')
                        return ConversationHandler.END
                else:
                    bot.sendMessage(chat_id=update.message.chat_id, text='Только преподаватели могут сбрасывать расписание.')
                    return ConversationHandler.END


            elif update.message.text.lower() == 'записаться':
                print(self.teachers)
                if update.message.chat_id not in self.teachers:
                    if open_list: # есть свободные места
                        bot.sendMessage(chat_id=update.message.chat_id, text='На какое занятие Вы хотите записаться?', reply_markup=open_timetable)
                        print(open_list)
                        return 'enrol'
                    elif not timetable_list: # вообще нет занятий
                        bot.sendMessage(chat_id=update.message.chat_id, text='Пока что на эту неделю не назначено ни одного занятия.')
                        return ConversationHandler.END
                    else: # нет свободных мест
                        bot.sendMessage(chat_id=update.message.chat_id, text='К сожалению, сейчас ни на одно занятие нет свободных мест.')
                        return ConversationHandler.END
                else:
                    bot.sendMessage(chat_id=update.message.chat_id, text='Только студенты могут записатся на занятие.')
                    return ConversationHandler.END


            elif update.message.text.lower() == 'отписаться':
                print(self.teachers)
                if update.message.chat_id not in self.teachers:
                    user_timetable_list = [db.get_lesson(lesson_id) for lesson_id in db.user_lessons(self.chats[update.message.chat_id][0])]
                    print(user_timetable_list)
                    if user_timetable_list: # если пользователь на что-то записан
                        user_timetable_markup = [[InlineKeyboardButton('{}, {} {}'.format(lesson[0].capitalize(), lesson[1], lesson[2]), callback_data=lesson[5])] for lesson in user_timetable_list]
                        user_timetable = InlineKeyboardMarkup(user_timetable_markup)
                        bot.sendMessage(chat_id=update.message.chat_id, text='На какое занятие Вы хотите отменить запись?', reply_markup=user_timetable)
                        return 'canrol'
                    else:
                        bot.sendMessage(chat_id=update.message.chat_id, text='Пока что Вы не записаны ни на одно занятие.')
                        return ConversationHandler.END
                else:
                    bot.sendMessage(chat_id=update.message.chat_id, text='Только студены могут отменить запись на занятие.')
                    return ConversationHandler.END



            elif update.message.text.lower() == 'список':
                if timetable_list:
                    bot.sendMessage(chat_id=update.message.chat_id, text='Выберите занятие:', reply_markup=timetable)
                    return 'list'
                else:
                    bot.sendMessage(chat_id=update.message.chat_id, text='Пока на эту неделю не назначено ни одного занятия.')


            elif update.message.text.lower() == 'мои занятия':
                print(self.teachers)
                if update.message.chat_id not in self.teachers:
                    user_timetable_list = [db.get_lesson(lesson_id) for lesson_id in db.user_lessons(self.chats[update.message.chat_id][0])]
                    print(user_timetable_list)

                    lessons = '*Мои занятия:*'
                    if user_timetable_list: # если пользователь уже на что-то записан
                        for les in user_timetable_list: # добавляем строчки с занятиями
                            lesson = '`\n— {}, {} {}`'.format(les[0].capitalize(), les[1], les[2])
                            #print(lesson)
                            lessons = lessons+lesson
                    else:
                        lessons = 'Пока что Вы не записаны ни на одно занятие.'
                    print(lessons)
                    bot.sendMessage(chat_id=update.message.chat_id, parse_mode='Markdown', text=lessons)
                    #TODO: сделать разметку
                    return ConversationHandler.END
                else:
                    bot.sendMessage(chat_id=update.message.chat_id, text='Только студенты могут просматривать список своих занятий.')
                    return ConversationHandler.END


            else:
                update.message.reply_text('Команду распознать не удалось. Перенаправляю к инструкции...')
                self.help(bot, update)
                return ConversationHandler.END

    def create_lesson(self, bot, update):
        new_lesson = update.message.text.lower().replace(', ',',').split(',')
        print(new_lesson)
        if len(new_lesson) == 4 and new_lesson[3].isdigit(): # введены все параметры, последний -- число (размер группы)
            db.add_lesson(new_lesson[0], new_lesson[1], new_lesson[2], new_lesson[3])
            bot.sendMessage(chat_id=update.message.chat_id, text='Вы создали занятие {}, {} {}, с размером группы {} человек(а).'.format(new_lesson[0], new_lesson[1], new_lesson[2], new_lesson[3]))
            return ConversationHandler.END
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text='Неправильные данные! Пожалуйста, введите занятие в формате "Занятие, день недели, время, количество мест"\n_Пример: Силовая тренировка, понедельник, 17-00, 20_', parse_mode='Markdown')
            return 'create'

    def cancel_lesson(self, bot, update):
        query = update.callback_query
        lesson_id = query.data
        print(lesson_id)
        lesson = db.get_lesson(lesson_id)
        print(lesson)
        bot.sendMessage(chat_id=query.message.chat_id, text='Вы отменили занятие {}, {} {}. Все студенты, записавшиеся на это занятие, будут оповещены.'.format(lesson[0], lesson[1], lesson[2]))
        users = db.del_lesson(lesson_id)
        print(users)
        for user in users:
            if user in self.users: # если наш пользователь
                bot.sendMessage(chat_id=self.users[user][0], text='Занятие {}, {} {}, на которое Вы были записаны, отменено.'.format(lesson[0], lesson[1], lesson[2]))
        #TODO: можно ли рассылать не в цикле, а список давать?
        return ConversationHandler.END

    def enrol_for_lesson(self, bot, update):
        query = update.callback_query
        lesson_id = query.data
        print(lesson_id)
        lesson = db.get_lesson(lesson_id)
        print(lesson)
        user_id = self.chats[query.message.chat_id][0]
        users = db.list_lesson(lesson_id)
        if user_id in users: # уже на занятии
            bot.sendMessage(chat_id=query.message.chat_id, text='Вы уже записаны на занятие {}, {} {}. Хорошей тренировки!'.format(lesson[0], lesson[1], lesson[2]))
        else:
            db.add_to_lesson(lesson_id, user_id)
            bot.sendMessage(chat_id=query.message.chat_id, text='Вы записались на занятие {}, {} {}. Хорошей тренировки!'.format(lesson[0], lesson[1], lesson[2]))
            #TODO: добавлять в группу ожидания
            #except:
            #    bot.sendMessage(chat_id=query.message.chat_id, text='К сожалению, места на это занятие уже кончились.')
        return ConversationHandler.END

    def cancel_enrolment(self, bot, update):
        query = update.callback_query
        lesson_id = query.data
        print(lesson_id)
        lesson = db.get_lesson(lesson_id)
        print(lesson)
        db.del_from_lesson(lesson_id, self.chats[query.message.chat_id][0])
        bot.sendMessage(chat_id=query.message.chat_id, text='Вы отменили запись на занятие {}, {} {}. Приходите ещё!'.format(lesson[0], lesson[1], lesson[2]))
        return ConversationHandler.END

    def list_lesson(self, bot, update):
        query = update.callback_query
        lesson_id = query.data
        print(lesson_id)
        lesson = db.get_lesson(lesson_id)
        print(lesson)
        user_ids = db.list_lesson(lesson_id)
        users = db.list_them(user_ids)
        print(users)
        if users: # если кто-то уже записан
            user_list = ''
            for i, user in enumerate(users):
                user_list+='`{}) {} {}, {}`\n'.format(i+1, user[0], user[1], user[2])
            user_list+='`\nОсталось мест: {}`'.format(lesson[4])
            print(user_list)
        else:
            user_list = 'На занятие пока никто не записан.'
        bot.sendMessage(chat_id=query.message.chat_id, parse_mode='Markdown', text='*{}, {} {} ({} чел.):*\n{}'.format(lesson[0].capitalize(), lesson[1], lesson[2], lesson[3], user_list))
        #TODO: сделать разметку
        return ConversationHandler.END



if __name__ == "__main__":
    print('Работаем!\n')
    bot = Bot(token)
    bot.updater.start_polling()
'''
while True: # отслеживаем время
    now = datetime.datetime.now()
    #print(now)
    if now.isoweekday() == 7 and now.hour == 0 and now.minute == 0 and now.second == 0: # воскресенье 00:00:00
        print(now)
        db.reset_timetable()
        print('Сброс расписания...')
'''
