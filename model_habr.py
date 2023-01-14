# Парсинг freelance.habr.com

import requests
from bs4 import BeautifulSoup as bs
import re


def parse_habr(platform: dict, method=1) -> (dict, str):
    """Parse habr.com"""
    data = dict()
    if platform['enable'] == 'n':
        return data, ''
    rq = None
    if method == 1:
        href = platform['link']
        headers = \
            {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
                 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
            }
        try:
            rq = requests.get(href, headers=headers)
            soup = bs(rq.text, 'html.parser')
        except Exception as err:
            return data, f'Freelance: unexpected {err=}, {type(err)=}\n'
    else:
        html = open(r'C:\Temp\Python\habr.html', encoding='utf8').read()
        soup = bs(html, 'html.parser')

    # Generate dictionary
    content = soup.find('ul', class_='content-list content-list_tasks')
    # print(content)
    if content is None:
        return data, f'Habr: content is empty!\nstatus={rq.status_code}, reason={rq.reason}\n'

    tasks = content.find_all('li', class_=re.compile('content-list__item'))
    for task in tasks:
        title = task.find('a')
        if title is None:
            title = '[Title not defined]'
            task_id = '0'
            link = ''
        else:
            task_id = title.get('href')
            task_id = task_id[task_id.rfind('/') + 1:]
            title = title.next.strip()
            link = 'https://freelance.habr.com/tasks/' + task_id
        # print(task_id, title)

        cost = task.find('span', class_='count')
        if cost is None:
            cost = task.find('span', class_='negotiated_price')
            if cost is None:
                cost = ''
            else:
                cost = cost.next.strip().lower()
        else:
            cost = cost.next.strip().lower()
        # print(cost)

        time = task.find('span', class_='params__published-at icon_task_publish_at')
        if time is None:
            time = ''
        else:
            time = time.find('span')
            if time is None:
                time = ''
            else:
                time = time.next.strip().lower()
        # print(time)

        resp = task.find('span', class_='params__responses icon_task_responses')
        if resp is None:
            resp = ''
        else:
            resp = resp.find('i', class_='params__count')
            if resp is None:
                resp = ''
            else:
                resp = resp.next.strip()
        # print(resp)

        data[task_id] = ['Habr', title, '', cost, time, resp, '', link]

    return data, ''


if __name__ == '__main__':
    settings = {"enable": "y", "link": "https://freelance.habr.com/tasks"}
    dummy = parse_habr(settings, 0)
