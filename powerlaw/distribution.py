from math import e, log, pow
from random import random
import matplotlib.pyplot as plt

def random_series(n = 1):
    """

    Generator to generate a stream of random numbers.

    **Parameters**
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

def exponential_series(Lambda = 1.0, n = 1, xmin = 1.0, discrete = False):
    """

    Generator to generate a stream of numbers taken from exponential distribution.

    **Parameters**
    
        Lambda : Float/Integer, Lambda constant for the distribution.
            Default value is 1.0

        n : Integer, number of elements to be generated.
            Default value is 1
            If n < 0, then unbounded number of elements are generated.

        xmin : Float/Integer, xmin for the distribution.
            Default value is 1.0
        
        discrete : Boolean, Whether the distribution is to be discrete or not (continous).
            Default value is False

    """
    
    def mapping(x):
        return xmin - (1.0/Lambda) * log(1-x)

    if discrete:
        xmin = xmin - 0.5
        for x in random_series(n):
            yield int(round(mapping(x)))

    else:
        for x in random_series(n):
            yield mapping(x)

def stretched_exponential_series(Lambda = 1.0, Beta = 1.0, n = 1, xmin = 1.0, discrete = False):
    """

    Generator to generate a stream of numbers taken from stretched exponential distribution.

    **Parameters**

        Lambda : Float/Integer, Lambda constant for the distribution.
            Default value is 1.0

        Beta : Float/Integer, Beta constant for the distribution.
            Default value is 1.0

        n : Integer, number of elements to be generated.
            Default value is 1
            If n < 0, then unbounded number of elements are generated.

        xmin : Float/Integer, xmin for the distribution.
            Default value is 1.0

        discrete : Boolean, Whether the distribution is to be discrete or not (continous).
            Default value is False

    """
    
    def mapping(x):
        return pow( pow(xmin, Beta)-(1.0/Lambda)*log(1.0-x), 1.0/Beta )

    if discrete:
        xmin = xmin - 0.5
        for x in random_series(n):
            yield int(round(mapping(x)))
    else:
        for x in random_series(n):
            yield mapping(x)

def powerlaw_series(Alpha = 2.0, n = 1, xmin = 1.0, discrete = False):
    """
    
    Generator to generate a stream of numbers taken from powerlaw distribution.

    **Parameters**

        Alpha : Float/Integer, Alpha constant for the distribution.
            Default value is 2.0
            Alpha value should be greater than 1.0

        n : Integer, number of elements to be generated.
            Default value is 1
            If n < 0, then unbounded number of elements are generated.

        xmin : Float/Integer, xmin for the distribution.
            Default value is 1.0

        discrete : Boolean, Whether the distribution is to be discrete or not (continous).
            Default value is False

    """
    
    def mapping(x):
        return xmin * pow( (1.0-x), -1.0/(Alpha - 1.0) )

    if discrete:
        xmin = xmin - 0.5
        for x in random_series(n):
            yield int(round(mapping(x)))
    else:
        for x in random_series(n):
            yield mapping(x)

def frequency_distribution(series, pdf = True, ccdf = True):
    """

    Generator to generates pdf(probability distribution function) or cdf(cummulative distribution function) or ccdf(complementary cummulative distribution function) of any series.

    **Parameters**

        series : list of values.

        pdf : Boolean. If True, return pdf else cdf
            Default value is True

        ccdf : Boolean. This is considered only if pdf is set to False. If ccdf = True, return ccdf else cdf
            Default value is True

    **Returns**
        
        (key, value) pairs are returned where key is one of the entries from the input series and value is the corresponding pdf for the key. 
        The pairs are sorted by key.

    """

    sorted_series = sorted(series)
    key_to_return = -1

    if(pdf==True or ccdf==False):
        
        if(pdf==True):
            def update_value (value):
                return 1
        else:
            def update_value (value):
                return value+1
        
        value_to_return = 0
        for key in sorted_series:
        # print key
            if(key>key_to_return and key_to_return!=-1):
                yield (key_to_return, value_to_return)
                key_to_return = key
                value_to_return = update_value(value_to_return)
            else:
                key_to_return = key
                value_to_return+=1
        yield (key_to_return, value_to_return)

    else:
        count = len(sorted_series)
        # print sorted_series
        value_to_deduct = 0
        for key in sorted_series:
            if(key>key_to_return and key_to_return!=-1):
                yield (key_to_return, count)
                count -=value_to_deduct
                key_to_return = key
                value_to_deduct = 1
            else:
                key_to_return = key
                value_to_deduct+=1
        yield (key_to_return, count)

def plot_pdf_series(series):
    """

    Plots pdf(probability distribution function) for any series.

    **Parameters**
        series : list of values.

    **Returns**
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
    n = 100000
    # series = powerlaw_series(n = n, xmin = 3, Alpha = 4)
    # series = [i for i in frequency_distribution(sorted([int(i) for i in powerlaw_series(n = n, xmin = 2, Alpha = 2.6)]), pdf=False)]
    #e print y
    # print series
    # for j in frequency_distribution([int(i) for i in powerlaw_series(n=n, xmin = 2, Alpha = 2.6)], pdf=False, ccdf=True):
        # print j
    # print estimate_scaling_parameter(powerlaw_series(n=n, xmin = 2, Alpha = 2.6), xmin = 2, discrete=False)
    # estimate_parameters(powerlaw_series(n=n, xmin = 2, Alpha = 2.6))