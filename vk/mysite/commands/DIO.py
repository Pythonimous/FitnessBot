import command_system
import vkapi
import settings

def cat():
   # Получаем случайную картинку из паблика
   attachment = vkapi.get_random_wall_picture(-119102645, settings.access_token)
   message = 'Держи котика!\nВ следующий раз пришлю другого котика :)'
   return message, attachment

cat_command = command_system.Command()

cat_command.keys = ['котик', 'кошка', 'кот', 'котенок', 'котяра', 'cat']
cat_command.description = 'Пришлю картинку с котиком ( ͡° ͜ʖ ͡°)'
cat_command.process = cat