from base.foot import Foot

UNIT_TIME = 5 * 60


class Foots:

    def __init__(self):
        self.foots = dict()

    def add(self, time, price):
        foot_hash = self.get_foot_hash(time)
        if foot_hash in self.foots:
            self.foots[foot_hash].add_price(price)
        else:
            foot = Foot(time, price)
            self.foots[foot_hash] = foot

    def get_foot_hash(self, time):
        """

        :rtype: int
        """
        return int(time / UNIT_TIME)
