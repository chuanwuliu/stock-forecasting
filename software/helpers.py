import numpy as np


def batch_generator(a, batch=1, step=1, target_col=3):
    """
    Get a generator of for iterating over the array with given batch and step.

    :param a: array
    :param batch: batch size
    :param step: step length
    :target_col: target column
    :return: array and float
    """
    assert len(a) > batch, "Length of array must be larger than batch size"
    assert batch > 0 and step > 0, "Batch and step must be positive"

    a = np.array(a)
    i = batch
    while i < len(a):
        X = a[i - batch: i].flatten()
        y = a[i, target_col]
        i += step
        yield X, y
