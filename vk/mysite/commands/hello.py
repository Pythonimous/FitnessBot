import command_system

def hello():
   message = 'И тебе доброго здравия!\nЯ новый чат-бот.'
   return message, ''

hello_command = command_system.Command()

hello_command.keys = ['привет', 'hello', 'дратути', 'здравствуй', 'здравствуйте']
hello_command.description = 'Поприветствую тебя!'
hello_command.process = hello