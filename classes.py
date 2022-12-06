
import sys

import conf
import key
import os
import pandas as pd
import pandas_ta as ta
import datetime
import json
from decimal import Decimal
from kucoin.client import Market, Trade, User



class Gate_spot:

    def __init__(self):
        print('Gate.io')



class Kucoin_spot:

    def __init__(self):
        self.tf = conf.tf
        self.url = 'https://api.kucoin.com'
        if os.path.isfile('key.py'):
            self.key = key.kucoin_key
            self.secret = key.kucoin_secret
            self.pasw = key.kucoin_pasw
        else:
            self.key = conf.kucoin_key
            self.secret = conf.kucoin_secret
            self.pasw = key.kucoin_pasw
        self.market = Market(self.url)
        self.trade = Trade(key=self.key, secret=self.secret, passphrase=self.pasw, url=self.url)

    def get_kline(self, symbol):
        '''

        :param symbol:
        :return:
        ['1670351400',
        '0.314833',
        '0.314448',
        '0.314833',
        '0.314369',
        '10477.0278',
        '3298.0528755327']
        '''
        return self.market.get_kline(symbol=symbol, kline_type=self.tf)

    def get_symbol_list(self):
        '''
        Получаем информацию о торговых парах
        :return:
        {'symbol': 'MHC-ETH',
        'name': 'MHC-ETH',
        'baseCurrency': 'MHC',
        'quoteCurrency': 'ETH',
        'feeCurrency': 'ETH',
        'market': 'ALTS',
        'baseMinSize': '1',
        'quoteMinSize': '0.0001',
        'baseMaxSize': '10000000000',
        'quoteMaxSize': '99999999',
        'baseIncrement': '0.0001',
        'quoteIncrement': '0.000000001',
        'priceIncrement': '0.000000001',
        'priceLimitRate': '0.1',
        'minFunds': '0.00001',
        'isMarginEnabled': False,
        'enableTrading': True}
        '''
        return self.market.get_symbol_list()

    def orders_list(self, status):
        return self.trade.get_order_list(status=status, type='limit', tradeType='TRADE')

    def fiat_price(self, coin):
        return self.market.get_fiat_price(currencies=coin)

    def s(self, symbol, side, size):
        return self.trade.create_market_order(symbol=symbol, side=side, type='market', size=size)







if conf.exchange == 'Kucoin.com':
    api = Kucoin_spot()
elif conf.exchange == 'Gate.io':
    api = Gate_spot()



class Bot:

    def __init__(self):
        self.tf = conf.tf

    def kline(self, symbol):
        return api.get_kline(symbol=symbol)

    def symbol_list(self):
        return api.get_symbol_list()

    def ones_symbol_list(self):
        '''
        Получаем список торговых пар
        :return:
        '''
        s = Bot().symbol_list()
        s_list = []
        for i in s:
            s_list.append(i['symbol'])
        return s_list

    def orders_list(self, status):
        return api.orders_list(status=status)

    def is_file_json(self):
        '''
        Если вспомогательного файла нет. то создаём
        и заполняем его пустым списком
        Подсчитываем не пустые файлы
        :return:
        '''
        kol_poz = 0
        for i in conf.whait_list:
            if not os.path.isfile('stock/{}.json'.format(i)):
                Bot().write_json([], i)
            else:
                data = Bot().read_json(i)
                if len(data) > 0:
                    kol_poz += 1
        return kol_poz

    def tm(self):
        """
        :return: Возвращает текущее время в формате ЧЧ:ММ:СС
        """
        return datetime.datetime.now().strftime('%H:%M:%S')

    def debug(self, var, inf):
        """
        :param var:
        :param inf:
        :return:
        """
        time = self.tm() if var == 'debug' else None
        if conf.debug == 'inform':
            if var == 'inform':
                print(inf)
            elif var == 'debug':
                print('\033[32m {} - {} \033[0;0m'.format(time, inf))
            else:
                print('\033[31m {} \033[0;0m'.format(inf))
        if conf.debug == 'debug':
            if var == 'debug':
                print('\033[32m {} - {} \033[0;0m'.format(time, inf))
            else:
                print('\033[31m {} \033[0;0m'.format(inf))
        if conf.debug == 'error':
            if var == 'error':
                print('\033[31m {} \033[0;0m'.format(inf))

    def write_json(self, data, para):
        """
        Записываем информацию по купленному или проданному ордеру
        :param data:
        :param para:
        :return:
        """
        with open('stock/{}.json'.format(para), 'w') as f:
            json.dump(data, f, indent=2)

    def read_json(self, para):
        """
        Читаем файл и заносим информацию в data
        усли файла нет то создаём его
        :param para:
        :return:
        """
        try:
            with open('stock/{}.json'.format(para)) as f:
                data = json.load(f)
        except FileNotFoundError:
            Bot().write_json(data=[], para=para)
        else:
            return data

    def create_df(self, symbol):
        data = Bot().kline(symbol=symbol)
        tm, close, high, low, opn, vol = [], [], [], [], [], []
        if conf.exchange == 'Kucoin.com':
            for i in list(reversed(data)):
                tm.append(int(i[0]) * 1000)
                close.append(float(i[2]))
                high.append(float(i[3]))
                low.append(float(i[4]))
                opn.append(float(i[1]))
                vol.append(float(i[5]))
        df = pd.DataFrame({'Time': tm,
                           'Close': close,
                           'High': high,
                           'Low': low,
                           'Open': opn,
                           'Volume': vol})
        df['Time'] = pd.to_datetime(df.Time, unit='ms')
        df.set_index('Time', inplace=True)
        #df = df[df.High != df.Low]  # удаляем свечи без движения
        # добавляем индикатор CCI
        df = Indicater().cci(df=df)
        #df.to_csv('dat.csv')  # записываем датафрейм в файл
        return df

    def create_position(self, symbol, side):
        symbol_infa = None
        # Получаем информацию о торговой паре
        if not os.path.isfile('stock/symbols.json'):
            symbol_list = api.get_symbol_list()
            Bot().write_json(symbol_list, 'symbols')
        else:
            symbol_list = Bot().read_json('symbols')
        for i in symbol_list:
            if i['symbol'] == symbol:
                symbol_infa = i
        # Высчитываем кол-во монет в ордер
        usd_price = float(api.fiat_price(symbol_infa['baseCurrency'])[symbol_infa['baseCurrency']])
        coins_in_order = conf.size_usd / usd_price
        if coins_in_order < symbol_infa['baseMinSize']:
            coins_in_order = symbol_infa['baseMinSize']
        print(coins_in_order)
        print(symbol_infa)


class Indicater:

    def __init__(self):
        pass

    def cci(self, df):
        df['CCI'] = ta.cci(df.High, df.Low, df.Close, length=20)
        return df
