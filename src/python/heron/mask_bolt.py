from dipy.segment.mask import median_otsu
from heronpy.api.bolt.bolt import Bolt


class MaskBolt(Bolt):
    outputs = ['id', 'mri', 'mask']

    def initialize(self, config, context):
        pass

    def process(self, tup):
        if tup.values[0] == 0:
            image_data = tup.values[1]
            _, mask = median_otsu(image_data, 4, 2, False, dilate=1)
            self.log("emitting mask with shap {} edge: {} center: {}".format(mask.shape, mask[0][0][0], mask[32, 32, 15]))
            self.emit(['reference', image_data, mask])
