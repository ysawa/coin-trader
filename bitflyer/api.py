import json
from urllib.parse import quote_plus

import requests

from base.api import BaseApi

CURRENCY_PAIR_BTC_JPY = 'BTC_JPY'
END_POINT = 'https://api.bitflyer.jp/v1'


class BitflyerApi(BaseApi):

    def request_last_price(self, currency_pair=None):
        url = '{}/board/'.format(END_POINT)
        if currency_pair:
            url += '?product_code={}'.format(quote_plus(currency_pair))
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception('return status code is {}'.format(response.status_code))
        result = json.loads(response.text)
        return result['mid_price']
