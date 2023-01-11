# Парсинг freelance.habr.com

import requests as rq
import html2text as ht


def parse_task_habr(text: str) -> (str, str):
    """Check task id and task name"""
    n1 = text.find('[')
    n2 = text.find(']')
    temp = text.split('/tasks/')
    task_id = '0'
    if len(temp) > 1:
        task_id = temp[len(temp)-1][:-1]
    title = '[Task not detected]' if n1 == 0 or n2 == 0 else text[n1 + 1:n2].strip()
    return title, task_id


def parse_response_habr(text: str) -> (int, int, str):
    nums = text.split('_')
    selected = True
    time = list()
    response = 0
    view = 0
    if len(nums) == 3:
        response = 0
        view = nums[1] if 'просмотр' in text else 0
        time = nums[2].strip().split()
    elif len(nums) > 3:
        response = nums[1] if 'отклик' in text else 0
        view = nums[3] if 'просмотр' in text else 0
        time = nums[4].strip().split()
    else:
        selected = False
    if selected:
        time.pop(0)
        time = ' '.join(time)
        return int(response), int(view), time
    else:
        return 0, 0, text.strip()


def parse_habr(method=1) -> (dict, str):
    """Parse habr.com"""
    data = dict()
    if method == 1:
        try:
            s = rq.get('https://freelance.habr.com/tasks')
            text = ht.html2text(s.text)
        except Exception as err:
            return data, f'Habr: unexpected {err=}, {type(err)=}\n'
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
            if nchar >= len(text):
                break
        if stop:
            break

        title, task_id = parse_task_habr(text[nchar])
        response, view, time = parse_response_habr(text[nchar + 2])
        nchar += 3

        while 'руб.' not in text[nchar] and 'договорная' not in text[nchar]:
            nchar += 1
        if 'руб.' in text[nchar]:
            cost = text[nchar]
            cost = cost[0:cost.find('руб.')].replace(' ', '')
        else:
            cost = 'договорная'
        link = 'https://freelance.habr.com/tasks/' + task_id if task_id != '0' else ''
        data[task_id] = ['Habr', title, '', cost, time, str(response), str(view), link]
        # print(task_id, title)

    return data, ''


if __name__ == '__main__':
    dummy = parse_habr(0)
