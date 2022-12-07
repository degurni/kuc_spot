
import conf
from datetime import datetime
import time
import sys

from classes import Bot, Kucoin_spot

bot = Bot()
api = Kucoin_spot()

symbol = 'SOL-USDT'
symbol2 = 'ATOM-USDT'


# s = bot.create_df(symbol)

# s = bot.kline(symbol)

# s = bot.ones_symbol_list()

# s = api.get_symbol_list()
# for i in s:
#     if i['symbol'] == symbol:
#         print(i)

#{'symbol': 'ATOM-USDT', 'name': 'ATOM-USDT', 'baseCurrency': 'ATOM', 'quoteCurrency': 'USDT', 'feeCurrency': 'USDT', 'market': 'USDS', 'baseMinSize': '0.01', 'quoteMinSize': '0.00000001', 'baseMaxSize': '10000000000', 'quoteMaxSize': '99999999', 'baseIncrement': '0.0001', 'quoteIncrement': '0.0001', 'priceIncrement': '0.0001', 'priceLimitRate': '0.1', 'minFunds': '0.1', 'isMarginEnabled': True, 'enableTrading': True}
#{'symbol': 'SOL-USDT', 'name': 'SOL-USDT', 'baseCurrency': 'SOL', 'quoteCurrency': 'USDT', 'feeCurrency': 'USDT', 'market': 'USDS', 'baseMinSize': '0.01', 'quoteMinSize': '0.1', 'baseMaxSize': '10000000000', 'quoteMaxSize': '99999999', 'baseIncrement': '0.0001', 'quoteIncrement': '0.001', 'priceIncrement': '0.001', 'priceLimitRate': '0.1', 'minFunds': '0.1', 'isMarginEnabled': True, 'enableTrading': True}


s = api.get_kline('SOL-USDT')
print(s)


