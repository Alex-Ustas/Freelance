# Парсинг fl.ru

import requests
from bs4 import BeautifulSoup as bs
import common_lib as lib


def parse_fl(fl_dict: dict, method=1) -> dict:
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
        soup = bs(rq.text, 'lxml')
    else:
        html = open(r'C:\Temp\Python\fl2.html', encoding='utf8').read()
        soup = bs(html, 'lxml')

    content = soup.find('div', class_='b-page__lenta')
    # print(content)
    if content == None:
        print(rq.status_code, rq.reason)
        exit()

    tasks = content.find_all('div', class_='b-post__grid')

    for ref in tasks:
        # print(ref)
        title = ref.find('a')
        if title == None:
            title = '<Title not defined>'
            id = '0'
        else:
            id = title.get('name')[3:]
            title = f'{id} {title.next.strip()}'
            title = lib.mark_words(title)
        # print(title)

        scripts = ref.find_all('script')
        price = '<Title not defined>'
        if len(scripts) > 0:
            price = scripts[0]
            if 'По договоренности' in str(price):
                price = 'По договоренности'
            else:
                price = bs(price.next.split("'")[1], 'lxml').find('div')
                curr = price.find('span', class_='d-none')
                curr = '' if curr == None else curr.next

                cost = price.find('a')
                if cost == None:
                    cost = price.next
                else:
                    cost = cost.next.next.next.next
                price = (cost + curr).strip()
        # print('\t' + price)

        info = '<Info not defined>'
        if len(scripts) > 0:
            info = scripts[1]
            info = bs(info.next.split("'")[1], 'lxml').find('div', class_="b-post__txt")
            if info == None:
                info = '<Info not defined>'
            else:
                info = lib.split_sentence(lib.mark_words(info.next.strip()), 120, '\t')
        # print(info)

        resp = '<Response not defined>'
        if len(scripts) > 1:
            resp = scripts[2]
            resp = bs(resp.next.split("'")[1], 'lxml').find('div', class_="b-post__txt")
            if resp == None:
                resp = '<Response not defined>'
            else:
                resp = resp.find('a').next.next
        # print('\t' + resp)
        data[id] = [title, price, info, resp]

        time = '<Time not defined>'
        if len(scripts) > 1:
            time = scripts[2]
            time = bs(time.next.split("'")[1], 'lxml').find('div', class_="b-post__txt")
            if time == None:
                time = '<Time not defined>'
            else:
                time = time.find('span', class_='b-post__bold b-layout__txt_inline-block')
                if time == None:
                    time = '<Time not defined>'
                else:
                    time = str(time.next).strip() + ' ' + str(time.next.next).strip()
        # print('\t' + time)
        data[id] = [title, price, info, resp, time]

    # Check new projects
    new_task = False
    for key, datalist in data.items():
        if key not in fl_dict.keys():
            fl_dict[key] = datalist
            for word in lib.KEYWORDS.split(','):
                if word in datalist[0] or word in datalist[2]:
                    print('\033[1m\033[32m{}\033[0m'.format('FL.ru:'), datalist[0])
                    print(datalist[2])
                    print('\t' + datalist[1])
                    print('\t' + datalist[3])
                    print('\t' + datalist[4])
                    new_task = True

    if beep and new_task:
        lib.beep_beep()
    return fl_dict


if __name__ == '__main__':
    dummy = parse_fl(dict(), 0)
