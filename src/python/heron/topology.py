import os.path as op

from heronpy.api.stream import Grouping
from heronpy.api.topology import TopologyBuilder

from image_spout import ImageSpout

from affine_registration import AffineRegistrationBolt
from classifier_bolt import ClassifierBolt
from mask_bolt import MaskBolt

if __name__ == '__main__':
    """
    Aim: Select part of the brain image which activity is correlated with the classification.
    
    Parameters: 
    p: float fraction of data which should be taken into consideration. Maybe it would be better to take a threshold. 
    stable_threshold: Number of iteration for which set of voxels were not changed.
    """

    config = {
        "benchmark_config": dict(data_path=op.join(op.expanduser('~'), 'data', 'rtfmri', 'func_0000.nii.gz'),
                                 classes_path=op.join(op.expanduser('~'), 'data', 'rtfmri', 'timingFiles', 'fullRunLabels.txt'),
                                 pure_training_size=10)
    }

    builder = TopologyBuilder("heron")

    # Load demo data (without loading whole file at once) (nibabel - mmap) (with classification results)
    image_spout = builder.add_spout("image_spout", ImageSpout, par=1, config=config)

    # Optional: low/er down the resolution

    # Affine registration - fixing possible moves or rotations (multicore)
    mask_bolt = builder.add_bolt("mask_bolt", MaskBolt, par=1, config=config,
                                 inputs={image_spout: Grouping.ALL})

    affine_registration_bolt = builder.add_bolt("affine_registration_bolt", AffineRegistrationBolt, par=7, config=config,
                                                inputs={mask_bolt: Grouping.ALL,
                                                        image_spout: Grouping.SHUFFLE})

    classifier_bolt = builder.add_bolt("classifier_bolt", ClassifierBolt, par=1, config=config,
                                       inputs={affine_registration_bolt: Grouping.SHUFFLE})

    builder.build_and_submit()
