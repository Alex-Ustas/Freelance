import time
import model_fl as fl
import model_habr as habr


def execute():
    dict_habr = dict()
    dict_fl = dict()
    i = 0.5
    while True:
        dict_habr = habr.habr_free(dict_habr)
        dict_fl = fl.parse_fl(dict_fl)
        if int(i) % 5 == 0 and i - int(i) == 0:
            print(int(i), 'мин.')
        i += 0.5
        time.sleep(30)
