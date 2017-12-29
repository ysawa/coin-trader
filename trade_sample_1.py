from bitflyer.api import BitflyerApi
from zaif.api import ZaifApi, CURRENCY_PAIR_BTC_JPY

bitflyer_api = BitflyerApi()
result = bitflyer_api.request_private_api('/v1/me/getbalance', 'GET')
print(result)

zaif_api = ZaifApi()
result = zaif_api.request_currency_pairs()
print(result)

result = zaif_api.request_latest_trade_api({
    'method': 'active_orders',
    'currency_pairs': 'btc_jpy'
})
print(result)

result = zaif_api.request_latest_trade_api({
    'method': 'get_info',
})
print(result)

result = zaif_api.request_latest_trade_api({
    'method': 'get_info2',
})
print(result)

result = zaif_api.request_latest_trade_api({
    'method': 'trade_history',
})
print(result)

result = zaif_api.request_balance()
print(result)
