# -*- coding: utf-8 -*-

from zaif.api import ZaifApi

api = ZaifApi()
print('LAST PRICE: {} JPY/BTC'.format(api.last_price()))
