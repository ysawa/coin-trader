from datetime import datetime
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy as np
import random, sys

from base.foots import Foots
from base.price_model import BasePriceModel
import pytz



SENTENCE_LENGTH = 20
step = 3


class CoincheckPriceModel(BasePriceModel):

    def __init__(self):
        self.foots = Foots()
        self.model = self.make_model()

    def load(self, path):
        file = open(path)
        timezone = pytz.timezone('Asia/Tokyo')
        count = 0
        while True:
            line = file.readline()
            if not line:
                break
            line = line.strip()
            csv = line.split(',')
            time = int(csv[0])
            last_price = float(csv[1])
            self.foots.add(time, last_price)
            time = datetime.fromtimestamp(time, timezone)
            if count > 100:
                break
            count += 1
        for foot_hash, foot in self.foots.foots.items():
            print(foot)
            print(foot.time, foot.opening, foot.high, foot.low, foot.closing)
        file.close()

    def make_model(self):
        model = Sequential()
        lstm = LSTM(1, input_shape=(1, 10))
        model.add(lstm)
