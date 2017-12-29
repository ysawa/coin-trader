from bitflyer.api import BitflyerApi

bitflyer_api = BitflyerApi()
print('BitFlyer LAST PRICE: {} JPY/BTC'.format(bitflyer_api.request_last_price()))

result = bitflyer_api.request_trade('0.001', True)
print('BitFlyer child_order_acceptance_id: ', result)

