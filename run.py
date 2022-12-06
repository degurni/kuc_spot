
import conf
from datetime import datetime
import time
import sys

from classes import Bot

bot = Bot()
def kuc_spot():
    start_time = datetime.now()
    max_zakaz = 0
    paras = conf.whait_list
    kol_poz = bot.is_file_json()  # Проверяем наличие вспомогательных файлов

    while True:
        if kol_poz < conf.max_poz:
            for para in paras:
                if kol_poz >= conf.max_poz:
                    break
                if len(bot.read_json(para)) == 0:
                    bot.debug('debug', '{}: Позиция ещё не открыта'.format(para))
                    df = bot.create_df(symbol=para)  # создаём датафрейм с последними свечами и сигналами индикаторов
                    if df.CCI[-2] < df.CCI[-1] < (conf.predel_cci * -1):
                        bot.debug('inform', '{}: Точка входа в позицию'.format(para))
                        # Заходим в позицию по рынку . заносим данные заказа в файл
                        t = bot.create_position(symbol=para, side='buy')




        time.sleep(1)






        new_time = datetime.now() - start_time
        nt = ((str(new_time)).split('.'))[0]
        print('Бот в работе - {} : MAX заказов - {}'.format(nt, max_zakaz))




if __name__ == '__main__':
    kuc_spot()
