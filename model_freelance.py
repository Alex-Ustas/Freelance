# Парсинг freelance

import requests
from bs4 import BeautifulSoup as bs
import common_lib as lib
import re


def parse_freelance(new_tasks: dict, method=1) -> (dict, int, str):
    """Parse freelance.ru"""
    data = dict()
    rq = None
    new = 0
    if method == 1:
        href = 'https://freelance.ru/project/search'
        headers = \
            {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
                 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0'
            }
        try:
            rq = requests.get(href, headers=headers)
            soup = bs(rq.text, 'html.parser')
        except Exception as err:
            return new_tasks, 0, f'Freelance: unexpected {err=}, {type(err)=}\n'
    else:
        html = open(r'C:\Temp\Python\freelance2.html', encoding='utf8').read()
        soup = bs(html, 'html.parser')

    content = soup.find('div', class_='projects m-t-2')
    # print(content)
    if content is None:
        print(rq.status_code, rq.reason)
        exit()

    tasks = content.find_all('div', class_=re.compile('box-shadow project'))

    for task in tasks:
        title_part = task.find('div', class_='box-title')
        footer_part = task.find('div', class_='box-info')

        title = title_part.find('h2', class_='title')
        if title is None:
            title = '[Title not defined]'
        else:
            title = title.get('title')
        # print(title)

        task_id = title_part.find('h2', class_='title')
        if task_id is None:
            task_id = '0'
        else:
            task_id = task_id.find('a').get('href')[:-5]
            task_id = task_id[task_id.rfind('-') + 1:]
        # print(task_id)

        info = title_part.find('a', class_='description')
        if info is None:
            info = ''
        else:
            info = info.next.strip().replace('\n', ' ').replace('\r', ' ').replace('  ', ' ')
        # print(info)

        cost = footer_part.find('div', class_='cost')
        if cost is None:
            cost = ''
        else:
            cost = cost.next.strip()
        # print(cost)

        time = title_part.find('time', class_='timeago')
        if time is None:
            time = ''
        else:
            time = time.next.strip()
        # print(time)

        resp = title_part.find('i', class_='fa fa-comments-o')
        if resp is None:
            resp = ''
        else:
            resp = resp.next.replace('Откликов:', '').strip()
        # print(resp)

        term = footer_part.find('div', class_='term')
        if term is None:
            term = ''
        else:
            term = term.next.strip()
        # print(term)

        link = title_part.find('a', class_='description')
        if link is None:
            link = ''
        else:
            link = 'https://freelance.ru' + link.get('href')
        # print(link)

        data[task_id] = [title, info, cost, time, resp, term, link]

    # Check new projects
    for key, data_list in data.items():
        if key not in new_tasks.keys():
            for word in lib.KEYWORDS.split(','):
                if word in data_list[0].lower() or word in data_list[1].lower():
                    new_tasks[key] = ['Freelance', data_list[0], data_list[1], data_list[2],
                                      data_list[3], data_list[4], data_list[5], data_list[6], 'y']
                    new = 1

    return new_tasks, new, ''


if __name__ == '__main__':
    dummy = parse_freelance(dict(), 0)
