from heronpy.api.bolt.bolt import Bolt


class VotingBolt(Bolt):
    outputs = ['prediction', 'actual', 'id', 'training_count']

    def initialize(self, config, context):
        self.classifier_count = config["classifier_count"]
        self.predictions = {}
        self.results = []

    def process(self, tup):
        prediction, classification, id, _ = tup.values

        if id not in self.predictions:
            self.predictions[id] = {'Active': 0, 'Rest': 0}

        self.predictions[id][prediction] += 1

        if self.predictions[id]['Active'] + self.predictions[id]['Rest'] == self.classifier_count:
            prediction = 'Active' if self.predictions[id]['Active'] > self.predictions[id]['Rest'] else 'Rest'
            self.results.append(prediction == classification)
            self.log("voting prediction {} result: {} (predicted: {}, actual: {}) accuracy: {}%, last 32: {}%".format(
                len(self.results),
                prediction == classification, prediction, classification,
                100 * sum(self.results) // len(self.results),
                100 * sum(self.results[-32:]) // len(self.results[-32:])))
            self.emit([prediction, classification, id, self.classifier_count])
