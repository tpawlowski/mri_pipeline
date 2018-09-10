import nibabel as nib
import pandas as pd
from heronpy.api.spout.spout import Spout


class ImageSpout(Spout):
    """
    Spout fetching mri image from hcp (if necessary) and outputting one image at a time with classification results.

    Based on http://nipy.org/nibabel/images_and_memory.html#saving-time-and-memory this approach should work efficient,
    which means it should load lazily parts of the image.
    """
    outputs = ['id', 'mri', 'classification']

    def initialize(self, config, context):
        self.data = nib.load(config["benchmark_config"]["data_path"])
        self.classes = pd.read_csv(config["benchmark_config"]["classes_path"], header=None)

        self.iterator = 0
        self.emit_count = 0

    def next_tuple(self):
        while self.iterator < self.data.shape[-1]:
            classification = self.classes.iat[self.iterator, 0]
            if classification in ['Rest', 'Active']:
                self.log("emit {} with image {} of class {}".format(self.emit_count, self.iterator, classification))
                self.emit([self.emit_count, self.data.dataobj[..., self.iterator], classification])
                self.emit_count += 1
                self.iterator += 1
                break
            else:
                self.log("skipping {} of class {}".format(self.iterator, classification))
                self.iterator += 1
