from math import e, log, pow
from random import random

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
        yield mapping(x)


if __name__ == "__main__":
    for i in stretched_exponential_series(n = 10):
        print i