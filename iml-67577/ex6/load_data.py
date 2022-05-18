import tensorflow as tf
import numpy as np


def get_digits(first_digit, second_digit):
    mnist = tf.keras.datasets.mnist

    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    x_train = (x_train / 255.0 * 2 - 1).reshape(x_train.shape[0], -1)
    x_test = (x_test / 255.0 * 2 - 1).reshape(x_test.shape[0], -1)

    train_indices = np.logical_or(y_train == first_digit,  y_train == second_digit)
    test_indices = np.logical_or(y_test == first_digit, y_test == second_digit)

    x_train = x_train[train_indices]
    y_train = y_train[train_indices, np.newaxis].astype(np.float)
    x_test = x_test[test_indices]
    y_test = y_test[test_indices, np.newaxis].astype(np.float)
    return x_train, y_train, x_test, y_test


