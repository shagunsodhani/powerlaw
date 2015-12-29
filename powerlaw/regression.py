import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
from math import pow, e, log, sqrt
from distribution import frequency_distribution, powerlaw_series, random_series
import sys
import random

def least_square_regression(x, y, xlabel = "x", ylabel = "y", prefix="", suffix=""):
    """

    Perform least square regression to find the best fit line and returns the slope of the line.

    **Parameters**
        x : List of values along x axis.
        y : List of values along y axis.   

    """

    X = np.asarray(x).reshape((len(x), 1))
    Y = np.asarray(y).reshape((len(y), 1))
    regr = linear_model.LinearRegression()
    regr.fit(X, Y)

    label_string = "Best fit line, y = "+str(regr.coef_[0][0])+" * x + "+str(regr.intercept_[0])
    print label_string
    print "Residual sum of squares: %.2f" % np.mean((regr.predict(X) - Y) ** 2)
    print "Variance score: %.2f" % regr.score(X, Y)

    # Plot outputs
    original_data, = plt.plot(X, Y,'go', label="original data")
    # best_fit_line, = plt.plot(X, map(lambda x: pow(e, -x), X), 'bo', label=label_string)
    best_fit_line, = plt.plot(X, regr.predict(X), color='blue', linewidth=3, label=label_string)
    plt.title("Least Square Regression"+suffix)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

    curves = [original_data, best_fit_line]
    labels = [curve.get_label() for curve in curves]

    plt.legend(curves, labels)
    plt.savefig(prefix+"least_square_regression_fit"+suffix+".png")
    plt.show()
    return regr.coef_[0][0]

def estimate_scaling_parameter(series, xmin = 1, discrete = False):
    
    """

    Perform Method of Maximum Liklihood (MLE) to find the best fit value of Alpha.

    **Parameters**
    
        series : series of data to be fit.
        xmin : Float/Integer, xmin for the distribution - assumed to be known before-hand. Default value is 1.0
        discrete : Boolean, whether to treat series as discrete or continous. Default value is False

    **Returns**

        Estimated Alpha value.

    """
    
    normalizing_constant = 0.0
    if(discrete):
        normalizing_constant = 0.5
    partial_sum = 0.0
    count = 0.0
    # print series
    for x in series:
        partial_sum += log (x/(xmin - normalizing_constant))
        count+=1
    Alpha = 1.0 + count*(1/partial_sum) 
    return Alpha

def estimate_parameters(series, min_size_series = 50):
    """
    
    Apply Clauset et al.'s method to find the best fit value of xmin and Alpha.

    **Parameters**

        series : series of data to be fit.
        
        min_size_series : Minimum possible size of the distribution to which power-law fit will be attempted. Fitting power-law to a very small series would give biased results where power-law may appear to be a good fit even when data is not drawn from power-law distribution. The default value is taken to be 50 as suggested in the paper.

    **Returns**

        Tuple of (Estimated xmin, Estimated Alpha value).

    """

    sorted_series = sorted(series)
    xmin_candidates = []
    x_prev = sorted_series[0]
    xmin_candidates.append(x_prev)
    for x in sorted_series:
        if(x>x_prev):
            x_prev = x
            xmin_candidates.append(x_prev)

    ks_statistics_min = sys.maxint;
    xmin_result = 0
    Alpha_result = 2
    for xmin in xmin_candidates[:-1*(min_size_series-1)]: 
        data =  filter(lambda x: x>=xmin, sorted_series)
        estimated_Alpha = estimate_scaling_parameter(data, xmin)
        n = len(data)
        Sx = [i[1] for i in frequency_distribution(data, pdf=False)]
        Px = [i[1] for i in frequency_distribution(powerlaw_series(Alpha = estimated_Alpha, n = n, xmin = xmin), pdf = False)]
        ks_statistics = max( map (lambda counter: abs(Sx[counter] - Px[counter]) , range(0, n) ) )
        if(ks_statistics<ks_statistics_min):
            ks_statistics_min = ks_statistics
            xmin_result = xmin
            Alpha_result = estimated_Alpha

    return (xmin_result, Alpha_result)

def generate_dataset(series, xmin, alpha, epsilon = 0.01):

    """
    
    Generator to generate datasets for goodness_of_fit test.

    **Parameters**

        series : series of data on which the power-law model was fitted.

        xmin : xmin for the fitted power-law model.

        alpha : alpha for the fitted power-law model.

        epsilon : desired accuracy in p-value. Default is set to 0.01

    **Returns**

        A generator to generate list of numbers (datasets).

    """
    number_of_datasets = int(round(0.25/(epsilon**2)) +1)
    print number_of_datasets
    n = len(series)
    non_powerlaw_series = filter(lambda x: x<xmin, series)
    ntail = n - len(non_powerlaw_series)
    p = float(ntail)/n
    # print p
    # print ntail
    # print n

    for i in range(0, number_of_datasets):
        dataset = []
        count_powerlaw_series = 0
        # how many numbers are to be picked from powerlaw distribution
        for random_number in random_series(n):
            if(random_number<=p):
                count_powerlaw_series+=1
                # generate number from power-law distribution
            else:
                # pick number from non_powerlaw_series
              dataset.append(random.choice(non_powerlaw_series))
        
        dataset = dataset + [i for i in powerlaw_series(Alpha = alpha, xmin = xmin, n = count_powerlaw_series)]

        yield dataset


if __name__ == "__main__":
    n = 100
    data = [i for i in powerlaw_series(n=n, xmin = 20, Alpha = 2.6)]
    # print data
    (xmin, alpha) = estimate_parameters(data, min_size_series = 100)
    # print "xmin = "+str(xmin)
    # print "alpha = "+str(alpha)
    for i in generate_dataset(series=data, xmin=xmin, alpha=alpha, epsilon = 0.1):
        print i