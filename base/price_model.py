
class BasePriceModel:
    model = None

    def fit(self):
        self.model.fit()

    def load(self, path):
        """

        :param str path:
        """
        pass

    def make_model(self):
        """

        :rtype: keras.models.Sequential
        """
        return None
    