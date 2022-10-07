# Mimos

## Development setup

Create a virtual environment and activate it

```
$ python3.10 -m venv venv
$ source venv/bin/activate
```

Install an editable version of the package

```
$ pip install -e .
```

## Build

Make sure you have the lates version of PyPA's [build](https://packaging.python.org/en/latest/key_projects/#build) installed:

```
$ pip install --upgrade build
```

Run the following to build the wheels

```
python -m build
```
