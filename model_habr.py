# Парсинг freelance.habr.com

import requests as rq
import common_lib as lib
import html2text as ht


# ------------------------------------------------------------------------------------------- Habr freelance
def parse_task_habr(text: str) -> (str, str):
    n1 = text.find('[')
    n2 = text.find(']')
    temp = text.split('/tasks/')
    task_id = '0'
    if len(temp) > 1:
        task_id = temp[len(temp)-1][:-1]
    task = '[Task not detected]' if n1 == 0 or n2 == 0 else text[n1 + 1:n2].strip()
    return task, task_id


def parse_response_habr(text: str):
    nums = text.split('_')
    selected = True
    ago = list()
    response = 0
    view = 0
    if len(nums) == 3:
        response = 0
        view = nums[1] if 'просмотр' in text else 0
        ago = nums[2].strip().split()
    elif len(nums) > 3:
        response = nums[1] if 'отклик' in text else 0
        view = nums[3] if 'просмотр' in text else 0
        ago = nums[4].strip().split()
    else:
        selected = False
    if selected:
        ago.pop(0)
        ago = ' '.join(ago)
        return int(response), int(view), ago
    else:
        return 0, 0, text.strip()


def parse_habr(habr_dict: dict, new_tasks: dict, method=1) -> (dict, dict):
    """Parse habr.com"""
    keyword = lib.KEYWORDS.split(',')
    if method == 1:
        s = rq.get('https://freelance.habr.com/tasks')
        text = ht.html2text(s.text)
    else:
        html = open(r'C:\Temp\Python\habr_html.txt', encoding='utf8').read()
        text = ht.html2text(html)
    text = text.split('\n')

    # Generate dictionary
    nchar = 0
    while True:
        stop = False
        while '/tasks/' not in text[nchar]:
            if '<- Сюда' in text[nchar]:
                stop = True
                break
            nchar += 1
        if stop:
            break

        task, task_id = parse_task_habr(text[nchar])
        new_task = habr_dict.get(task_id, '_New_')
        new_task = True if new_task == '_New_' else False
        response, view, ago = parse_response_habr(text[nchar + 2])
        nchar += 3

        while 'руб.' not in text[nchar] and 'договорная' not in text[nchar]:
            nchar += 1
        if 'руб.' in text[nchar]:
            cash = text[nchar]
            cash = cash[0:cash.find('руб.')].replace(' ', '')
        else:
            cash = 'договорная'
        habr_dict[task_id] = [task, new_task, response, view, ago, cash]

    # Check new projects
    for key, data_list in habr_dict.items():
        for word in keyword:
            if word in data_list[0].lower():
                if data_list[1]:
                    cost = 'договорная' if data_list[5] == 'договорная' else "{:,.0f}".format(int(data_list[5]))
                    new_tasks[key] = ['Habr', data_list[0], '', cost, data_list[4], str(data_list[2]), '']
                break

    return habr_dict, new_tasks


if __name__ == '__main__':
    dummy = parse_habr(dict(), dict(), 0)
