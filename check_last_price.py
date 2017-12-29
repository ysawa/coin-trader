from zaif.api import ZaifApi

api = ZaifApi()
print('LAST PRICE: {} JPY/BTC'.format(api.request_last_price()))
