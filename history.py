# Store every record for tasks in history.csv file
import os
from datetime import datetime as dt

LOG_FILE = 'history.csv'


def write_records(tasks: dict):
    if os.path.exists(LOG_FILE):
        file = open(LOG_FILE, 'a')
    else:
        file = open(LOG_FILE, 'w')
    old_tasks = get_history()
    for key, data in tasks.items():
        old = old_tasks.get(key, None)
        if old is None:
            line = dt.now().strftime('%d.%m.%y %H:%M:%S') + ';' + key
            for item in data:
                line += ';' + item.replace(';', '$$$')
            file.write(line + '\n')
    file.close()


def get_history() -> dict:
    with open(LOG_FILE, 'r', encoding='utf8') as file:
        lines = file.readline().split(';')
        tasks = dict()
        lines = [line.replace('$$$', ';') for line in lines]
        tasks[lines[1]] = [lines[2], lines[3], lines[4], lines[5], lines[0], lines[7], lines[8]]
        while lines:
            lines = file.readline().split(';')
            lines = [line.replace('$$$', ';') for line in lines]
            tasks[lines[1]] = [lines[2], lines[3], lines[4], lines[5], lines[0], lines[7], lines[8]]
        return tasks
