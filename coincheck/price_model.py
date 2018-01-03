from datetime import datetime
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop, Adamax
from keras.utils.data_utils import get_file
import numpy as np
import random, sys

from sklearn import model_selection

from base.foots import Foots
from base.price_model import BasePriceModel
import pytz


class CoincheckPriceModel(BasePriceModel):

    def __init__(self):
        self.sentence_length = 288

    def fit(self, path):
        data = np.load(path)
        data_length = len(data)
        sentences_count = data_length - self.sentence_length
        print('data length:', data_length)
        print('sentences count:', sentences_count)
        X = []
        y = []
        for sentence_index in range(0, sentences_count):
            x = data[sentence_index:sentence_index + self.sentence_length]
            max_x = np.max(x)
            X.append(x / max_x)
            y_ = data[sentence_index + self.sentence_length]
            y.append(y_ / max_x)
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64)
        self.model.fit(X, y, batch_size=128, epochs=1)
        score = self.model.evaluate(X, y)
        print('score:', score)

    def make_data(self, path, limit=None):
        foots = Foots()
        file = open(path)
        count = 0
        while True:
            line = file.readline()
            if not line:
                break
            line = line.strip()
            csv = line.split(',')
            time = int(csv[0])
            last_price = float(csv[1])
            foots.add(time, last_price)
            if limit and count > limit:
                break
            count += 1
        file.close()
        foot_hashes = list(foots.foots.keys())
        first_foot_hash = foot_hashes[0]
        last_foot_hash = foot_hashes[-1]
        foot = None
        data = []
        for foot_hash in range(first_foot_hash, last_foot_hash + 1):
            if foot_hash in foots.foots:
                foot = foots.foots[foot_hash]
            data.append(foot.array)
        np.save(path, np.asarray(data))

    def make_model(self):
        model = Sequential()
        lstm = LSTM(128, input_shape=(self.sentence_length, 4))
        model.add(lstm)
        model.add(Activation('relu'))
        model.add(Dropout(0.5))
        model.add(Dense(128))
        model.add(Dense(4))
        optimizer = Adamax()
        model.compile(loss='mean_squared_error', optimizer=optimizer)
        self.model = model
        return self.model
