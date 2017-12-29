from zaif.api import ZaifApi, CURRENCY_PAIR_BTC_JPY

api = ZaifApi()
result = api.request_currency_pairs()
print(result)

result = api.request_latest_trade_api({
    'method': 'active_orders',
    'currency_pairs': 'btc_jpy'
})
print(result)

result = api.request_latest_trade_api({
    'method': 'get_info',
})
print(result)

result = api.request_latest_trade_api({
    'method': 'get_info2',
})
print(result)

result = api.request_latest_trade_api({
    'method': 'trade_history',
})
print(result)

result = api.request_balance()
print(result)
