# Парсинг freelance

import requests
from bs4 import BeautifulSoup as bs


def parse_project(tasks, project: dict):
    for task in tasks:
        title_part = task.find('div', class_='row')
        footer_part = task.find('div', class_='project-footer')

        task_id = '0'
        title = '[Title not defined]'
        info = ''
        cost = ''
        time = ''
        resp = ''
        term = ''
        link = ''
        if title_part is not None:
            title = title_part.find('h2', class_='title')
            if title is None:
                title = '[Title not defined]'
            else:
                title = title.get('title').strip()

            task_id = title_part.find('h2', class_='title')
            if task_id is None:
                task_id = '0'
            else:
                task_id = task_id.find('a').get('href')[:-5]
                task_id = task_id[task_id.rfind('-') + 1:]
            # print(task_id, title)

            info = title_part.find('a', class_='description')
            if info is None:
                info = ''
            else:
                info = info.next.strip().replace('\n', ' ').replace('\r', ' ').replace('  ', ' ')
            # print(info)

            cost = title_part.find('div', class_='cost')
            if cost is None:
                cost = ''
            else:
                cost = cost.next.strip().lower()
            # print(cost)

            term = title_part.find('div', class_='term')
            if term is None:
                term = ''
            else:
                term = term.find('span')
                if term is None:
                    term = ''
                else:
                    term = 'Срок выполнения: ' + term.next.strip()
            # print(term)

            link = title_part.find('a', class_='description')
            if link is None:
                link = ''
            else:
                link = 'https://freelance.ru' + link.get('href')
            # print(link)

        if footer_part is not None:
            time = footer_part.find('time', class_='timeago')
            if time is None:
                time = ''
            else:
                time = 'Опубликовано: ' + time.next.strip()
            # print(time)

            resp = footer_part.find('span', class_='comments-count')
            if resp is None:
                resp = ''
            else:
                resp = resp.next.strip()
            # print(resp)

        project[task_id] = ['Freelance', title, info, cost, time, resp, term, link]


def parse_freelance(platform: dict, method=1) -> (dict, str):
    """Parse freelance.ru"""
    data = dict()
    if platform['enable'] == 'n':
        return data, ''
    rq = None
    if method == 1:
        href = platform['link']
        headers = \
            {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
                 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
            }
        try:
            rq = requests.get(href, headers=headers)
            soup = bs(rq.text, 'html.parser')
        except Exception as err:
            return data, f'Freelance: unexpected {err=}, {type(err)=}\n'
    else:
        html = open(r'C:\Temp\Python\freelance3.html', encoding='utf8').read()
        soup = bs(html, 'html.parser')

    content = soup.find('div', class_='projects m-t-2')
    if content is None:
        return data, f'Freelance: empty content.\nstatus={rq.status_code}, reason={rq.reason}\n'

    tasks = content.find_all('div', class_='project')
    parse_project(tasks, data)
    tasks = content.find_all('div', class_='project highlight')
    parse_project(tasks, data)

    return data, ''


if __name__ == '__main__':
    settings = {"enable": "y", "link": "https://freelance.ru/project/search"}
    dummy = parse_freelance(settings, 0)
