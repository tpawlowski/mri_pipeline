python_library(
    name = "spouts-bolts-py",
    sources=globs('*.py', exclude=[['topology.py']]),
)

python_binary(
    name = "heron",
    source='topology.py',
    dependencies = [
        ':spouts-bolts-py',
        '3rdparty/python:heronpy',
        '3rdparty/python:six',
        '3rdparty/python:protobuf',
        '3rdparty/python:numpy',
        '3rdparty/python:scikit-image',
        '3rdparty/python:boto3',
        '3rdparty/python:nilearn',
        '3rdparty/python:sklearn',
        '3rdparty/python:pyAFQ'
    ],
)
