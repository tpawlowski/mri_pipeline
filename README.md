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
pip install -r requirements.txt
```

### Jupyter

```
pip install jupyter

pip install ipykernel
python -m ipykernel install --user --name=venv
```
