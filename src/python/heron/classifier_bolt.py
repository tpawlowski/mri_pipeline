from heronpy.api.bolt.bolt import Bolt
from sklearn.linear_model import SGDClassifier


class ClassifierBolt(Bolt):
    outputs = ['prediction', 'actual', 'id', 'training_count']

    def initialize(self, config, context):
        self.clf = SGDClassifier()
        self.trained_count = 0
        self.pure_training_size = config["benchmark_config"]["pure_training_size"]
        self.results = []

    def process(self, tup):
        id, image_data, classification = tup.values

        x = [image_data]
        if self.trained_count >= self.pure_training_size:
            prediction = self.clf.predict(x)[0]
            self.results.append(prediction == classification)
            self.log("prediction: {} (predicted: {}, actual: {}) accuracy: {}%, last 32: {}%".format(
                prediction == classification, prediction, classification,
                100 * sum(self.results) // len(self.results),
                100 * sum(self.results[-32:]) // len(self.results[-32:])))
            self.emit([prediction, classification, id, self.trained_count])

        y = [classification]
        self.clf.partial_fit(x, y, classes=['Active', 'Rest'])
        self.trained_count += 1
        self.log("trained {}".format(self.trained_count))
