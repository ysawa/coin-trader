from bitflyer.api import BitflyerApi
from zaif.api import ZaifApi

zaif_api = ZaifApi()
print('Zaif LAST PRICE: {} JPY/BTC'.format(zaif_api.request_last_price()))

bitflyer_api = BitflyerApi()
print('BitFlyer LAST PRICE: {} JPY/BTC'.format(bitflyer_api.request_last_price()))
