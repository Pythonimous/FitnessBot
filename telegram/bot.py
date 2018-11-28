import random
import db_sqlite
from telegram.ext import Filters
from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler
from telegram.ext import Updater
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.message import Message

token='764336853:AAHHE0kNv9m95kUnCt5xmsX2w2av9LwTnaw'

class Bot():

    def __init__(self, token):
        self.chats = {} # chat_id: user_id
        self.users = {} # user_id: chat_id

        self.updater = Updater(token=token)  # заводим апдейтер
        self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
        self.updater.dispatcher.add_handler(CommandHandler('history', self.history))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self.handle_message))  # обработчик сообщений
        self.updater.dispatcher.add_handler((CallbackQueryHandler(self.button)))


    menu_markup = [[KeyboardButton('Расписание'), KeyboardButton('Список')],
                    [KeyboardButton('Записаться'), KeyboardButton('Отписаться')]]
    menu = ReplyKeyboardMarkup(menu_markup, resize_keyboard=True, one_time_keyboard=True)

    timetable_markup = [[InlineKeyboardButton('Занятие 1', callback_data='1'),
                     InlineKeyboardButton('Занятие 2', callback_data='2')]]
    timetable = InlineKeyboardMarkup(timetable_markup)

    timetable_html = '<h1 align="center">Расписание</h1><ul> {} </ul>'
    lesson_html = '<li>{}, {} {}. Осталось мест: {}'


    def start(self, bot, update):
        if update.message.chat_id in self.chats: # чат не новый
            print('users\t', self.users)
            print('chats\t', self.chats)
            bot.sendMessage(chat_id=update.message.chat_id, text='Здравствуйте, {}! Что бы вы хотели сделать?'.format(self.chats.get(update.message.chat_id)), reply_markup=self.menu)
        else:
            update.message.reply_text('Здравствуйте! Похоже, Вы у нас впервые. Я присвою Вам id -- пожалуйста, запомните его, чтобы мой брат в ВК мог узнать Вас.')
            #user_ids = (id[0] for id in db_sqlite.list_all()) # кто есть в базе
            #print('users in base\t', user_ids)
            user_id = random.randint(1000, 9999) # четырёхзначное число
            #while user_id in user_ids:
            #    user_id = random.randint(1000, 9999)
            self.chats[update.message.chat_id] = user_id
            self.users[user_id] = update.message.chat_id
            update.message.reply_text('{}'.format(user_id))


    def button(self, bot, update):
        print('Button!')
        query = update.callback_query
        print(query)
        bot.sendMessage(chat_id=query.message.chat_id, text='Выбрано {}'.format(query.data))
        print('button', query.data)

    def handle_message(self, bot, update):
        print("Received", update.message, '\n')
        print(update)

        if update.message.text.lower() == 'расписание':
            #bot.sendMessage(chat_id=update.message.chat_id, text='HTML')
            timetable = db_sqlite.list_timetable()
            lessons = ''
            for l in timetable: # добавляем строчки с уроками
                lessons = lessons+self.lesson_html.format(l[0], l[1], l[2], l[3])
            bot.sendMessage(chat_id=update.message.chat_id, parse_mode='HTML', text=self.timetable_html.format(lessons))


        elif update.message.text.lower() == 'записаться':
            bot.sendMessage(chat_id=update.message.chat_id, text='Выберите занятие:', reply_markup=self.timetable)

        elif update.message.text.lower() == 'отписаться':
            bot.sendMessage(chat_id=update.message.chat_id, text='Выберите занятие:', reply_markup=self.timetable)

        elif update.message.text.lower() == 'список':
            bot.sendMessage(chat_id=update.message.chat_id, text='Выберите занятие:', reply_markup=self.timetable)

        elif update.message.text.lower() == 'sql':
            bot.sendMessage(chat_id=update.message.chat_id, text='Подключаюсь к sql...')
            data = db_sqlite.list_all()
            print(data)
            bot.sendMessage(chat_id=update.message.chat_id, text='{}'.format(data))


        else:
            bot.sendMessage(chat_id=update.message.chat_id, text='Ась?', reply_markup=self.menu)


    def spec_mess(self, bot, update):
        message = input('Сообщение: ')
        chat_id=update.message.chat_id
        text=update.message.text
        return chat_id, text, message

    def history(bot):
        print('history')
        for update in bot.get_updates():
            print(update)


if __name__ == "__main__":
    print('Работаем!\n')
    bot = Bot(token)
    bot.updater.start_polling()
