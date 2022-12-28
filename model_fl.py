# Парсинг fl.ru

import requests
from bs4 import BeautifulSoup as bs
import common_lib as lib


def parse_fl(fl_dict: dict, new_tasks: dict, method=1) -> (dict, dict):
    """Parse fl.ru"""
    beep = True if len(fl_dict) > 0 else False
    data = dict()
    if method == 1:
        href_fl = 'https://www.fl.ru/projects/'
        headers = \
            {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
                 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0'
            }
        rq = requests.get(href_fl, headers=headers)
        soup = bs(rq.text, 'html.parser')
    else:
        html = open(r'C:\Temp\Python\fl2.html', encoding='utf8').read()
        soup = bs(html, 'html.parser')

    content = soup.find('div', class_='b-page__lenta')
    # print(content)
    if content is None:
        print(rq.status_code, rq.reason)
        exit()

    tasks = content.find_all('div', class_='b-post__grid')

    for ref in tasks:
        # print(ref)
        title = ref.find('a')
        if title is None:
            title = '<Title not defined>'
            task_id = '0'
        else:
            task_id = title.get('name')[3:]
            title = title.next.strip()
            # title = lib.mark_words(title)
        # print(title)

        scripts = ref.find_all('script')
        price = '<Title not defined>'
        if len(scripts) > 0:
            price = scripts[0]
            if 'По договоренности' in str(price):
                price = 'По договоренности'
            else:
                price = bs(price.next.split("'")[1], 'html.parser').find('div')
                curr = price.find('span', class_='d-none')
                curr = '' if curr is None else curr.next

                cost = price.find('a')
                if cost is None:
                    cost = price.next
                else:
                    cost = cost.next.next.next.next
                price = (cost + curr).strip()
        # print('\t' + price)

        info = '<Info not defined>'
        if len(scripts) > 0:
            info = scripts[1]
            info = bs(info.next.split("'")[1], 'html.parser').find('div', class_="b-post__txt")
            info = '<Info not defined>' if info is None else info.next.strip()
        # print(info)

        resp = '<Response not defined>'
        if len(scripts) > 1:
            resp = scripts[2]
            resp = bs(resp.next.split("'")[1], 'html.parser').find('div', class_="b-post__txt")
            if resp is None:
                resp = '<Response not defined>'
            else:
                resp = resp.find('a').next.next.strip().lower()
        # print('\t' + resp)
        data[task_id] = [title, price, info, resp]

        time = '<Time not defined>'
        if len(scripts) > 1:
            time = scripts[2]
            time = bs(time.next.split("'")[1], 'html.parser').find('div', class_="b-post__txt")
            if time is None:
                time = '<Time not defined>'
            else:
                time = time.find('span', class_='b-post__bold b-layout__txt_inline-block')
                if time is None:
                    time = '<Time not defined>'
                else:
                    time = str(time.next).strip() + ' ' + str(time.next.next).strip()
        # print('\t' + time)
        data[task_id] = [title, price, info, resp, time]

    # Check new projects
    new_task = False
    for key, data_list in data.items():
        if key not in fl_dict.keys():
            fl_dict[key] = data_list
            for word in lib.KEYWORDS.split(','):
                if word in data_list[0].lower() or word in data_list[2].lower():
                    # print('\033[1m\033[32m{}\033[0m'.format('FL.ru:'), data_list[0])
                    # print(data_list[2])
                    # print('\t' + data_list[1])
                    # print('\t' + data_list[3])
                    # print('\t' + data_list[4])
                    new_task = True
                    new_tasks[key] = ['FL.ru', data_list[0], data_list[2], data_list[1], data_list[4], data_list[3], '']

    if beep and new_task:
        lib.beep_beep()
    return fl_dict, new_tasks


if __name__ == '__main__':
    dummy = parse_fl(dict(), dict(), 0)
