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

        self.updater = Updater(token=token)  # заводим апдейтер
        self.updater.dispatcher.add_handler(ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                'id':[MessageHandler(Filters.text, self.check_id)], # генерация и сопоставление по id
                'name':[MessageHandler(Filters.text, self.name)] # запоминание инфы о пользователе
            },
            fallbacks=[CommandHandler('stop', self.stop)]
        ))

        self.updater.dispatcher.add_handler(ConversationHandler(
            entry_points=[MessageHandler(Filters.text, self.handle_message)],

            states={
                'create': [MessageHandler(Filters.text, self.create_lesson)], #создать занятие
                'cancel': [CallbackQueryHandler(self.cancel_lesson)], # отменить занятие
                'enrol': [CallbackQueryHandler(self.enrol_for_lesson)], # записаться на занятие
                'canrol': [CallbackQueryHandler(self.cancel_enrolment)], # отменить запись
                'list': [CallbackQueryHandler(self.list_lesson)] # просмотреть список на занятие
            },
            fallbacks=[CommandHandler('stop', self.stop)]
        ))

    menu_markup = [[KeyboardButton('Расписание'), KeyboardButton('Список')],
                   [KeyboardButton('Записаться'), KeyboardButton('Отписаться')],
                   [KeyboardButton('Создать занятие'), KeyboardButton('Отменить занятие')]]
    menu = ReplyKeyboardMarkup(menu_markup, resize_keyboard=True, one_time_keyboard=True)

    teacher_markup = [[KeyboardButton('Расписание'), KeyboardButton('Список')],
                   [KeyboardButton('Создать занятие'), KeyboardButton('Отменить занятие')]]
    teacher_menu = ReplyKeyboardMarkup(teacher_markup, resize_keyboard=True, one_time_keyboard=True)

    student_markup = [[KeyboardButton('Расписание'), KeyboardButton('Список')],
                   [KeyboardButton('Записаться'), KeyboardButton('Отписаться')]]
    student_menu = ReplyKeyboardMarkup(student_markup, resize_keyboard=True, one_time_keyboard=True)


    def stop(self, bot, update):
        update.message.reply_text('Действие отменено.')
        return ConversationHandler.END


    def start(self, bot, update):
        if update.message.chat_id in self.chats: # чат не новый
            print('users\t', self.users)
            print('chats\t', self.chats)
            print('users in base\t', [user for user in db.list_all()])
            bot.sendMessage(chat_id=update.message.chat_id, text='Здравствуйте, {} ({})! Что бы вы хотели сделать?'.format(self.chats[update.message.chat_id][1], self.chats[update.message.chat_id][0]), reply_markup=self.menu)
            return ConversationHandler.END
        else:
            update.message.reply_text('Здравствуйте! Похоже, Вы у нас впервые. Я присвою Вам id -- пожалуйста, запомните его, чтобы мой брат в ВК мог узнать Вас. Или он Вам уже присвоен? Введите свой id или отправьте любое сообщение, чтобы получить его.')
            return 'id'

    def check_id(self, bot, update):
        answer = update.message.text
        if answer.isdigit(): # если ввели код
            print(answer)
            user = db.list_them([answer])[0]
            print(user)
            self.users[int(answer)] = [update.message.chat_id, (user[1])]
            self.chats[update.message.chat_id] = [int(answer), user[1]]
            print('users\t', self.users)
            print('chats\t', self.chats)
            bot.sendMessage(chat_id=update.message.chat_id, text='Здравствуйте, {} ({})! Что бы вы хотели сделать?'.format(self.chats[update.message.chat_id][1], self.chats[update.message.chat_id][0]), reply_markup=self.menu)
            return ConversationHandler.END
        else: # совсем новенький
            user_ids = [user[0] for user in db.list_all()] # кто есть в базе
            print('users in base\t', user_ids)
            user_id = random.randint(1000, 9999) # четырёхзначное число
            while user_id in user_ids:
                user_id = random.randint(1000, 9999)
            self.chats[update.message.chat_id] = [user_id]
            self.users[user_id] = [update.message.chat_id]
            update.message.reply_text('{}'.format(user_id))
            update.message.reply_text('Тогда представьтесь, пожалуйста. Введите фамилию, имя и группу в формате "Фамилия, Имя, группа"\nПример: Иванов, Иван, 15ФПЛ')
            return 'name'

    def name(self, bot, update):
        surname, name, gruppa = update.message.text.replace(' ','').split(',')
        user_id = self.chats[update.message.chat_id][0]
        self.users[user_id].append(name)
        self.chats[update.message.chat_id].append(name)
        db.add_user(user_id, surname, name, gruppa)
        bot.sendMessage(chat_id=update.message.chat_id, text='Отлично, {} ({})! Что бы вы хотели сделать?'.format(self.chats[update.message.chat_id][1], self.chats[update.message.chat_id][0]), reply_markup=self.menu)
        return ConversationHandler.END


    def handle_message(self, bot, update):
        print("Received", update.message, '\n')
        print(update)

        timetable_list = db.list_timetable()
        timetable_markup = [[InlineKeyboardButton('{}, {} {}'.format(lesson[0], lesson[1], lesson[2]), callback_data=lesson[4])] for lesson in timetable_list]
        timetable = InlineKeyboardMarkup(timetable_markup)

        if update.message.text.lower() == 'расписание':
            #bot.sendMessage(chat_id=update.message.chat_id, text='HTML')
            print(timetable_list)
            lessons = '*Расписание:*'
            for les in timetable_list: # добавляем строчки с уроками
                lesson = '\n- {}, {} {}. Осталось мест: {}'.format(les[0], les[1], les[2], les[3])
                #print(lesson)
                lessons = lessons+lesson
            print(lessons)
            bot.sendMessage(chat_id=update.message.chat_id, parse_mode='Markdown', text=lessons)
            return ConversationHandler.END

        elif update.message.text.lower() == 'создать занятие':
            bot.sendMessage(chat_id=update.message.chat_id, text='Введите занятие в формате "Занятие, день недели, время, количество мест"\nПример: Силовая тренировка, понедельник, 17-00, 20')
            return 'create'

        elif update.message.text.lower() == 'отменить занятие':
            bot.sendMessage(chat_id=update.message.chat_id, text='Какое занятие Вы хотите отменить?', reply_markup=timetable)
            return 'cancel'

        elif update.message.text.lower() == 'записаться':
            bot.sendMessage(chat_id=update.message.chat_id, text='На какое занятие Вы хотите записаться?', reply_markup=timetable)
            return 'enrol'

        elif update.message.text.lower() == 'отписаться':
            user_timetable_list = [db.get_lesson(lesson_id) for lesson_id in db.user_lessons(self.chats[update.message.chat_id][0])]
            print(user_timetable_list)
            user_timetable_markup = [[InlineKeyboardButton('{}, {} {}'.format(lesson[0], lesson[1], lesson[2]), callback_data=lesson[3])] for lesson in user_timetable_list]
            user_timetable = InlineKeyboardMarkup(user_timetable_markup)

            bot.sendMessage(chat_id=update.message.chat_id, text='На какое занятие Вы хотите отменить запись?', reply_markup=user_timetable)
            return 'canrol'

        elif update.message.text.lower() == 'список':
            bot.sendMessage(chat_id=update.message.chat_id, text='Выберите занятие:', reply_markup=timetable)
            return 'list'

        else:
            bot.sendMessage(chat_id=update.message.chat_id, text='Ась?', reply_markup=self.menu)


    def create_lesson(self, bot, update):
        new_lesson = update.message.text.lower().replace(' ','').split(',')
        print(new_lesson)
        db.add_lesson(new_lesson[0], new_lesson[1], new_lesson[2], new_lesson[3])
        bot.sendMessage(chat_id=update.message.chat_id, text='Вы создали занятие {}, {} {}, с размером группы {} человек(а).'.format(new_lesson[0], new_lesson[1], new_lesson[2], new_lesson[3]))
        return ConversationHandler.END

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
        db.add_to_lesson(lesson_id, self.chats[query.message.chat_id][0])
        bot.sendMessage(chat_id=query.message.chat_id, text='Вы записались на занятие {}, {} {}. Хорошей тренировки!'.format(lesson[0], lesson[1], lesson[2]))
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
        user_list = '*Список записавшихся на {}, {} {}:*\n'.format(lesson[0], lesson[1], lesson[2])
        for i, user in enumerate(users):
            user_list+='{}) {} {}, {}\n'.format(i+1, user[0], user[1], user[2])
        user_list+='---------------\nОсталось мест: {}'.format(lesson[4])
        print(user_list)
        bot.sendMessage(chat_id=query.message.chat_id, parse_mode='Markdown', text='На занятие {}, {} {} записаны пользователи:\n{}'.format(lesson[0], lesson[1], lesson[2], user_list))
        return ConversationHandler.END



if __name__ == "__main__":
    print('Работаем!\n')
    bot = Bot(token)
    bot.updater.start_polling()
