
import conf
from datetime import datetime
import time
import sys

from classes import Bot

bot = Bot()
def kuc_spot():
    # для отслеживания времени работы скрипта и максимального количества ордеров
    start_time = datetime.now()
    max_zakaz = 0
    paras = conf.whait_list  # Список возможных пар для торговли
    kol_poz = bot.is_file_json()  # Проверяем наличие вспомогательных файлов

    while True:
        try:
            if kol_poz < conf.max_poz:  # Если открытых позиций меньше допустимого
                for para in paras:
                    if kol_poz >= conf.max_poz:
                        break
                    if len(bot.read_json(para)) == 0:  # Если позиция по торговой паре ещё не открыта
                        bot.debug('debug', '{}: Позиция ещё не открыта'.format(para))
                        df = bot.create_df(symbol=para)  # создаём датафрейм с последними свечами и сигналами индикаторов
                        if df.CCI[-2] < df.CCI[-1] < (conf.predel_cci * -1):
                            bot.debug('inform', '{}: Точка входа в позицию'.format(para))
                            # Заходим в позицию по рынку . заносим данные заказа в файл
                            t = bot.create_position(symbol=para, side='buy')
                            if t:
                                kol_poz += 1
            if kol_poz:
                for para in paras:
                    if len(bot.read_json(para)) > 0:  # если уже открыта позиция
                        df = bot.create_df(symbol=para)  # создаём датафрейм с последними свечами и сигналами индикаторов
                        t = bot.check_profit(df=df, para=para)
                        if t:
                            kol_poz -= 1
            print('=' * 60)
            for para in paras:
                data = bot.read_json(para)
                if max_zakaz < len(data):
                    max_zakaz = len(data)
            new_time = datetime.now() - start_time
            nt = ((str(new_time)).split('.'))[0]
            print('Бот в работе - {} : MAX заказов - {}'.format(nt, max_zakaz))
            time.sleep(conf.sleep)
        except KeyboardInterrupt:
            bot.debug('inform', 'Работа бота завершена')
            sys.exit(0)
        except Exception as e:
            print(type(e))
            bot.debug('inform', 'Возникла непредвиденная ошибка - {}'.format(e))
            time.sleep(conf.sleep)
            bot.debug('inform', 'Перезапускаюсь...')




if __name__ == '__main__':
    kuc_spot()
