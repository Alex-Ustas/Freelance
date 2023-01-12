# Store every record for tasks in history.csv file
# Handle file with keywords

import os
from datetime import datetime as dt

LOG_FILE = 'history.csv'
KEYWORDS = 'keywords.txt'


def write_tasks(tasks: dict):
    """Write tasks to file"""
    if os.path.exists(LOG_FILE):
        file = open(LOG_FILE, 'a', encoding='utf-8')
    else:
        file = open(LOG_FILE, 'w', encoding='utf-8')
    old_tasks = get_history()
    for key, data in tasks.items():
        old = old_tasks.get(key, None)
        if old is None:
            line = dt.now().strftime('%d.%m.%y %H:%M:%S') + ';' + key
            for item in data:
                line += ';' + item.replace(';', '$$$')
            file.write(line + '\n')
    file.close()


def get_history(tasks_num=-1) -> dict:
    """Get all tasks from history file"""
    tasks = dict()
    if not os.path.exists(LOG_FILE):
        return tasks
    with open(LOG_FILE, 'r', encoding='utf-8') as file:
        all_lines = file.readlines()
    if len(all_lines):
        start_line = 0 if tasks_num == -1 else len(all_lines) - tasks_num
        start_line = 0 if start_line < 0 else start_line
        for line in all_lines[start_line:len(all_lines)]:
            line = line.replace('\n', '')
            items = line.split(';')
            items = [item.replace('$$$', ';') for item in items]
            tasks[items[1]] = [items[2], items[3], items[4], items[5], 'Дата/время: ' + items[0],
                               items[7], items[8], items[9], items[10]]
    return tasks


def get_task(task_id: str) -> dict:
    """Get one task from history file"""
    task = dict()
    if not os.path.exists(LOG_FILE):
        return task
    with open(LOG_FILE, 'r', encoding='utf-8') as file:
        all_lines = file.readlines()
    for line in all_lines:
        line = line.replace('\n', '')
        items = line.split(';')
        items = [item.replace('$$$', ';') for item in items]
        if items[1] == task_id:
            task[items[1]] = [items[2], items[3], items[4], items[5], 'Дата/время: ' + items[0],
                              items[7], items[8], items[9], items[10]]
            break
    return task


def get_keywords() -> list:
    """Get keywords from file"""
    if not os.path.exists(KEYWORDS):
        return list()
    with open(KEYWORDS, 'r', encoding='utf-8') as file:
        keyword = file.readline()
    return keyword.replace('\n', '').split(',')


def change_keywords(word: str, action: str) -> str:
    """Add/delete keyword in file"""
    result = ''
    keywords = get_keywords()
    action = action.strip().lower()
    word = word.strip().lower()
    if action == 'add':
        if word in keywords:
            result = f'Слово {word} уже есть в списке'
        else:
            keywords.append(word)
    elif action == 'del':
        if word in keywords:
            keywords.remove(word)
        else:
            result = f'Слово {word} не найдено, удаление невозможно'
    else:
        result = 'Операция не определена'
    if result == '':
        with open(KEYWORDS, 'w', encoding='utf-8') as file:
            file.write(','.join(keywords))
    return result
