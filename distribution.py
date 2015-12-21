from math import e, log
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
    Lambda : Float/Integer, Lambda constant for exponential distribution.
        Default value is 1.0
    n : Integer, number of elements to be generated.
        Default value is 1
        If n < 0, then unbounded number of elements are generated.
    xmin : Float/Integer, xmin for the exponential distribution.
        Default value is 1.0
        If n < 0, then unbounded number of elements are generated.
    """
    
    def mapping(x):
        return xmin - (1.0/Lambda) * log(1-x)

    for x in random_series(n):
        yield mapping(x)

if __name__ == "__main__":
    for i in exponential_series(Lambda = 1, n = 10):
        print i