# Show text in terminal and telegram

import loader


def colored_text(text: str, color: str) -> str:
    colors = {'black': '30',
              'red': '31',
              'green': '32',
              'yellow': '33',
              'blue': '34',
              'violet': '35',
              'turquoise': '36',
              'white': '37'}
    return f'\033[1m\033[{colors[color]}m{text}\033[0m'


def mark_words(exp: str, keywords: list, msg_type='terminal') -> str:
    """Mark keywords in sentence by specified color or bold for msg_type=bot"""
    for word in keywords:
        if word in exp.lower():
            pos = exp.lower().find(word)
            cut = exp[pos:pos + len(word)]
            if msg_type == 'bot':
                exp = exp.replace(cut, '<b>' + cut + '</b>')
            else:
                exp = exp.replace(cut, colored_text(cut, 'yellow'))
    return exp


def replacer(text: str, what_to_replace: str) -> str:
    for sym in what_to_replace:
        text = text.replace(sym, '')
    return text


def split_sentence(text: str, length: int, start_with='') -> str:
    """Split long sentence to several lines"""
    new = ''
    text = text.strip()
    if len(text) > 0:
        text = text.split()
        while len(text) > 0:
            part = text[0]
            del text[0]
            if len(part) < length and len(text) > 0:
                while True:
                    word = text[0]
                    if len(part) + len(word) + 1 > length:
                        break
                    part += ' ' + word
                    del text[0]
                    if len(text) == 0:
                        break
            if part != '':
                new = start_with + part if new == '' else new + '\n' + start_with + part
    return new


def show_tasks(tasks: dict, new_only=True):
    """Show detailed info regarding every task"""
    keywords = loader.get_keywords()
    platform = loader.get_platform()
    for key, data in tasks.items():
        if not new_only or (new_only and data[8] == 'y'):
            title = data[0]
            if title in platform.keys():
                title = colored_text(title + ':', platform[title]['color'])
            title += ' ' + split_sentence(key + ' ' + mark_words(data[1], keywords), 110)
            print(title)
            if data[2]:
                print(split_sentence(mark_words(data[2], keywords), 120, '\t'))
            if data[3]:
                print(f'\tСтоимость: {data[3]}')
            if data[4]:
                print(f'\t{data[4]}')
            if data[5]:
                print(f'\tОткликов: {data[5]}')
            if data[6]:
                print(f'\t{data[6]}')


def show_for_bot(bot, message, tasks: dict, new_only=True):
    """Show detailed info regarding every task in telegram"""
    keywords = loader.get_keywords()
    for key, data in tasks.items():
        if not new_only or (new_only and data[8] == 'y'):
            msg = '<b>' + data[0] + ':</b> ' + key + ' ' + \
                  mark_words(replacer(data[1], '<>'), keywords, 'bot') + '\n'
            msg += '_' * 40 + '\n'
            if data[2]:
                msg += mark_words(replacer(data[2], '<>'), keywords, 'bot') + '\n'
            if data[3]:
                msg += f'Стоимость: <b>{data[3]}</b>\n'
            if data[4]:
                msg += f'{data[4]}\n'
            if data[5]:
                msg += f'Откликов: {data[5]}\n'
            if data[6]:
                msg += data[6] + '\n'
            if data[7]:
                msg += f'<a href="{data[7]}">Link</a>'
            try:
                bot.send_message(message.chat.id, msg, parse_mode='html')
            except Exception as err:
                error = data[0] + ' ' + key + ' ' + data[1] + f'\nUnexpected {err=}, {type(err)=}'
                show_error(bot, message, error)


def show_error(bot, message, error_text: str):
    if error_text:
        print(colored_text('Ошибка обработки данных', 'red'))
        print(split_sentence(error_text, 120, '\t'))
        msg = '*Ошибка обработки данных*\n' + error_text
        bot.send_message(message.chat.id, msg, parse_mode='Markdown')
