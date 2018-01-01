import os

from coincheck.price_model import CoincheckPriceModel

CSV_PATH = 'data/last_price/bitcoincharts/bitcoincharts-coincheckJPY.csv'
NUMPY_PATH = 'data/last_price/bitcoincharts/bitcoincharts-coincheckJPY.csv.npy'
MODEL_PATH = 'data/last_price/bitcoincharts/bitcoincharts-coincheckJPY.h5'


def main():
    model = CoincheckPriceModel()
    if not os.path.exists(NUMPY_PATH):
        print("making data...")
        model.make_data(CSV_PATH)
    print("making model...")
    model.make_model()
    print("fitting model...")
    model.fit(NUMPY_PATH)
    print("saving model...")
    model.model.save(MODEL_PATH)


if __name__ == '__main__':
    main()
