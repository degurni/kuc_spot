
import sys
import time

import conf
import key
import os
import pandas as pd
import pandas_ta as ta
import datetime
import json
from decimal import Decimal
from kucoin.client import Market, Trade, User  # pip install kucoin-python



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
            self.pasw = conf.kucoin_pasw
        self.market = Market(self.url)
        self.trade = Trade(key=self.key, secret=self.secret, passphrase=self.pasw, url=self.url)
        self.user = User(key=self.key, secret=self.secret, passphrase=self.pasw, url=self.url)

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
        time.sleep(conf.sl)
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
        time.sleep(conf.sl)
        return self.market.get_symbol_list()

    def orders_list(self, status):
        time.sleep(conf.sl)
        return self.trade.get_order_list(status=status, type='limit', tradeType='TRADE')

    def fiat_price(self, coin):
        time.sleep(conf.sl)
        return self.market.get_fiat_price(currencies=coin)

    def balance(self, coin):
        time.sleep(conf.sl)
        return self.user.get_account_list(currency=coin, account_type='trade')

    def create_order(self, symbol, side, size):
        time.sleep(conf.sl)
        return self.trade.create_market_order(symbol=symbol, side=side, type='market', size=size)

    def order_details(self, order_id):
        '''

        :param order_id:
        :return:
        {'id': '63902e9e5c73210001be4341',
        'symbol': 'ATOM-USDT',
        'opType': 'DEAL',
        'type': 'market',
        'side': 'buy',
        'price': '0',
        'size': '0.01',
        'funds': '0',
        'dealFunds': '0.100577',
        'dealSize': '0.01',
        'fee': '0.000100577',
        'feeCurrency': 'USDT',
        'stp': '',
        'stop': '',
        'stopTriggered': False,
        'stopPrice': '0',
        'timeInForce': 'GTC',
        'postOnly': False,
        'hidden': False,
        'iceberg': False,
        'visibleSize': '0',
        'cancelAfter': 0,
        'channel': 'API',
        'clientOid': '036f6a7c75f611ed8cafc46e1f218b2a',
        'remark': None,
        'tags': None,
        'isActive': False,
        'cancelExist': False,
        'createdAt': 1670393502516,
        'tradeType': 'TRADE'}
        '''
        time.sleep(conf.sl)
        return self.trade.get_order_details(orderId=order_id)







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
            if i['enableTrading']:
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
            # Если файла с ордерами нет, то создаём его в папке <stock> и заполняем пустым списком
            if not os.path.isfile('stock/{}.json'.format(i)):
                Bot().write_json([], i)
            else  :# Если есть, подсчитываем кол-во открытых позиций
                data = Bot().read_json(i)
                if len(data) > 0:
                    kol_poz += 1
        # Если нет файла с результатами торгов, то создаём его
        if not os.path.isfile('stock/{}.json'.format('result')):
            res = []
            for i in conf.whait_list:
                inf = {'symbol': i, 'result': 0}
                res.append(inf)
        else:  # Если есть проверяем
            res = Bot().read_json('result')
            for i in conf.whait_list:
                nal = False
                for j in res:
                    if i == j['symbol']:
                        nal = True
                if not nal:
                    res.append({'symbol': i, 'result': 0})
        Bot().write_json(res, 'result')
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

    def having_balance(self, quote):
        hav_balance = True
        quote_price = api.fiat_price(quote)[quote]  # '17028.26975477'
        quote_balance = api.balance(quote)[0]['available']
        need = conf.size_usd / float(quote_price)
        need = Decimal(str(need))
        if need > Decimal(quote_balance):
            hav_balance = False
        return hav_balance

    def progress(self, para, orders, navar_price, price_close, mimo_price):
        kr = '\033[31m'
        gr = '\033[32m'
        sbros = '\033[0m'
        pruf = 10
        navar_price = float(navar_price)
        mimo_price = float(mimo_price)
        z = '.'
        # pr = '{}{}{}{}{}'.format(sbros, kr, para, sbros, gr)

        delen = (mimo_price - navar_price) / pruf
        if price_close >= navar_price:
            lev = 0
            z = '<'
        else:
            lev = round((price_close - navar_price) / delen)
            if lev > pruf:
                lev = pruf
                z = '>'
        prav = pruf - lev
        time = self.tm()
        print('{}{} - {}: Ордеров {}, {} {}{}{}{}{} {}{}'.format(
            gr, time, para, orders, navar_price, kr, z * lev, sbros, gr, z * prav, mimo_price, sbros))


    def result(self, symbol):
        gr = '\033[32m'
        sbros = '\033[0m'
        kr = '\033[31m'
        color = gr
        data = Bot().read_json(para='result')
        for i in data:
            if i['symbol'] == symbol:
                result = i['result']
                if result < 0:
                    color = kr
                print('{}{}: Total: {}{}{}'.format(gr, symbol, color, result, sbros))

    def check_profit(self, df, para):
        k = False
        data = Bot().read_json(para)
        navar = 1 + (conf.navar / 100)
        mimo = 1 - (conf.navar / 100)
        navar_price = Decimal(data[-1]['price'] * navar)
        mimo_price = Decimal(data[-1]['price'] * mimo)
        navar_price = navar_price.quantize(Decimal(data[-1]['tick_size']))
        mimo_price = mimo_price.quantize(Decimal(data[-1]['tick_size']))
        Bot().progress(para=para, orders=len(data), navar_price=navar_price, price_close=df.Close[-1],
                       mimo_price=mimo_price)
        Bot().result(symbol=para)
        # print('price - {}'.format(df.Close[-1]))
        # print('CCI-1 - {} : CCI-2 - {}'.format(df.CCI[-1], df.CCI[-2]))
        if float(navar_price) < df.Close[-1] and df.CCI[-1] < df.CCI[-2]:
            Bot().debug('inform', '{} : Продаём {} {}'.format(para, data[-1]['size'], data[-1]['coin']))
            s = Bot().create_order(symbol=para, side='sell')
            if s:
                k = True
        elif mimo_price > df.Close[-1] and df.CCI[-1] > df.CCI[-2]:
            Bot().debug('inform', '{} : Докупаем {} {}'.format(para, data[-1]['size'], data[-1]['coin']))
            Bot().create_order(symbol=para, side='buy')
        return k

    def create_order(self, symbol, side):
        p = False
        data = Bot().read_json(para=symbol)
        res = Bot().read_json(para='result')
        order_id = api.create_order(symbol=symbol, side=side, size=data[-1]['size'])['orderId']
        inf_order = api.order_details(order_id=order_id)
        made_price = float(inf_order['dealFunds']) / float(inf_order['size'])  # цена исполнения ордера
        if side == 'buy':
            inf = {'id': inf_order['id'],
                   'symbol': inf_order['symbol'],
                   'coin': data[-1]['coin'],
                   'size': data[-1]['size'],
                   'fee': inf_order['fee'],
                   'price': made_price,
                   'zatrat': inf_order['dealFunds'],
                   'tick_size': data[-1]['tick_size'],
                   'mod_price': made_price,
                   'mp': made_price / 100 * conf.perc_mod_price}
            data.append(inf)
            for i in res:
                if i['symbol'] == symbol:
                    i['result'] -= (float(inf_order['dealFunds']) + float(inf_order['fee']))
        elif side == 'sell':
            data.pop(-1)
            for i in res:
                if i['symbol'] == symbol:
                    i['result'] += float(inf_order['dealFunds'])
                    i['result'] -= float(inf_order['fee'])
            data[0]['mod_price'] -= data[0]['mp']
            if data[0]['mod_price'] <= 0:
                order_id = api.create_order(symbol=symbol, side=side, size=data[-1]['size'])['orderId']
                inf_order = api.order_details(order_id=order_id)
                for i in res:
                    if i['symbol'] == symbol:
                        i['result'] += float(inf_order['dealFunds'])
                        i['result'] -= float(inf_order['fee'])
                data.pop(0)
            if len(data) == 0:
                p = True
                for i in res:
                    if i['symbol'] == symbol:
                        if not conf.sum_result:
                            i['result'] = 0
        Bot().write_json(data=data, para=symbol)
        Bot().write_json(data=res, para='result')
        return p

    def create_position(self, symbol, side='buy'):
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
        if coins_in_order < float(symbol_infa['baseMinSize']):
            coins_in_order = symbol_infa['baseMinSize']
        coins_in_order = Decimal(coins_in_order)
        size = str(coins_in_order.quantize(Decimal(symbol_infa['baseIncrement'])))
        # Проверяем баланс для закупа
        hav_balance = Bot().having_balance(symbol_infa['quoteCurrency'])
        if not hav_balance:
            Bot().debug('error', 'Необходимо пополнить баланс {}'.format(symbol_infa['quoteCurrency']))
        else:
            # Выставляем начальный ордер
            order_id = api.create_order(symbol=symbol, side=side, size=size)['orderId']
            inf_order = api.order_details(order_id=order_id)
            made_price = float(inf_order['dealFunds']) / float(inf_order['size'])  # цена исполнения ордера
            basecoin = inf_order['symbol'].split('-')[0]
            inf = {'id': inf_order['id'],
                   'symbol': inf_order['symbol'],
                   'coin': basecoin,
                   'size': inf_order['size'],
                   'fee': inf_order['fee'],
                   'price': made_price,
                   'zatrat': inf_order['dealFunds'],
                   'tick_size': symbol_infa['quoteIncrement'],
                   'mod_price': made_price,
                   'mp': made_price / 100 * conf.perc_mod_price}
            data = Bot().read_json(para=inf_order['symbol'])
            data.append(inf)
            Bot().write_json(data=data, para=inf_order['symbol'])
            res = Bot().read_json('result')
            for i in res:
                if i['symbol'] == inf_order['symbol']:
                    i['result'] -= (float(inf_order['dealFunds']) + float(inf_order['fee']))
                    Bot().write_json(data=res, para='result')
            return True









class Indicater:

    def __init__(self):
        pass

    def cci(self, df):
        df['CCI'] = ta.cci(df.High, df.Low, df.Close, length=20)
        return df
