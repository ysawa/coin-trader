import os

from base.save_last_price import save_last_price
from zaif.api import ZaifApi

DIRECTORY = os.path.join("data", "last_price", "zaif")


def main():
    api = ZaifApi()
    save_last_price(api, DIRECTORY)


if __name__ == '__main__':
    main()
