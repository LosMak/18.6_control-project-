import telebot
from config import TOKEN, keys
from utils import CurrencyConverter, ConvertException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def function_name(message: telebot.types.Message):
    bot.send_message(message.chat.id, f'Здравствуйте,\t {message.chat.first_name}!')
    bot.send_message(message.chat.id, 'Воспользуйтесь подсказками бота /help')


@bot.message_handler(commands=['help'])
def start_help(message: telebot.types.Message):
    text = 'Для начала работы введите текст в следующем формате:\n' \
           '<Валюта, которую хотите поменять>\n <Валюта, которую хотите купить>\n' \
           '<Количество валюты>\n' \
           'Посмотреть список доступных валют: /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values_ = message.text.split(' ')
        if len(values_) > 3:
            raise ConvertException('Не нужно вводить столько данных!\nВведите только 3 параметра!')

        if len(values_) < 3:
            raise ConvertException('Вы что-то забыли указать!')
        origin_cur, target_cur, amount = values_
        origin_cur = origin_cur.lower()
        target_cur = target_cur.lower()
        rate = CurrencyConverter.currency_convert(origin_cur, target_cur, amount)
    except ConvertException as e:
        bot.reply_to(message, e)
    except Exception as e:
        bot.reply_to(message, f'Ошибка!\n Не удалось обработать команду\n {e}')
    else:
        text = f'{amount} {origin_cur} равно {round(rate * int(amount))} {target_cur}'
        bot.send_message(message.chat.id, text)


bot.polling()
