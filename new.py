
import conf
from datetime import datetime
import time
import sys

from classes import Bot, Kucoin_spot

bot = Bot()
api = Kucoin_spot()

symbol = 'ATOM-USDT'


# s = bot.create_df(symbol)

# s = bot.kline(symbol)
t = api.s(symbol, 'buy', 0.01)







