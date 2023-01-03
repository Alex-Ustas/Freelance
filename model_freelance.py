# Парсинг freelance

import requests
from bs4 import BeautifulSoup as bs
import common_lib as lib


def parse_freelance(free_dict: dict, new_tasks: dict, method=1) -> (dict, dict):
    """Parse freelance.ru"""
    data = dict()
    rq = None
    if method == 1:
        href = 'https://freelance.ru/project/search'
        headers = \
            {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
                 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0'
            }
        rq = requests.get(href, headers=headers)
        soup = bs(rq.text, 'html.parser')
    else:
        html = open(r'C:\Temp\Python\freelance.html', encoding='utf8').read()
        soup = bs(html, 'html.parser')

    content = soup.find('div', class_='projects m-t-2')
    # print(content)
    if content is None:
        print(rq.status_code, rq.reason)
        exit()

    tasks = content.find_all('div', class_='box-shadow project')

    for task in tasks:
        title_part = task.find('div', class_='box-title')
        footer_part = task.find('div', class_='box-info')

        title = title_part.find('h2', class_='title')
        if title is None:
            title = '<Title not defined>'
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
            info = '<Info not defined>'
        else:
            info = info.next.strip().replace('\n', ' ').replace('\r', ' ').replace('  ', ' ')
        # print(info)

        cost = footer_part.find('div', class_='cost')
        if cost is None:
            cost = '<Cost not defined>'
        else:
            cost = cost.next.strip()
        # print(cost)

        time = title_part.find('time', class_='timeago')
        if time is None:
            time = '<Time not defined>'
        else:
            time = time.next.strip()
        # print(time)

        resp = title_part.find('i', class_='fa fa-comments-o')
        if resp is None:
            resp = '<Response not defined>'
        else:
            resp = resp.next.replace('Откликов:', '').strip()
        # print(resp)

        term = footer_part.find('div', class_='term')
        if term is None:
            term = '<Term not defined>'
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
        if key not in free_dict.keys():
            free_dict[key] = data_list
            for word in lib.KEYWORDS.split(','):
                if word in data_list[0].lower() or word in data_list[1].lower():
                    new_tasks[key] = ['Freelance', data_list[0], data_list[1], data_list[2],
                                      data_list[3], data_list[4], data_list[5], data_list[6]]

    return free_dict, new_tasks


if __name__ == '__main__':
    dummy = parse_freelance(dict(), dict(), 0)
