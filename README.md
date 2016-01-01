# powerlaw

[![Documentation Status](https://readthedocs.org/projects/powerlaw/badge/?version=latest)](http://powerlaw.readthedocs.org/en/latest/?badge=latest)

Power-Law Distribution Analysis based on [Power-law distributions in Empirical data](http://arxiv.org/pdf/0706.1062.pdf) paper.

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

The current implementation supports fitting both continous and discrete data to a powerlaw (using both Linear Regression and Maximum Liklihood Estimator method) and calculating the goodness of fit for the fitted powerlaw. Additionally, there are methods to generate random numbers for powerlaw, exponential and strectched exponenetial series. The complete documentation can be fount [here](https://powerlaw.readthedocs.org).


## References

[Clauset, Aaron, Cosma Rohilla Shalizi, and Mark EJ Newman. "Power-law distributions in empirical data." SIAM review 51.4 (2009): 661-703.](http://arxiv.org/pdf/0706.1062.pdf)

## License

[MIT](http://shagun.mit-license.org/)