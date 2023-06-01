# Telegram: https://t.me/AlexUstas0

# TODO:
#   + Add model_kwork
#   - Parse certain task with command /task <id> and change record in history for it
#   - Clear history from closed tasks
#   - Создать асинхронную обработку запросов
#   - Save logs for users which use bot (datetime, user id, user name, written text)

import view
import loader
import model_fl as fl
import model_habr as habr
import model_freelance as free
import model_kwork as kwork

import winsound
import time
import telebot
import bot_token

# Name: AlexFreelance
# Bot name: alex_freelance_bot


bot = telebot.TeleBot(bot_token.TOKEN)
description = """
Бот предназначен для обработки фриланс
сервисов для поиска задач по
ключевым словам.
----------------------------------------
Запустить поиск задач: [/go]
Список ключевых слов: [/keywords]
Последние 5 задач: [/history]
Информация по заданию: [/task] <id>
Информация по сайтам: [/sites]
Эта справка: [/help]"""


def beep_beep():
    """Alarm"""
    winsound.Beep(2000, 200)
    time.sleep(0.1)
    winsound.Beep(2000, 200)
    time.sleep(0.1)
    winsound.Beep(1500, 400)


def check_new_tasks(all_tasks: dict, check_tasks: dict) -> int:
    """Compare all tasks with parsed tasks to identify new tasks"""
    new = 0
    keywords = loader.get_keywords()
    for key, task in check_tasks.items():
        if key not in all_tasks.keys():
            for word in keywords:
                try:
                    if word in task[1].lower() or word in task[2].lower():
                        item = [task[i] for i in range(len(task))]
                        item.append('y')
                        all_tasks[key] = item
                        new = 1
                        break
                except Exception as err:
                    print(err)
                    print(key, task[1], task[2])
    return new


@bot.message_handler(commands=['start', 'help'])
def bot_description(message):
    """Show help for bot using and add buttons"""
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    button1 = telebot.types.KeyboardButton('/help')
    button2 = telebot.types.KeyboardButton('/go')
    button3 = telebot.types.KeyboardButton('/keywords')
    button4 = telebot.types.KeyboardButton('/sites')
    markup.add(button1, button2, button3, button4)
    bot.send_message(message.chat.id, description, parse_mode='Markdown', reply_markup=markup)


@bot.message_handler(commands=['keywords'], content_types=['text'])
def get_keywords(message):
    """Show, add, delete keywords"""
    text = message.text.split()
    word_list = loader.get_keywords()
    if len(text) < 3:
        text = '*Список ключевых слов:*\n' + '\n'.join(word_list)
        text += '\n\n*/keywords add <word>* - добавление слова'
        text += '\n*/keywords del <word>* - удаление слова'
        bot.send_message(message.chat.id, text, parse_mode='Markdown')
    else:
        result = loader.change_keywords(text[2], text[1])
        word_list = loader.get_keywords()
        text = '*Результат обработки:*\n' + '\n'.join(word_list)
        if result:
            text += f'\n\n*{result}*'
        bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(commands=['go'])
def run_parser(message):
    """Parse platforms and show new tasks"""
    all_tasks = loader.get_history()
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
        error = list('' for j in range(4))
        new = 0
        platform = loader.get_platform()

        tasks, error[0] = habr.parse_habr(platform['Habr'])
        new += check_new_tasks(all_tasks, tasks)

        tasks, error[1] = fl.parse_fl(platform['FL'])
        new += check_new_tasks(all_tasks, tasks)

        tasks, error[2] = free.parse_freelance(platform['Freelance'])
        new += check_new_tasks(all_tasks, tasks)

        tasks, error[3] = kwork.parse_kwork(platform['Kwork'])
        new += check_new_tasks(all_tasks, tasks)

        if new:
            beep_beep()
            view.show_tasks(all_tasks)
            view.show_for_bot(bot, message, all_tasks)
            for key in all_tasks.keys():
                all_tasks[key][8] = 'n'
            loader.save_tasks(all_tasks)

        error = ''.join(error)
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
    tasks = loader.get_history(5)
    bot.send_message(message.chat.id, f'Последние *{len(tasks)}* задач:', parse_mode='Markdown')
    view.show_for_bot(bot, message, tasks, False)


@bot.message_handler(commands=['task'], content_types=['text'])
def get_task(message):
    """Get task by id from file"""
    text = message.text.split()
    if len(text) == 1:
        bot.reply_to(message, 'Для получения информации укажите *id* задания', parse_mode='Markdown')
    else:
        task = loader.get_task(text[1])
        if task:
            view.show_for_bot(bot, message, task, False)
        else:
            bot.reply_to(message, f'Задание *{text[1]}* не найдено', parse_mode='Markdown')


@bot.message_handler(commands=['sites'])
def show_sites(message):
    """Show info about sites"""
    platform = loader.get_platform()
    info = '*Сайты:*\n'
    for name, param in platform.items():
        link = param['link']
        enable = '- *включен*' if param['enable'] == 'y' else '- _отключен_'
        info += f'[{name}]({link}) {enable}\n'
    info += '\nВключить/отключить парсинг сайта:\n[/enable] *<site> <y/n>*\n' + \
            'Включить/отключить парсинг всех сайтов: [/enable] *all <y/n>*'
    bot.send_message(message.chat.id, info, parse_mode='Markdown')


@bot.message_handler(commands=['enable'], content_types=['text'])
def enable_sites(message):
    """Enable/disable sites"""
    text = message.text.split()
    info = 'Включить/отключить парсинг сайта:\n[/enable] *<site> <y/n>*\n' + \
           'Включить/отключить парсинг всех сайтов: [/enable] *all <y/n>*'
    if len(text) == 1:
        bot.reply_to(message, info, parse_mode='Markdown')
    elif len(text) == 3:
        flag = text[2]
        if flag != 'y' and flag != 'n':
            info = 'Параметр должен быть *y* или *n*\n' + info
            bot.reply_to(message, info, parse_mode='Markdown')
        else:
            platform = loader.get_platform()
            done = False
            for name, param in platform.items():
                if text[1] == 'all':
                    loader.set_platform(name, 'enable', flag)
                    done = True
                elif text[1].lower() == name.lower():
                    loader.set_platform(name, 'enable', flag)
                    done = True
                    break
            if done:
                show_sites(message)
            else:
                bot.reply_to(message, f'Сайт *{text[1]}* не определен', parse_mode='Markdown')
    else:
        info = 'Неверная команда\n' + info
        bot.reply_to(message, info, parse_mode='Markdown')


bot.infinity_polling()
