import command_system
import vkapi
import settings

def dog():
   # Получаем случайную картинку из паблика
   attachment = vkapi.get_random_wall_picture(-119071337, settings.access_token)
   message = 'На тебе пёселя!\nВ следующий раз пришлю другого пёселя :)'
   vkapi.to_drive(attachment)
   message += '\n\nЗагрузил пёселя на диск!'
   return message, attachment

dog_command = command_system.Command()

dog_command.keys = ['собака', 'пёс', 'пес', 'собакен','песель', 'пёсель', 'щенок', 'псина', 'dog', 'dawg', 'puppy']
dog_command.description = 'Пришлю картинку с щеночком и запишу её на сервер ( ͡° ͜ʖ ͡°)'
dog_command.process = dog