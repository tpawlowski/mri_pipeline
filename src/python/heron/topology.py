import os.path as op

from heronpy.api.stream import Grouping
from heronpy.api.topology import TopologyBuilder

from image_spout import ImageSpout

from affine_registration import AffineRegistrationBolt
from classifier_bolt import ClassifierBolt
from mask_bolt import MaskBolt
from cross_validation_bolt import CrossValidationBolt
from voting_bolt import VotingBolt


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
                                 pure_training_size=10,
                                 shuffle_seed=1,  # 1 for no shuffle, 1000000007 for a nice random
                                 )
    }

    builder = TopologyBuilder("heron")

    # Load demo data (without loading whole file at once) (nibabel - mmap) (with classification results)
    image_spout = builder.add_spout("image_spout", ImageSpout, par=1, config=config)

    # Optional: low/er down the resolution

    # Affine registration - fixing possible moves or rotations (multicore)
    mask_bolt = builder.add_bolt("mask_bolt", MaskBolt, par=1, config=config,
                                 inputs={image_spout: Grouping.ALL})

    affine_registration_bolt = builder.add_bolt("affine_registration_bolt", AffineRegistrationBolt, par=6, config=config,
                                                inputs={mask_bolt: Grouping.ALL,
                                                        image_spout: Grouping.SHUFFLE})

    classifiers = []

    model = 'SGD'
    for loss in ['hinge', 'log', 'modified_huber']:
        for penalty in ['l1', 'elasticnet']:
            config["sgd_config"] = {'model': model, 'loss': loss, 'penalty': penalty}
            classifiers.append(builder.add_bolt("classifier_{}_{}_{}".format(model, loss, penalty), ClassifierBolt, par=1, config=config.copy(),
                                                inputs={affine_registration_bolt: Grouping.SHUFFLE}))
            builder.add_bolt("validation_{}_{}_{}".format(model, loss, penalty), CrossValidationBolt, par=1,
                             config=config.copy(),
                             inputs={affine_registration_bolt: Grouping.SHUFFLE})

    for hidden_layer_sizes in [(100,), (200,), (300,), (500,), (200, 100), (300, 200)]:
        config["sgd_config"] = {'model': 'MLP', 'hidden_layer_sizes': hidden_layer_sizes}
        classifiers.append(builder.add_bolt("classifier_MLP_{}".format('x'.join(map(str, list(hidden_layer_sizes)))), ClassifierBolt, par=1, config=config.copy(),
                           inputs={affine_registration_bolt: Grouping.SHUFFLE}))
        builder.add_bolt("validation_MLP_{}".format('x'.join(map(str, list(hidden_layer_sizes)))), CrossValidationBolt,
                         par=1, config=config.copy(),
                         inputs={affine_registration_bolt: Grouping.SHUFFLE})

    # for model in ['PassiveAggressive']:
    #     config["sgd_config"] = {'model': model}
    #     classifiers.append(builder.add_bolt("classifier_{}".format(model), ClassifierBolt, par=1, config=config.copy(),
    #                        inputs={affine_registration_bolt: Grouping.SHUFFLE}))
    #     builder.add_bolt("validation_{}".format(model), CrossValidationBolt, par=1, config=config.copy(),
    #                      inputs={affine_registration_bolt: Grouping.SHUFFLE})

    # model = 'Perceptron'
    # for penalty in ['l1', 'l2', 'elasticnet']:
    #     config["sgd_config"] = {'model': model, 'penalty': penalty}
    #     classifiers.append(builder.add_bolt("classifier_{}_{}".format(model, penalty), ClassifierBolt, par=1, config=config.copy(),
    #                                         inputs={affine_registration_bolt: Grouping.SHUFFLE}))
    #     builder.add_bolt("validation_{}_{}".format(model, penalty), CrossValidationBolt, par=1, config=config.copy(),
    #                      inputs={affine_registration_bolt: Grouping.SHUFFLE})

    del config["sgd_config"]
    config["classifier_count"] = len(classifiers)
    voting_bolt = builder.add_bolt("voting_bolt", VotingBolt, par=1, config=config,
                                   inputs=dict(zip(classifiers, [Grouping.ALL] * len(classifiers))))

    config["sgd_config"] = {'model': 'SVC'}
    builder.add_bolt("validation_{}".format('SVC'), CrossValidationBolt, par=1, config=config.copy(),
                     inputs={affine_registration_bolt: Grouping.SHUFFLE})

    builder.build_and_submit()
