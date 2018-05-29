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
