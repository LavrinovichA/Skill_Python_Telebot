import telebot
import config
from extensions import CryptoCompareAPI, APIException, keys

bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_instructions(message):
    instructions = f'<b>Добрый день, {message.from_user.first_name} {message.from_user.last_name}!</b>\n\nЯ телеграмм бот для просмотра курсов валют.\nДля повтора этого сообщения, наберите команду /start.\nДля справки наберите /help.\nДля того чтобы увидеть поддерживаемые валюты наберите /values.'
    bot.reply_to(message, instructions)

@bot.message_handler(commands=['help'])
def send_instructions(message):
    instructions = 'Для получения цены введите сообщение в формате: \n<имя валюты> <имя валюты в которой надо узнать цену первой валюты> <количество первой валюты>. \nДанные вводить через пробел \nДоступные валюты /values'
    bot.reply_to(message, instructions)

@bot.message_handler(commands=['values'])
def send_values(message):
    values = 'Доступные валюты:'
    for key in keys.keys():
        values = '\n- '.join((values, key, ))
    bot.reply_to(message, values)

@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    try:
        base, quote, amount = message.text.split(' ')
        result = CryptoCompareAPI.get_price(base.capitalize(), quote.capitalize(), float(amount))
        reply = f'{amount} {base.capitalize()} = {result} {quote.capitalize()}'
    except APIException as e:
        reply = f'Ошибка API: {str(e)}'
    except Exception as e:
        reply = f'Ошибка: {str(e)}'
    bot.reply_to(message, reply)

bot.polling()