# Парсинг kwork.ru

from bs4 import BeautifulSoup as bs
from selenium import webdriver


def parse_kwork(platform: dict, method=1) -> (dict, str):
    """Parse Kwork"""
    data = dict()
    if platform['enable'] == 'n':
        return data, ''
    if method == 1:
        href = platform['link']
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)
            driver.get(href)
            soup = bs(driver.page_source, 'html.parser')
            driver.quit()
        except Exception as err:
            return data, f'Kwork: unexpected {err=}, {type(err)=}\n'
    else:
        html = open(r'C:\Temp\Python\Kwork6.html', encoding='utf8').read()
        soup = bs(html, 'html.parser')

    content = soup.find('div', class_='wants-content')
    if content is None:
        return data, 'Kwork: empty content.\n'

    tasks = content.find_all('div', class_='card__content pb5')
    if not tasks:
        # print(content)
        return data, 'Kwork: cannot find tasks.\n'

    for ref in tasks:
        # print(ref)
        task_id = ref.parent.get('data-id')
        link = f'{platform["link"]}{task_id}/view'
        title = ref.find('div', class_='wants-card__left')
        if title is None:
            title = '[Title not defined]'
        else:
            title = title.find('a')
            if title is None:
                title = '[Title not defined]'
            else:
                title = title.next
        # print(task_id, title)
        # print(link)

        info = ref.find('div', class_='wants-card__space')
        if info is None:
            info = ''
        else:
            info = info.next_sibling
            if '<br/>' == str(info):
                info = info.next
            info = '' if info is None else str(info)
        # print(info)

        price = ref.find('div', class_='wants-card__header-price wants-card__price m-hidden')
        if price is None:
            price = ''
        else:
            price = ''
            for text in ref.find('div', class_='wants-card__header-price wants-card__price m-hidden').find_all('span'):
                price += str(text.next + ' ')
            price = str(price).replace(' ', '')
            price = price[price.find(':') + 1:-1].strip()
            if not price[0].isdigit() and not price[1].isdigit():
                price = price[2:]

        higher_price = ref.find('div', class_='wants-card__description-higher-price')
        if higher_price is None:
            higher_price = ''
        else:
            higher_price = str(higher_price.next).replace('\t', '')
            for text in ref.find('div', class_='wants-card__description-higher-price').find_all('span'):
                higher_price += str(text.next).strip() + ' '
            higher_price = str(higher_price).replace('\n', ' ').replace(' ', '')
            higher_price = higher_price[higher_price.find(':') + 1:-1]
            if not higher_price[0].isdigit() and not higher_price[1].isdigit():
                higher_price = higher_price[2:]
            higher_price = ' - ' + '{:,.0f}'.format(int(higher_price))
        price = '{:,.0f}'.format(int(price)) + higher_price
        # print(price)

        author = ref.find('div', class_='dib')
        if author is None:
            author = ''
        else:
            author = 'Пользователь ' + author.find('a').next
        # print(author)

        resp = ''
        time = ref.find('span', class_='mr5')
        if time is None:
            time = ''
        else:
            resp = str(time.next_sibling.next.next)
            resp = 'Откликов: ' + resp[resp.find(' '):].strip()
            time = time.next
        # print(time)
        # print(resp, '\n')

        data[task_id] = ['Kwork', title, info, price, time, resp, author, link]

    return data, ''


if __name__ == '__main__':
    settings = {"enable": "y", "link": "https://kwork.ru/projects"}
    dummy = parse_kwork(settings, 1)
    if dummy[1]:
        print(dummy[1])
