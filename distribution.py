from math import e, log, pow
from random import random
from regression import least_square_regression
import matplotlib.pyplot as plt

def random_series(n = 1):
    """
    Generator to generate a stream of random numbers.

    Parameters
    ----------
    n : Integer, number of elements to be generated.
        Default value is 1
        If n < 0, then unbounded number of elements are generated.
    """
    if(n>-1):
        for i in range(n):
            yield random()
    else:
        while True:
            yield random()

def exponential_series(Lambda = 1.0, n = 1, xmin = 1.0):
    """
    Generator to generate a stream of numbers taken from exponential distribution.

    Parameters
    ----------
    Lambda : Float/Integer, Lambda constant for the distribution.
        Default value is 1.0
    n : Integer, number of elements to be generated.
        Default value is 1
        If n < 0, then unbounded number of elements are generated.
    xmin : Float/Integer, xmin for the distribution.
        Default value is 1.0
    """
    
    def mapping(x):
        return xmin - (1.0/Lambda) * log(1-x)

    for x in random_series(n):
        yield mapping(x)

def stretched_exponential_series(Lambda = 1.0, Beta = 1.0, n = 1, xmin = 1.0):
    """
    Generator to generate a stream of numbers taken from stretched exponential distribution.

    Parameters
    ----------
    Lambda : Float/Integer, Lambda constant for the distribution.
        Default value is 1.0
    Beta : Float/Integer, Beta constant for the distribution.
        Default value is 1.0
    n : Integer, number of elements to be generated.
        Default value is 1
        If n < 0, then unbounded number of elements are generated.
    xmin : Float/Integer, xmin for the distribution.
        Default value is 1.0
    """
    
    def mapping(x):
        return pow( pow(xmin, Beta)-(1.0/Lambda)*log(1.0-x), 1.0/Beta )

    for x in random_series(n):
        yield mapping(x)

def powerlaw_series(Alpha = 2.0, n = 1, xmin = 1.0):
    """
    Generator to generate a stream of numbers taken from powerlaw distribution.

    Parameters
    ----------
    Alpha : Float/Integer, Alpha constant for the distribution.
        Default value is 2.0
        Alpha value should be greater than 1.0
    n : Integer, number of elements to be generated.
        Default value is 1
        If n < 0, then unbounded number of elements are generated.
    xmin : Float/Integer, xmin for the distribution.
        Default value is 1.0
    """
    
    def mapping(x):
        return xmin * pow( (1.0-x), -1.0/(Alpha - 1.0) )

    for x in random_series(n):
        yield int(mapping(x))

def frequency_distribution(series, pdf = True):
    """
    Generator to generates pdf(probability distribution function) or cdf(cummulative distribution function) of any series.

    Parameters
    ----------
    series : list of values.

    pdf : Boolean. If True, return pdf else cdf
        Default value is True

    Returns
    -------
    (key, value) pairs are returned where key is one of the entries from the input series and value is the corresponding pdf for the key. 
        The pairs are sorted by key.
    """

    sorted_series = sorted(series)
    key_to_return = -1
    value_to_return = 0
    for key in sorted_series:
        if(key>key_to_return and key_to_return!=-1):
            yield (key_to_return, value_to_return)
            key_to_return = key
            if(pdf):
                value_to_return = 1
            else:
                value_to_return+=1
        else:
            key_to_return = key
            value_to_return+=1
    yield (key_to_return, value_to_return)


def plot_f_series(series):
    """
    Plots pdf(probability distribution function) for any series.

    Parameters
    ----------
    series : list of values.

    Returns
    -------
    Log log plot of the values.
    """
    # sorted_series = sorted(series)
    x = []
    y = []

    for (key, value) in pdf(series):
        x.append(key)
        y.append(value)
    plt.loglog(x, y,'go', label="original data")
    plt.show()



if __name__ == "__main__":
    n = 10
    # series = powerlaw_series(n = n, xmin = 3, Alpha = 4)
    series = [i for i in frequency_distribution(sorted([int(i) for i in powerlaw_series(n = n, xmin = 2, Alpha = 2.6)]), pdf=False)]
    #e print y
    print series

        