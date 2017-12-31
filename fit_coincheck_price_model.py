from coincheck.price_model import CoincheckPriceModel

PATH = 'data/last_price/bitcoincharts/bitcoincharts-coincheckJPY.csv'


def main():
    model = CoincheckPriceModel()
    model.load(PATH)
    model.fit()


if __name__ == '__main__':
    main()
