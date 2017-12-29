import hashlib
import hmac
from urllib.parse import urlencode, quote_plus

import os
import requests
import json
from settings import *

CURRENCY_PAIR_BTC_JPY = 'btc_jpy'
NONCE_FILE = 'nonce.txt'


class ZaifApi:
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
        response = requests.get('https://api.zaif.jp/api/1/currency_pairs/{}'.format(quote_plus(currency_pair)))
        if response.status_code != 200:
            raise Exception('return status code is {}'.format(response.status_code))
        result = json.loads(response.text)
        return result

    def request_last_price(self):
        response = requests.get('https://api.zaif.jp/api/1/last_price/{}'.format(quote_plus(CURRENCY_PAIR_BTC_JPY)))
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
        response = requests.post('https://api.zaif.jp/tapi', data=encoded, headers=headers)
        if response.status_code != 200:
            raise Exception('return status code is {}'.format(response.status_code))
        result = json.loads(response.text)
        if int(result['success']) != 1:
            raise Exception('return success code is {}'.format(result['success']))

        return result['return']
