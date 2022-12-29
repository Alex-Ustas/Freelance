import time
import view
import model_fl as fl
import model_habr as habr
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
Запустить поиск задач: [/go]
Эта справка: [/help]"""


@bot.message_handler(commands=['start', 'help'])
def bot_description(message):
    bot.send_message(message.chat.id, description, parse_mode='Markdown')


@bot.message_handler(commands=['keywords'])
def bot_description(message):
    word_list = lib.KEYWORDS.replace(",", "\n")
    bot.send_message(message.chat.id, 'Список ключевых слов:\n' + word_list)


@bot.message_handler(commands=['go'])
def bot_description(message):
    new_tasks = dict()
    # 0 - id (key)
    # 0 - service (fl, kwork, habr)
    # 1 - task name
    # 2 - detail description
    # 3 - cost
    # 4 - time
    # 5 - responses
    # 6 - customer
    dict_habr = dict()
    dict_fl = dict()
    i = 0.5
    while True:
        dict_habr, new_tasks = habr.parse_habr(dict_habr, new_tasks)
        dict_fl, new_tasks = fl.parse_fl(dict_fl, new_tasks)
        if len(new_tasks):
            view.show_tasks(new_tasks)
            view.show_for_bot(bot, message, new_tasks)
        if int(i) % 5 == 0 and i - int(i) == 0:
            print(int(i), 'мин.')
        i += 0.5
        time.sleep(30)
        new_tasks = dict()


bot.polling(non_stop=True)
