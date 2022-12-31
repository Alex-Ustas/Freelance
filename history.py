# Store every record for tasks in history.csv file
import os
from datetime import datetime as dt

LOG_FILE = 'history.csv'


def write_tasks(tasks: dict):
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
    tasks = dict()
    with open(LOG_FILE, 'r', encoding='utf-8') as file:
        all_lines = file.readlines()
    if len(all_lines):
        start_line = 0 if tasks_num == -1 else len(all_lines) - tasks_num
        start_line = 0 if start_line < 0 else start_line
        end_line = len(all_lines)
        for line in all_lines[start_line:end_line]:
            line = line.replace('\n', '')
            items = line.split(';')
            items = [item.replace('$$$', ';') for item in items]
            tasks[items[1]] = [items[2], items[3], items[4], items[5], 'Дата/время: ' + items[0], items[7], items[8]]
    return tasks
