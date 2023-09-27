# Control-oriented Dynamic Computational and Modeling (CDCM) Framework

This repository contains packages that are part of the Control-oriented Dynamical Computational and Modeling (CDCM) framework developed at the Resilient Extra-Terrestrial Habitats Institute (RETHi), a NASA funded STRI (Grant #80NSSC19K1076)

# Installation

Installing the `cdcm` package is best done through [conda](https://docs.conda.io/en/latest/). All contents of this package has been tested for Python 3.9. Some utilities of the CDCM framework (particularly _model calibration_) depends on [JAX](https://github.com/google/jax), so it is recommended to create a `conda` virtual environment with JAX to use the code.

## 1- Install Conda
To install `conda` in your workstation, please follow the [installation instructions for `conda`](https://conda.io/docs/user-guide/install/).

Ignore this step if you already have `conda` installed in your system, and is discoverable in your system path.

## 2- Install `cdcm` package


Create a `cdcm` virtual environment for installling the package, with `jax` and `jaxlib`. Currently, we need to install [JAX](https://github.com/google/jax) to utilize all functionalities of the package.

### 2.1- Create a `cdcm` virtual environment

You may execute the following command to create a `cdcm` virtual-environment with Python 3.9 and the `jax`, and `jaxlib` libraries

```
$ conda create -n <cdcm-venv-name> python=3.9 jax jaxlib
```

Activate the virtual environment for the completing the setup procedures

```
$ conda activate <cdcm-venv-name>
```


### 2.2- Install the `cdcm_execution` Python package

Once you activate the `<cdcm-venv-name>` virtual environment, you can install the `cdcm_execution` package into your virtual environment by executing the following command

```
pip install git+https://github.com/sjdyke-reth-institute/cdcm_execution
```

If you need access to the repository, please let email [R Murali Krishnan](mailto:mrajase@purdue.edu).
