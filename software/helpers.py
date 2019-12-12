import numpy as np


def sample_generator(a, lookback=1, delay=1, start=None, end=None, target_col=3, flatten=True):
    """
    Get a generator of for iterating over the array with given batch and step.

    :param a: array
    :param batch: batch size
    :param delay: step length
    :param start: start index
    :param end: end index
    :target_col: target column
    flatten: bool, flatten the sample
    :return: array and float
    """
    assert len(a) > lookback, "Length of array must be larger than batch size"
    assert lookback > 0 and delay > 0, "Batch and step must be positive"
    if start:
        a = a[start:]
    if end:
        a = a[: end + lookback + delay - 1]
    a = np.array(a)
    i = lookback
    while i < len(a):
        X = a[i - lookback: i]
        if flatten:
            X = X.flatten()
        y = a[i, target_col]
        i += 1
        yield X, y


def vectorize_input(iterable):
    """
    Vectorize input sample

    :param generator: bath generator
    :return:
    """
    data = np.array(list(iterable))
    X_list = data[:, 0]
    X = np.ndarray(shape=[len(X_list), len(X_list[0])])
    for i in range(len(X_list)):
        X[i] = X_list[i]
    return X


def vectorize_target(iterable):
    data = np.array(list(iterable))
    y = data[:, 1]
    return y


def smooth_curve(points, factor=0.9):
    smoothed_points = []
    for point in points:
        if smoothed_points:
            previous = smoothed_points[-1]
            smoothed_points.append(previous * factor + point * (1 - factor))
        else:
            smoothed_points.append(point)
    return smoothed_points
