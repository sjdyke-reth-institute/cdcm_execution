# Control-oriented Dynamic Computational Modeling (CDCM) Framework

This repository contains packages that are part of the **Control-oriented Dynamic Computational Modeling (CDCM)** framework developed at the [Resilient Extra-Terrestrial Habitats Institute (RETHi)](https://rethi.nd.edu), a NASA-funded Space Technology Research Institute (STRI) under Grant #80NSSC19K1076.

---

## Installation

Installing the `cdcm` package is best done through [conda](https://docs.conda.io/en/latest/). All contents of this package have been tested with **Python 3.9**. Some utilities of the CDCM framework (particularly *model calibration*) depend on [JAX](https://github.com/google/jax), so it is recommended to create a `conda` virtual environment with JAX support.

### 1. Install Conda

To install `conda`, follow the [official instructions](https://conda.io/docs/user-guide/install/).

> _Skip this step if you already have conda installed._

### 2. Install the `cdcm_execution` Package

#### 2.1 Create a CDCM virtual environment

Use the following command to create a `cdcm` virtual environment with Python 3.9 and JAX dependencies:

```bash
conda create -n <cdcm-venv-name> python=3.9 jax jaxlib
conda activate <cdcm-venv-name>
```

#### 2.2 Install from GitHub

Once inside the activated environment, install the `cdcm_execution` package using:

```bash
pip install git+https://github.com/sjdyke-reth-institute/cdcm_execution
```

---

## Citation

If you use this software, please cite it as below:

```bibtex
@software{cdcm_execution_2025,
  author       = {Ilias Bilionis and Murali Krishnan Rajasekharan Pillai},
  title        = {{sjdyke-reth-institute/cdcm_execution: Control-oriented Dynamic Computational Modeling (CDCM) Execution Language}},
  version      = {v0.9.7},
  date         = {2025-07-27},
  doi          = {10.5281/zenodo.16497968},
  url          = {https://doi.org/10.5281/zenodo.16497968}
}
```

You may also cite the associated SSRN publication:

> **Rajasekharan Pillai, Murali Krishnan; Bilionis, Ilias**, *"Control-oriented Dynamic Computational Modeling"*, SSRN, 2025. [https://ssrn.com/abstract/5223568](https://dx.doi.org/10.2139/ssrn.5223568)

Citation metadata is also included in the [CITATION.cff](./CITATION.cff) file in this repository.

---