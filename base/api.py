
class BaseApi:
    def request_balance(self):
        pass

    def request_last_price(self, currency_pair=None):
        pass

    def request_trade(self, amount, is_ask, price=None, currency_pair=None, **options):
        pass
