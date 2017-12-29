import hashlib
import hmac
from urllib.parse import urlencode, quote_plus

import os
import requests
import json

from base.api import BaseApi
from settings import *

CURRENCY_PAIR_BTC_JPY = 'btc_jpy'
END_POINT = 'https://api.zaif.jp/api/1'
END_POINT_LATEST_TRADE = 'https://api.zaif.jp/tapi'
NONCE_FILE = 'zaif_nonce.txt'


class ZaifApi(BaseApi):

    def get_currency_pair(self, currency_pair=None):
        if currency_pair is None:
            return CURRENCY_PAIR_BTC_JPY
        return currency_pair

    def load_nonce(self):
        if not os.path.exists(NONCE_FILE):
            return 0
        f = open(NONCE_FILE, 'r')
        nonce = int(f.readline())
        f.close()
        return nonce

    def save_nonce(self, nonce):
        f = open(NONCE_FILE, 'w')
        f.write(str(nonce))
        f.close()

    def request_balance(self):
        result = self.request_latest_trade_api({'method': 'get_info', })
        result = result['funds']
        return result

    def request_currency_pairs(self, currency_pair='all'):
        response = requests.get('{}/currency_pairs/{}'.format(END_POINT, quote_plus(currency_pair)))
        if response.status_code != 200:
            raise Exception('return status code is {}'.format(response.status_code))
        result = json.loads(response.text)
        return result

    def request_last_price(self, currency_pair=None):
        currency_pair = self.get_currency_pair(currency_pair)
        response = requests.get('{}/last_price/{}'.format(END_POINT, quote_plus(currency_pair)))
        if response.status_code != 200:
            raise Exception('return status code is {}'.format(response.status_code))
        result = json.loads(response.text)
        return result['last_price']

    def request_latest_trade_api(self, parameters=None):
        nonce = self.load_nonce()
        nonce += 1
        self.save_nonce(nonce)
        parameters['nonce'] = nonce
        encoded = urlencode(parameters)
        signature = hmac.new(bytearray(ZAIF_API_SECRET.encode('utf-8')), digestmod=hashlib.sha512)
        signature.update(encoded.encode('utf-8'))
        headers = {'key': ZAIF_API_KEY, 'sign': signature.hexdigest()}
        response = requests.post(END_POINT_LATEST_TRADE, data=encoded, headers=headers)
        if response.status_code != 200:
            raise Exception('return status code is {}'.format(response.status_code))
        result = json.loads(response.text)
        if int(result['success']) != 1:
            raise Exception('return success code is {}'.format(result['success']))

        return result['return']

    def request_trade(self, amount, is_ask, price=None, currency_pair=None, **options):
        currency_pair = self.get_currency_pair(currency_pair)
        parameters = {
            'currency_pair': currency_pair,
            'action': ('ask' if is_ask else 'bid'),
            'price': price,
            'amount': amount,
        }
        if 'limit' in options:
            parameters['limit'] = options['limit']
        if 'comment' in options:
            parameters['comment'] = options['comment']

        result = self.request_latest_trade_api(parameters)
        return result
