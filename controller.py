import time
import view
import model_fl as fl
import model_habr as habr


def execute():
    new_tasks = dict()
    # 0 - id (key)
    # 0 - service (fl, kwork, habr)
    # 1 - task name
    # 2 - detail description
    # 3 - cost
    # 4 - time
    # 5 - responses
    # 6 - customer
    dict_habr = dict()
    dict_fl = dict()
    i = 0.5
    while True:
        dict_habr, new_tasks = habr.parse_habr(dict_habr, new_tasks)
        dict_fl, new_tasks = fl.parse_fl(dict_fl, new_tasks)
        view.show_tasks(new_tasks)
        if int(i) % 5 == 0 and i - int(i) == 0:
            print(int(i), 'мин.')
        i += 0.5
        time.sleep(30)
        new_tasks = dict()


if __name__ == '__main__':
    execute()
