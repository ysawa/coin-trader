import os
import sys
import numpy as np
from keras.models import load_model
from coincheck.price_model import CoincheckPriceModel
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

CSV_PATH = 'data/last_price/bitcoincharts/bitcoincharts-coincheckJPY.csv'
NUMPY_PATH = 'data/last_price/bitcoincharts/bitcoincharts-coincheckJPY.csv.npy'
MODEL_PATH = 'data/last_price/bitcoincharts/bitcoincharts-coincheckJPY.h5'
PREDICTION_PATH = 'data/last_price/bitcoincharts/bitcoincharts-coincheckJPY-prediction.png'


def main():
    model = CoincheckPriceModel()
    if not os.path.exists(NUMPY_PATH):
        print("making data...")
        model.make_data(CSV_PATH)
    print("making model...")
    model.make_model()
    if '-p' in sys.argv[1:]:
        # prediction
        model.model = load_model(MODEL_PATH)
        data = np.load(NUMPY_PATH)
        sentence_length = model.sentence_length
        turn = 0
        X = np.asarray([data[(sentence_length * turn):(sentence_length * (turn + 1))]])
        Y = data[(sentence_length * (turn + 1)):(sentence_length * (turn + 2))]
        Y_ = []
        for i in range(0, sentence_length):
            predicted = model.predict(X)
            Y_.append(predicted[0])
            X = np.asarray([np.append(X[0][1:sentence_length], predicted, axis=0)])
        Y_ = np.asarray(Y_)
        X_ = np.asarray(data[sentence_length:(sentence_length * 2)])[:, 3]
        plt.plot(np.append(X_, Y_[:, 3], axis=0), label='real')
        plt.plot(np.append(X_, Y[:, 3], axis=0), label='predict')
        plt.savefig(PREDICTION_PATH)

    else:
        print("fitting model...")
        model.fit(NUMPY_PATH)
        print("saving model...")
        model.model.save(MODEL_PATH)


if __name__ == '__main__':
    main()
