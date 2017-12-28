# -*- coding: utf-8 -*-
import hashlib
import hmac
import uuid
from urllib import urlencode

import os
import requests
import json
from settings import *

NONCE_FILE = 'nonce.txt'


class ZaifApi:

    def load_nonce(self):
        if not os.path.exists(NONCE_FILE):
            return 0
        f = open(NONCE_FILE, 'r')
        nonce = int(f.readline())
        f.close()
        return nonce

    def last_price(self):
        response = requests.get('https://api.zaif.jp/api/1/last_price/btc_jpy')
        if response.status_code != 200:
            raise Exception('return status code is {}'.format(response.status_code))
        result = json.loads(response.text)
        return result['last_price']

    def save_nonce(self, nonce):
        f = open(NONCE_FILE, 'w')
        f.write(str(nonce))
        f.close()

    def trade_api(self, parameters=None):
        nonce = self.load_nonce()
        nonce += 1
        self.save_nonce(nonce)
        parameters['nonce'] = nonce
        encoded = urlencode(parameters)
        signature = hmac.new(bytearray(ZAIF_API_SECRET.encode('utf-8')), digestmod=hashlib.sha512)
        signature.update(encoded.encode('utf-8'))
        headers = {
            'key': ZAIF_API_KEY,
            'sign': signature.hexdigest()
        }
        response = requests.post('https://api.zaif.jp/tapi', data=encoded, headers=headers)
        if response.status_code != 200:
            raise Exception('return status code is {}'.format(response.status_code))
        result = json.loads(response.text)
        print(result)

        return result
