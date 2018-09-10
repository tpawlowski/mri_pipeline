# MRI Pipeline

## Installation

### Virtualenv

This step is not required, but running this program in python virtual environment separates it from other programs run on the same machine. To install virtualenv follow the [documentation](https://virtualenv.pypa.io/en/stable/installation/).

```
virtualenv -p python3 venv
source venv/bin/activate
```

### Dependencies

```
git clone https://github.com/yeatmanlab/pyAFQ
pip install -r pyAFQ/requirements.txt
pip install ./pyAFQ
pip install -r requirements.txt
```

### Jupyter

```
pip install jupyter

pip install ipykernel
python -m ipykernel install --user --name=venv
```

# Heron
```
virtualenv -p python venv_heron
source venv_heron/bin/activate
pip install -r pyAFQ/requirements.txt
pip install ./pyAFQ
cd pyAFQ
python ./setup.py install
cd -
pip install -r requirements_heron.txt
```

## Local cluster setup

open https://github.com/apache/incubator-heron/releases and download proper heron install script.
```
wget https://github.com/apache/incubator-heron/releases/download/0.17.8/heron-install-0.17.8-darwin.sh
chmod +x heron-*.sh
```

Install in `~/.heron/` with command: 
```
./heron-install-0.17.8-darwin.sh --user
```

Afterwards make sure that `~/bin` is in the path. If you don't want to add just prefix each heron execution with `~/bin/`.

## Building

Heron cluster requires bundling a topology with all its dependencies before submitting. Following command will do that.
```
./pants binary src/python/heron
```