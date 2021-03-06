from heronpy.api.bolt.bolt import Bolt
from sklearn.linear_model import SGDClassifier, PassiveAggressiveClassifier, Perceptron
from sklearn.neural_network import MLPClassifier


class ClassifierBolt(Bolt):
    outputs = ['prediction', 'actual', 'id', 'training_count']

    def initialize(self, config, context):
        self.config = config["sgd_config"].copy()
        if self.config['model'] == 'SGD':
            self.clf = SGDClassifier(loss=self.config['loss'], penalty=self.config['penalty'])
        elif self.config['model'] == 'MLP':
            self.clf = MLPClassifier(hidden_layer_sizes=self.config['hidden_layer_sizes'])
        elif self.config['model'] == 'PassiveAggressive':
            self.clf = PassiveAggressiveClassifier()
        elif self.config['model'] == 'Perceptron':
            self.clf = Perceptron(penalty=self.config['penalty'])

        self.trained_count = 0
        self.pure_training_size = config["benchmark_config"]["pure_training_size"]
        self.results = []

    def process(self, tup):
        id, image_data, classification = tup.values

        x = [image_data]
        if self.trained_count >= self.pure_training_size:
            prediction = self.clf.predict(x)[0]
            self.results.append(prediction == classification)
            self.log("{} prediction {} result: {} (predicted: {}, actual: {}) accuracy: {}%, last 32: {}%".format(
                self.config,
                len(self.results),
                prediction == classification, prediction, classification,
                100 * sum(self.results) // len(self.results),
                100 * sum(self.results[-32:]) // len(self.results[-32:])))
            self.emit([prediction, classification, id, self.trained_count])

        y = [classification]
        self.clf.partial_fit(x, y, classes=['Active', 'Rest'])
        self.trained_count += 1
        self.log("trained {}".format(self.trained_count))
