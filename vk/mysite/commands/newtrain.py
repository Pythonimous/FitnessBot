import command_system

def new():
    message = 'Создам для вас новое занятие.\nВведите запрос следующего вида: занятие (название) дата время. Например: "занятие (тренажерный зал) 12.09.18 14:00".'
    return message, ''

new_command = command_system.Command()

new_command.keys = ['занятие']
new_command.description = 'Создам новое занятие'
new_command.process = new