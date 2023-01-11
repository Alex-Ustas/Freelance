# Telegram: https://t.me/AlexUstas0

import winsound
import time
import view
import history
import model_fl as fl
import model_habr as habr
import model_freelance as free
import common_lib as lib

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


def check_new_tasks(all_tasks: dict, check_tasks: dict) -> (dict, int):
    new = 0
    for key, task in check_tasks.items():
        if key not in all_tasks.keys():
            for word in lib.KEYWORDS.split(','):
                if word in task[1].lower() or word in task[2].lower():
                    item = [task[i] for i in range(0, 8)]
                    item.append('y')
                    all_tasks[key] = item
                    new = 1
    return all_tasks, new


@bot.message_handler(commands=['start', 'help'])
def bot_description(message):
    """Show help for bot using and add buttons"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    itembtn1 = types.KeyboardButton('/help')
    itembtn2 = types.KeyboardButton('/go')
    itembtn3 = types.KeyboardButton('/keywords')
    itembtn4 = types.KeyboardButton('/history')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)
    bot.send_message(message.chat.id, description, parse_mode='Markdown', reply_markup=markup)


@bot.message_handler(commands=['keywords'])
def get_keywords(message):
    """Show keywords"""
    word_list = view.get_keywords()
    bot.send_message(message.chat.id, 'Список ключевых слов:\n' + word_list)


@bot.message_handler(commands=['go'])
def run_parser(message):
    """Parse platforms and show new tasks"""
    all_tasks = history.get_history()
    # - - id (key)
    # 0 - platform (fl, kwork, habr, freelance)
    # 1 - task name
    # 2 - detail description
    # 3 - cost
    # 4 - time
    # 5 - responses
    # 6 - customer/term
    # 7 - link
    # 8 - flag for new task (y/n)
    i = 0.5
    while True:
        tasks, err1 = habr.parse_habr()
        all_tasks, new1 = check_new_tasks(all_tasks, tasks)

        tasks, err2 = fl.parse_fl()
        all_tasks, new2 = check_new_tasks(all_tasks, tasks)

        tasks, err3 = free.parse_freelance()
        all_tasks, new3 = check_new_tasks(all_tasks, tasks)

        new = new1 + new2 + new3
        error = err1 + err2 + err3
        if new:
            beep_beep()
            view.show_tasks(all_tasks)
            view.show_for_bot(bot, message, all_tasks)
            for key in all_tasks.keys():
                all_tasks[key][8] = 'n'
            history.write_tasks(all_tasks)
        if error:
            beep_beep()
            view.show_error(bot, message, error)
        if int(i) % 5 == 0 and i - int(i) == 0:
            print(int(i), 'мин.')
        i += 0.5
        time.sleep(30)


@bot.message_handler(commands=['history'])
def get_history(message):
    """Get several last tasks from file"""
    tasks = history.get_history(5)
    bot.send_message(message.chat.id, f'Последние *{len(tasks)}* задач:', parse_mode='Markdown')
    view.show_for_bot(bot, message, tasks, False)


@bot.message_handler(commands=['task'], content_types=['text'])
def get_task(message):
    """Get task by id from file"""
    text = message.text.split()
    if len(text) == 1:
        bot.reply_to(message, 'Для получения информации укажите *id* задания', parse_mode='Markdown')
    else:
        task = history.get_task(text[1])
        if task:
            view.show_for_bot(bot, message, task, False)
        else:
            bot.reply_to(message, f'Задание *{text[1]}* не найдено', parse_mode='Markdown')


bot.infinity_polling()
