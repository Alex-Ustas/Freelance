# Bot handler

import common_lib as lib
import telebot
import bot_token
# Name: AlexFreelance
# Bot name: alex_freelance_bot

bot = telebot.TeleBot(bot_token.TOKEN)
description = """
Бот предназначен для обработки фриланс
сервисов для поиска задач по
ключевым словам.
Список ключевых слов: [/keywords]
Эта справка: [/help]"""


@bot.message_handler(commands=['start', 'help'])
def bot_description(message):
    bot.send_message(message.chat.id, description, parse_mode='Markdown')


@bot.message_handler(commands=['keywords'])
def bot_description(message):
    word_list = lib.KEYWORDS.replace(',', '\n')
    bot.send_message(message.chat.id, word_list)


bot.polling(non_stop=True)
