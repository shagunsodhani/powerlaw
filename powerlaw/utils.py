def unique(series):
    """

    Generator to generate all unique values from the input series, in the order they appear for the first time.

    **Parameters**

        series : Input series.

    """

    occured = set()

    for element in series:
        if element not in occured:
            occured.add(element)
            yield element