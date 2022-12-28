# Парсинг kwork.ru

import requests
from bs4 import BeautifulSoup as bs


def parse_kwork(method=1):
    # href_kwork = 'https://kwork.ru/projects'
    # rq = requests.get(href_kwork, allow_redirects=True)
    # soup = bs(rq.text, 'html.parser')
    # print(soup)

    html = open(r'C:\Temp\Python\Kwork3.html', encoding='utf8').read()
    soup = bs(html, 'html.parser')

    content = soup.find('div', class_='wants-content')
    # print(content)
    data = dict()
    tasks = content.find_all('div', class_='card__content pb5')
    for ref in tasks:

        title = ref.find('div', class_='wants-card__left')
        if title == None:
            title = '<Title not defined>'
        else:
            title = title.find('a')
            if title == None:
                title = '<Title not defined>'
            else:
                title = title.next

        info = ref.find('div', class_='d-inline breakwords first-letter')
        if info == None:
            info = '<Info not described>'
        else:
            while 'div' in str(info):
                info = info.next

        price = ref.find('div', class_='wants-card__header-price wants-card__price m-hidden')
        if price == None:
            price = '<Price not defined>'
        else:
            price = ''
            for text in ref.find('div', class_='wants-card__header-price wants-card__price m-hidden').find_all('span'):
                price += str(text.next + ' ')

        higher_price = ref.find('div', class_='wants-card__description-higher-price')
        if higher_price == None:
            higher_price = ''
        else:
            higher_price = str(higher_price.next).replace('\t', '')
            for text in ref.find('div', class_='wants-card__description-higher-price').find_all('span'):
                higher_price += str(text.next).strip() + ' '
            higher_price = ', ' + higher_price.replace('\n', ' ')

        author = ref.find('div', class_='dib')
        if author == None:
            author = '<Author not defined>'
        else:
            author = author.find('a').next

        remain = ref.find('span', class_='mr5')
        if remain == None:
            remain = '<Remain time not defined>'
        else:
            remain = remain.next

        data[ref.parent.get('data-id')] = [title, info, price.strip() + higher_price.strip(), author, remain]

    for key, task in data.items():
        print('\033[1m\033[31m{}\033[0m'.format('Kwork:'), key, task[0])
        print('\t', task[1])
        print('\t', task[2])
        print('\t', 'Заказчик', task[3])
        print('\t', task[4])


if __name__ == '__main__':
    parse_kwork()
