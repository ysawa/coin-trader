import os
import sys
import numpy as np
from keras.models import load_model
from coincheck.price_model import CoincheckPriceModel
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
        loaded_model = load_model(MODEL_PATH)
        data = np.load(NUMPY_PATH)
        X = np.asarray([data[0:model.sentence_length]])
        Y = data[model.sentence_length:(model.sentence_length * 2)]
        print(Y[:,3])
        Y_ = []
        for i in range(0, model.sentence_length):
            X = X / X[0][0]
            predicted = loaded_model.model.predict(X)
            Y_.append((predicted * data[i][0])[0])
            X = np.asarray([np.append(X[0][1:model.sentence_length], predicted, axis=0)])
        Y_ = np.asarray(Y_)
        X_ = np.asarray(data[0:model.sentence_length])[:,3]
        plt.plot(np.append(X_, Y_[:,3], axis=0))
        plt.plot(np.append(X_, Y[:,3], axis=0))
        plt.savefig(PREDICTION_PATH)

    else:
        print("fitting model...")
        model.fit(NUMPY_PATH)
        print("saving model...")
        model.model.save(MODEL_PATH)


if __name__ == '__main__':
    main()
