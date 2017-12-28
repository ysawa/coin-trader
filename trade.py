# -*- coding: utf-8 -*-

from zaif.api import ZaifApi

api = ZaifApi()
api.trade_api({
    'method': 'active_orders',
    'currency_pairs': 'btc_jpy'
})
