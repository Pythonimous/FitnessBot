from telegram.ext import Filters
from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler
from telegram.ext import Updater
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.message import Message
import drive

token='764336853:AAHHE0kNv9m95kUnCt5xmsX2w2av9LwTnaw'

class Bot():

    def __init__(self, token):
        self.users = {}

        self.updater = Updater(token=token)  # заводим апдейтер
        self.updater.dispatcher.add_handler(CommandHandler('start', self.start))
        self.updater.dispatcher.add_handler(CommandHandler('name', self.name))
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text, self.handle_message))  # обработчик сообщений
        self.updater.dispatcher.add_handler((CallbackQueryHandler(self.button)))

    menu_markup = [[KeyboardButton('Расписание'), KeyboardButton('Список')],
                    [KeyboardButton('Записаться'), KeyboardButton('Отписаться')]]
    menu = ReplyKeyboardMarkup(menu_markup, resize_keyboard=True, one_time_keyboard=True)


    timetable_markup = [[InlineKeyboardButton('Занятие 1', callback_data='1'),
                     InlineKeyboardButton('Занятие 2', callback_data='2')]]
    timetable = InlineKeyboardMarkup(timetable_markup)

    timetable_html = '<b>Расписание:</b>\nЗанятие 1\nЗанятие 2'


    def start(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text='Здравствуйте! Что бы вы хотели сделать?', reply_markup=self.menu)

    def name(self, bot, update):
        print('Received', update.message)
        id, text, mess = self.spec_mess(bot, update)
        print(id, '\n')
        print(text, '\n')
        print(mess)
        bot.sendMessage(chat_id=id, text='text: {}\n message: {}'.format(text, mess))

        '''
        bot.sendMessage(chat_id=update.message.chat_id, text='Представьтесь, пожалуйста:')
        #print('text', update.message.text)
        print('reply', Message.reply_to_message)
        print('forward from', Message.forward_from)
        print('text', Message.text)
        print('rep text', Message.reply_text((update.message)))
        #self.users[update.message.chat_id] = update.message.username
        #print()
        #print('Users:', self.users)
        '''


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
            bot.sendMessage(chat_id=update.message.chat_id, parse_mode='HTML', text=self.timetable_html)

        elif update.message.text.lower() == 'записаться':
            bot.sendMessage(chat_id=update.message.chat_id, text='Выберите занятие:', reply_markup=self.timetable)

        elif update.message.text.lower() == 'отписаться':
            bot.sendMessage(chat_id=update.message.chat_id, text='Выберите занятие:', reply_markup=self.timetable)

        elif update.message.text.lower() == 'список':
            bot.sendMessage(chat_id=update.message.chat_id, text='Выберите занятие:', reply_markup=self.timetable)

        elif update.message.text.lower() == 'файл':
            open('file.txt', 'w').write('Hello!')
            drive.to_drive('file.txt')
            bot.sendMessage(chat_id=update.message.chat_id, text='Success!')


        else:
            bot.sendMessage(chat_id=update.message.chat_id, text='Ась?', reply_markup=self.menu)


    def spec_mess(self, bot, update):
        message = input('Сообщение: ')
        chat_id=update.message.chat_id
        text=update.message.text
        return chat_id, text, chat_id



if __name__ == "__main__":
    print('Работаем!\n')
    bot = Bot(token)
    bot.updater.start_polling()
