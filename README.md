# powerlaw

[![Documentation Status](https://readthedocs.org/projects/powerlaw/badge/?version=latest)](http://powerlaw.readthedocs.org/en/latest/?badge=latest)

[![DOI](https://zenodo.org/badge/48375467.svg)](https://zenodo.org/badge/latestdoi/48375467)


Power-Law Distribution Analysis based on [Power-law distributions in Empirical data](http://arxiv.org/pdf/0706.1062.pdf) paper ([Summary](/paper/README.md)).

## Basic use


```
from powerlaw.regression import estimate_parameters, goodness_of_fit

data = [1.1, 2.2, ...]

(xmin, alpha, ks_statistics) = estimate_parameters(data)

p_value = goodness_of_fit(series, xmin, alpha, ks_statistics)
```

## Install

```
sudo pip install git+https://github.com/shagunsodhani/powerlaw.git
```

#### Alternatively

```
git clone https://github.com/shagunsodhani/powerlaw.git

cd powerlaw

sudo python setup.py install
```

## Features

The current implementation supports fitting both continuous and discrete data to a power-law (using both Linear Regression and Maximum Likelihood Estimator method) and calculating the goodness of fit for the fitted power-law. Additionally, there are methods to generate random numbers for power-law, exponential and stretched exponential series. The complete documentation can be found [here](https://powerlaw.readthedocs.org).

A short summary of the paper can be found [here](/paper/README.md).

## References

[Clauset, Aaron, Cosma Rohilla Shalizi, and Mark EJ Newman. "Power-law distributions in empirical data." SIAM review 51.4 (2009): 661-703.](http://arxiv.org/pdf/0706.1062.pdf)

## License

[MIT](http://shagun.mit-license.org/)
