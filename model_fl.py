# Парсинг fl.ru

import requests
from bs4 import BeautifulSoup as bs


def parse_fl(platform: dict, method=1) -> (dict, str):
    """Parse fl.ru"""
    data = dict()
    if platform['enable'] == 'n':
        return data, ''
    rq = None
    if method == 1:
        href = platform['link']
        headers = \
            {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
                 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0'
            }
        try:
            rq = requests.get(href, headers=headers)
            soup = bs(rq.text, 'html.parser')
        except Exception as err:
            return data, f'FL: unexpected {err=}, {type(err)=}\n'
    else:
        html = open(r'C:\Temp\Python\fl5.html', encoding='utf8').read()
        soup = bs(html, 'html.parser')

    content = soup.find('div', class_='b-page__lenta')
    if content is None:
        return data, f'FL: empty content.\nstatus={rq.status_code}, reason={rq.reason}\n'

    tasks = content.find_all('div', class_='b-post__grid')

    for ref in tasks:
        title = ref.find('a')
        if title is None:
            title = '[Title not defined]'
            link = ''
            task_id = '0'
        else:
            task_id = title.get('name')[3:]
            link = 'https://www.fl.ru' + title.get('href')
            title = title.next.strip()
        # print(task_id, title)
        # print(link)

        scripts = ref.find_all('script')
        price = ''
        if len(scripts) > 0:
            price = scripts[0]
            if 'По договоренности' in str(price):
                price = 'по договоренности'
            else:
                price = bs(price.next.split("'")[1], 'html.parser').find('div')
                curr = price.find('span', class_='d-none')
                curr = '' if curr is None else curr.next.strip()

                cost = price.find('span')
                if cost is None:
                    cost = 'not defined'
                else:
                    cost = str(cost.next).strip()
                if cost.isdigit():
                    cost = '{:,.0f}'.format(int(cost))
                price = (cost + ' ' + curr).strip().lower()
        # print(price)

        info = ''
        if len(scripts) > 0:
            info = scripts[1]
            info = bs(info.next.split("'")[1], 'html.parser').find('div', class_="b-post__txt")
            if info is None:
                info = ''
            else:
                info = info.next.strip()
        # print(info)

        resp = ''
        if len(scripts) > 1:
            resp = scripts[2]
            resp = bs(resp.next.split("'")[1], 'html.parser').find('div', class_="b-post__txt")
            if resp is None:
                resp = ''
            else:
                resp = str(resp.find('svg').next_sibling).strip().lower()
                if ' ' in resp:
                    resp = resp[:resp.find(' ')]
        # print(resp)

        time = ''
        if len(scripts) > 1:
            time = scripts[2]
            time = bs(time.next.split("'")[1], 'html.parser').find('div', class_="b-post__txt")
            if time is None:
                time = ''
            else:
                time = time.find('span', class_='b-post__bold b-layout__txt_inline-block')
                if time is None:
                    time = ''
                else:
                    time = str(time.next).strip() + ' ' + str(time.next.next).strip()
        # print(time)
        data[task_id] = ['FL', title, info, price, time, resp, '', link]

    return data, ''


if __name__ == '__main__':
    settings = {"enable": "y", "link": "https://www.fl.ru/projects/"}
    dummy = parse_fl(settings, 0)
