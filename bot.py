import telebot
import config
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_command(message: telebot.types.Message):
    text = 'Привет! Чтобы начать, введи название валюты, цену которой нужно узнать, ' \
           'затем название валюты, в которой нужно узнать цену и количество первой валюты ' \
           '(например: евро доллар 1).\nВведите команду /values, чтобы увидеть список доступных валют.'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values_command(message: telebot.types.Message):
    text = 'Доступные валюты: евро, доллар, рубль.'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text', ])
def convert_command(message: telebot.types.Message):
    try:
        base, quote, amount = message.text.split(' ')
        base = get_currency_code(base.lower())
        quote = get_currency_code(quote.lower())
        result = CryptoConverter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка: {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Стоимость {amount} {get_currency_name(base)} в {get_currency_name(quote)} равна {result:.2f}'
        bot.send_message(message.chat.id, text)


def get_currency_code(currency_name):
    return config.CURRENCY_CODES.get(currency_name)


def get_currency_name(currency_code):
    return config.CURRENCY_NAMES.get(currency_code)


bot.polling()