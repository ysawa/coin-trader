import os

from base.save_last_price import save_last_price
from bitflyer.api import BitflyerApi


DIRECTORY = os.path.join("data", "last_price", "bitflyer")


def main():
    api = BitflyerApi()
    save_last_price(api, DIRECTORY)


if __name__ == '__main__':
    main()
