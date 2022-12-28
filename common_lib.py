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

