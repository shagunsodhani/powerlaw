import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt
from scipy.special import zeta

from .distribution import frequency_distribution, powerlaw_series, random_series
from .utils import unique

from math import pow, e, log, sqrt
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
    print(label_string)
    print("Residual sum of squares: %.2f" % np.mean((regr.predict(X) - Y) ** 2))
    print("Variance score: %.2f" % regr.score(X, Y))

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
        discrete : Boolean, whether to treat series as discrete or continous. Default value is False.

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

def estimate_parameters(series, min_size_series = 50, discrete = False):
    """
    
    Apply Clauset et al.'s method to find the best fit value of xmin and Alpha.

    **Parameters**

        series : series of data to be fit.
        
        min_size_series : Minimum possible size of the distribution to which power-law fit will be attempted. Fitting power-law to a very small series would give biased results where power-law may appear to be a good fit even when data is not drawn from power-law distribution. The default value is taken to be 50 as suggested in the paper.

        discrete : Boolean, whether to treat series as discrete or continous. Default value is False

    **Returns**

        Tuple of (Estimated xmin, Estimated Alpha value, minimum KS statistics score).

    """

    sorted_series = sorted(series)
    xmin_candidates = []
    x_prev = sorted_series[0]
    xmin_candidates.append(x_prev)
    for x in sorted_series:
        if(x>x_prev):
            x_prev = x
            xmin_candidates.append(x_prev)

    ks_statistics_min = sys.maxsize;
    xmin_result = 0
    Alpha_result = 2
    for xmin in xmin_candidates[:-1*(min_size_series-1)]: 
        data =  [x for x in sorted_series if x>=xmin]
        estimated_Alpha = estimate_scaling_parameter(data, xmin)
        if(discrete):
            Px = [zeta(estimated_Alpha, x)/zeta(estimated_Alpha, xmin) for x in unique(data)]
        else:
            Px = [pow(float(x)/xmin, 1 - estimated_Alpha ) for x in unique(data)]
        n = len(Px)
        Sx = [i[1]/n for i in frequency_distribution(data, pdf=False)]
        ks_statistics = max( [abs(Sx[counter] - Px[counter]) for counter in range(0, n)] )
        if(ks_statistics<ks_statistics_min):
            ks_statistics_min = ks_statistics
            xmin_result = xmin
            Alpha_result = estimated_Alpha

    return (xmin_result, Alpha_result, ks_statistics_min)

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
    print(number_of_datasets)
    n = len(series)
    non_powerlaw_series = [x for x in series if x<xmin]
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

def goodness_of_fit(series, xmin, alpha, ks_statistics, epsilon = 0.01, min_size_series = 50):

    """
    
    Function to calculate the p-value as a measure of goodness_of_fit for the fitted model.

    **Parameters**

        series : series of data on which the power-law model was fitted.

        xmin : xmin for the fitted power-law model.

        alpha : alpha for the fitted power-law model.

        ks_statistics : KS statistics for the fitted power-law model.

        epsilon : desired accuracy in p-value. Default is set to 0.01.

        min_size_series : Minimum possible size of the distribution to which power-law fit will be attempted. This value is used when fitting power-law to the generated datasets. The default value is taken to be 50. For further details, see `estimate_parameters()`.

    **Returns**

        p-value for the fitted model.

    """

    count_dataset = 0.0
    # number of synthetic datasets tested
    n1 = 0.0
    # number of synthetic datasets where ks value is greater than ks value for given data 
    for dataset in generate_dataset(series=series, xmin=xmin, alpha=alpha, epsilon=epsilon):
        count_dataset+=1.0
        (xmin_dataset, alpha_dataset, ks_statistics_dataset) = estimate_parameters(series=dataset, min_size_series = min_size_series)
        if(ks_statistics_dataset>ks_statistics):
            n1+=1.0
    return n1/count_dataset


if __name__ == "__main__":
    n = 10
    data = [i for i in powerlaw_series(n=n, xmin = 20, Alpha = 2.6)]
    # print data
    (xmin, alpha, ks_statistics) = estimate_parameters(series=data, min_size_series = 5)
    print("xmin = "+str(xmin))
    print("alpha = "+str(alpha))

    print(goodness_of_fit(series=data, xmin=xmin, alpha=alpha, ks_statistics=ks_statistics, epsilon = 0.01, min_size_series = 50))
