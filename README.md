# Debsbom Plugin Examples

This repository provides examples for `debsbom` plugins.

## Plugin Installation

Create a virtual environment, e.g. with virtualenv:

```
virtualenv venv
. venv/bin/activate
```

Then install this plugin which automatically pulls in debsbom in the correct version:

```
pip install .
```

You can verify the installation worked by calling

```
debsbom download -h
```

and checking if the `simple-debian-snapshot` is available as a resolver choice.

## Download Resolver Plugin

An example for a download resolver plugin can be found in `src/debsbom_plugin_examples/resolver.py`. It is a simplified reimplementation of the Debian snapshot mirror resolver that is shipped already in `debsbom`. It is registered as `simple-debian-snapshot`.
