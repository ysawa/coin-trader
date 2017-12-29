import hashlib
import hmac
import json
import time
from urllib.parse import quote_plus, urlencode

import requests

from base.api import BaseApi
from settings import BITFLYER_API_SECRET, BITFLYER_API_KEY

CURRENCY_PAIR_BTC_JPY = 'BTC_JPY'
END_POINT = 'https://api.bitflyer.jp'


class BitflyerApi(BaseApi):

    def get_currency_pair(self, currency_pair=None):
        if currency_pair is None:
            return CURRENCY_PAIR_BTC_JPY
        return currency_pair

    def request_balance(self):
        result = None
        return result

    def request_cancel(self, child_order_id=None, child_order_acceptance_id=None, currency_pair=None, **options):
        currency_pair = self.get_currency_pair(currency_pair)
        parameters = {
            'product_code': currency_pair,
        }
        if child_order_id:
            parameters['child_order_id'] = child_order_id
        else:
            parameters['child_order_acceptance_id'] = child_order_acceptance_id
        result = self.request_private_api('/v1/me/cancelchildorder', parameters=parameters)
        return result

    def request_last_price(self, currency_pair=None):
        parameters = dict()
        if currency_pair:
            parameters['product_code'] = currency_pair
        result = self.request_public_api('/v1/board/', parameters)
        return result['mid_price']

    def request_private_api(self, path, method='POST', parameters=None):
        timestamp = str(time.time())
        if parameters is None:
            parameters = dict()
        body = ''
        if method == 'POST':
            body = json.dumps(parameters)
        elif parameters:
            body += '?' + urlencode(parameters)
        text = timestamp + method + path + body
        signature = hmac.new(bytearray(BITFLYER_API_SECRET.encode()), digestmod=hashlib.sha256)
        signature.update(text.encode())
        headers = {
            'ACCESS-KEY': BITFLYER_API_KEY,
            'ACCESS-TIMESTAMP': timestamp,
            'ACCESS-SIGN': signature.hexdigest(),
            'Content-Type': 'application/json'
        }
        url = '{}{}'.format(END_POINT, path)

        if method == 'POST':
            response = requests.post(url, data=body, headers=headers)
        else:
            url += body
            response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception('return status code is {} "{}"'.format(response.status_code, response.text))
        if not response.text:
            return None
        result = json.loads(response.text)
        return result

    def request_public_api(self, path, parameters=None):
        url = '{}{}'.format(END_POINT, path)
        if parameters:
            url += '&' + urlencode(parameters)
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception('return status code is {} "{}"'.format(response.status_code, response.text))
        result = json.loads(response.text)
        return result

    def request_trade(self, amount, is_ask, price=None, currency_pair=None, **options):
        currency_pair = self.get_currency_pair(currency_pair)
        parameters = {
            'product_code': currency_pair,
            'child_order_type': ('LIMIT' if price else 'MARKET'),
            'side': ('BUY' if is_ask else 'SELL'),
            'size': amount,
        }
        if price:
            parameters['price'] = price
        result = self.request_private_api('/v1/me/sendchildorder', parameters=parameters)
        return result['child_order_acceptance_id']
