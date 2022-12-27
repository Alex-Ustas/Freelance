# Парсинг freelance.habr.com

import requests as rq
import common_lib as lib
import html2text as ht


# ------------------------------------------------------------------------------------------- Habr freelance
def parse_task_habr(text: str):
    n1 = text.find('[')
    n2 = text.find(']')
    task = '[Task not detected]' if n1 == 0 or n2 == 0 else text[n1 + 1:n2].strip()
    return task


def parse_response_habr(text):
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


def habr_free(dict1):
    s = rq.get('https://freelance.habr.com/tasks')
    text = ht.html2text(s.text)
    text = text.split('\n')
    keyword = lib.KEYWORDS.split(',')
    beep = True if len(dict1.keys()) > 0 else False

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

        task = parse_task_habr(text[nchar])
        newtask = dict1.get(task, '_New_')
        newtask = True if newtask == '_New_' else False
        response, view, ago = parse_response_habr(text[nchar + 2])
        nchar += 3

        while 'руб.' not in text[nchar] and 'договорная' not in text[nchar]:
            nchar += 1
        if 'руб.' in text[nchar]:
            cash = text[nchar]
            cash = cash[0:cash.find('руб.')].replace(' ', '')
        else:
            cash = 'договорная'
        dict1[task] = [newtask, response, view, ago, cash]

    # Check new projects
    newtask = False
    for key, datalist in dict1.items():
        for word in keyword:
            if word in key.lower():
                if datalist[0]:
                    print('\033[1m\033[33m{}\033[0m'.format('Хабр:'), lib.mark_words(key))
                    if datalist[4] == 'договорная':
                        print(f'\tОткликов: {datalist[1]}, просмотров {datalist[2]}, {datalist[3]}, оплата: договорная')
                    else:
                        print(f'\tОткликов: {datalist[1]}, просмотров {datalist[2]}, {datalist[3]}, оплата:',
                              "{:,.0f}".format(int(datalist[4])))
                    newtask = True
                break
    if beep and newtask:
        lib.beep_beep()

    return dict1
