# Telegram: https://t.me/AlexUstas0

import winsound
import time
import view
import history
import model_fl as fl
import model_habr as habr
import model_freelance as free

import telebot
import bot_token
from telebot import types
# Name: AlexFreelance
# Bot name: alex_freelance_bot


bot = telebot.TeleBot(bot_token.TOKEN)
description = """
Бот предназначен для обработки фриланс
сервисов для поиска задач по
ключевым словам.
Список ключевых слов: [/keywords]
Запустить поиск задач: [/go]
Можно просмотреть последние
5 задач: [/history]
Информация по заданию: [/task] *id* 
Сайты:
[FL](https://www.fl.ru/projects/)
[Habr](https://freelance.habr.com/tasks)
[Kwork](https://kwork.ru/projects)
[Freelance](https://freelance.ru/project/search)
Эта справка: [/help]"""


def beep_beep():
    """Alarm"""
    winsound.Beep(2000, 200)
    time.sleep(0.1)
    winsound.Beep(2000, 200)
    time.sleep(0.1)
    winsound.Beep(1500, 400)


@bot.message_handler(commands=['start', 'help'])
def bot_description(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    itembtn1 = types.KeyboardButton('/help')
    itembtn2 = types.KeyboardButton('/go')
    itembtn3 = types.KeyboardButton('/keywords')
    itembtn4 = types.KeyboardButton('/history')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(message.chat.id, description, parse_mode='Markdown', reply_markup=markup)


@bot.message_handler(commands=['keywords'])
def get_keywords(message):
    word_list = view.get_keywords()
    bot.send_message(message.chat.id, 'Список ключевых слов:\n' + word_list)


@bot.message_handler(commands=['go'])
def run_parser(message):
    new_tasks = dict()
    # - - id (key)
    # 0 - service (fl, kwork, habr)
    # 1 - task name
    # 2 - detail description
    # 3 - cost
    # 4 - time
    # 5 - responses
    # 6 - customer
    dict_habr = dict()
    dict_fl = dict()
    dict_free = dict()
    i = 0.5
    while True:
        dict_habr, new_tasks = habr.parse_habr(dict_habr, new_tasks)
        dict_fl, new_tasks = fl.parse_fl(dict_fl, new_tasks)
        dict_free, new_tasks = free.parse_freelance(dict_free, new_tasks)
        if len(new_tasks):
            beep_beep()
            view.show_tasks(new_tasks)
            view.show_for_bot(bot, message, new_tasks)
            history.write_tasks(new_tasks)
        if int(i) % 5 == 0 and i - int(i) == 0:
            print(int(i), 'мин.')
        i += 0.5
        time.sleep(30)
        new_tasks = dict()


@bot.message_handler(commands=['history'])
def get_history(message):
    tasks = history.get_history(5)
    bot.send_message(message.chat.id, f'Последние *{len(tasks)}* задач:', parse_mode='Markdown')
    view.show_for_bot(bot, message, tasks)


@bot.message_handler(commands=['task'], content_types=['text'])
def get_task(message):
    text = message.text.split()
    if len(text) == 1:
        bot.reply_to(message, 'Для получения информации укажите *id* задания', parse_mode='Markdown')
    else:
        task = history.get_task(text[1])
        if task:
            view.show_for_bot(bot, message, task)
        else:
            bot.reply_to(message, f'Задание *{text[1]}* не найдено', parse_mode='Markdown')


bot.infinity_polling()
