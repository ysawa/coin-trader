# -*- coding: utf-8 -*-

import requests
import json


class ZaifApi:
    def last_price(self):
        response = requests.get('https://api.zaif.jp/api/1/last_price/btc_jpy')
        if response.status_code != 200:
            raise Exception('return status code is {}'.format(response.status_code))
        result = json.loads(response.text)
        return result['last_price']
    