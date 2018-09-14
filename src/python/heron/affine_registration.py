import skimage

import AFQ.registration as afr
import numpy as np

from heronpy.api.bolt.bolt import Bolt


class AffineRegistrationBolt(Bolt):
    outputs = ['id', 'features', 'classification']

    def initialize(self, config, context):
        self.reference_image = None
        self.waiting_for_first = []

    def process(self, tup):
        self.log("received tup {}".format(tup.values[0]))
        if self.reference_image is None:
            if tup.values[0] == 'reference':
                _, self.reference_image, self.mask = tup.values
                for values in self.waiting_for_first:
                    self.emit_registered(values)
                self.waiting_for_first = []
            else:
                self.waiting_for_first.append(tup.values)
        else:
            self.emit_registered(tup.values)

    def emit_registered(self, values):
        id, image, classification = values
        registered_image, _ = [image, None] if id == 0 else afr.affine_registration(image, self.reference_image)



        features = skimage.filters.gaussian(registered_image - self.reference_image, sigma=2)[self.mask].flatten()
        self.log("registered image {} {}".format(id, features))
        self.emit([id, features, classification])
