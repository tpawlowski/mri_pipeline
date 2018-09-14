import numpy
from heronpy.api.bolt.bolt import Bolt
from sklearn.model_selection import KFold, cross_val_score
from sklearn.linear_model import SGDClassifier, PassiveAggressiveClassifier, Perceptron
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC


class CrossValidationBolt(Bolt):
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
        elif self.config['model'] == 'SVC':
            self.clf = SVC(kernel='linear', C=100, probability=True)

        self.data = []
        self.labels = []
        self.pure_training_size = config["benchmark_config"]["pure_training_size"]

    def process(self, tup):
        id, image_data, classification = tup.values

        self.data.append(image_data)
        self.labels.append(classification)

        if len(self.data) >= self.pure_training_size and len(self.data) % 10 == 8:
            cv = KFold(n_splits=5)
            cv_score = cross_val_score(self.clf, self.data, self.labels, cv=cv)
            self.log('{} {} mean crossval acc: {}, stdDev: {}'.format(len(self.data), self.config, numpy.mean(cv_score), numpy.std(cv_score)))
