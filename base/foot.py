
class Foot:
    closing = None
    high = None
    low = None
    opening = None

    def __init__(self, time, price):
        """

        :param int time: unix time
        """
        self.time = time
        self.opening = price
        self.high = price
        self.low = price
        self.closing = price

    def add_price(self, price):
        self.closing = price
        if self.high < price:
            self.high = price
            return
        if price < self.low:
            self.low = price
            return
