import winsound
import time

KEYWORDS = 'excel,exel,эксел,ексел,vba,макрос,xls,csv,visual basic,таблиц,python,питон,power'
# KEYWORDS = 'прог,excel,exel,эксел,ексел,vba,макрос,xls,csv,visual basic,таблиц,python,питон,power'


def beep_beep():
    """Alarm"""
    winsound.Beep(2000, 200)
    time.sleep(0.1)
    winsound.Beep(2000, 200)
    time.sleep(0.1)
    winsound.Beep(1500, 400)


def mark_words(exp: str, keyword=KEYWORDS) -> str:
    """Mark keywords in sentence by yellow color"""
    keyword = keyword.split(',')
    for word in keyword:
        if word in exp.lower():
            pos = exp.lower().find(word)
            cut = exp[pos:pos + len(word)]
            exp = exp.replace(cut, '\033[1m\033[33m{}\033[0m'.format(cut))
    return exp


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
