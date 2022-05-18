import tensorflow as tf
import numpy as np
from models import DecisionTree, Logistic, KNN, Soft_SVM
from pandas import DataFrame
from plotnine import *
import matplotlib.pyplot as plt
import time


def rearrange_data(X):
    samples, height, width = X.shape
    return X.reshape((samples, height * width))


def question12(x_train, y_train):
    zero_imgs = x_train[y_train == 0]
    for i in range(3):
        plt.figure()
        plt.imshow(zero_imgs[i], cmap='gray')
        plt.savefig(f'{i}_zeros.png')
        plt.show()
    ones_imgs = x_train[y_train == 1]
    for i in range(3):
        plt.figure()
        plt.imshow(ones_imgs[i], cmap='gray')
        plt.savefig(f'{i}_ones.png')
        plt.show()


def load_data():
    mnist = tf.keras.datasets.mnist
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    train_images = (y_train == 0) | (y_train == 1)
    test_images = (y_test == 0) | (y_test == 1)

    x_train, y_train = x_train[train_images], y_train[train_images]
    x_test, y_test = x_test[test_images], y_test[test_images]
    return (x_train, y_train), (x_test, y_test)


def get_good_train_set(X_train, y_train, m):
    train_indexes = np.random.choice(y_train.shape[0], m, replace=False)
    X, y = X_train[train_indexes], y_train[train_indexes]
    while np.all(y == 1) or np.all(y == 0):
        train_indexes = np.random.choice(y_train.shape[0], m, replace=False)
        X, y = X_train[train_indexes], y_train[train_indexes]
    return X, y


def question14_test_a_model(model, samples, X_train, y_train, X_test, y_test,
                            repeat_constant=50):
    mean_accuracy = np.array([])
    mean_time = np.array([])
    for m in samples:
        curr_time = time.time()
        current_accuracy = 0
        for _ in range(repeat_constant):
            # choose points
            curr_X_train, curr_y_train = get_good_train_set(X_train, y_train, m)
            model.fit(curr_X_train, curr_y_train)
            acc = model.score(X_test, y_test)['accuracy']
            current_accuracy += acc
        curr_time = (time.time() - curr_time)
        mean_time = np.append(mean_time, curr_time / repeat_constant)
        # add to the mean accuracy the current test
        mean_accuracy = np.append(mean_accuracy,
                                  current_accuracy / repeat_constant)

    return mean_accuracy, mean_time


def add_points_to_graph(df, y_label='accuracy', x_label='samples',
                        legend='legend'):
    return geom_point(aes(x=x_label, y=y_label, color=y_label + ' ' + legend),
                      data=df, alpha=0.7, size=1.5)


def add_df_points_to_graph(plot, dfs, x_label='samples', y_label='accuracy',
                           legend='legend', add_line=False):
    for df in dfs:
        plot += geom_point(
            aes(x=x_label, y=y_label, color=y_label + ' ' + legend),
            data=df, alpha=0.7, size=1.5)
        if add_line:
            plot += geom_line(
                aes(x=x_label, y=y_label, color=y_label + ' ' + legend),
                data=df, alpha=0.5, size=0.8)
    return plot


def create_df_for_model(model, legend, samples, x_train, y_train,
                        x_test, y_test):
    accuracy, times = question14_test_a_model(model, samples, x_train, y_train,
                                              x_test, y_test)
    return DataFrame({'samples': samples, 'accuracy': accuracy,
                      'accuracy legend': [legend + ' accuracy'] * len(samples),
                      'time legend': [legend + ' time'] * len(samples),
                      'time': times})


def question14(x_train, y_train, x_test, y_test):
    samples = np.array([50, 100, 300, 500])
    df1 = create_df_for_model(KNN(), 'KNN', samples, x_train, y_train,
                              x_test, y_test)
    df2 = create_df_for_model(DecisionTree(), 'DecisionTree', samples, x_train,
                              y_train, x_test, y_test)
    df3 = create_df_for_model(Logistic(), 'Logistic', samples, x_train, y_train,
                              x_test, y_test)
    df4 = create_df_for_model(Soft_SVM(), 'Soft-SVM', samples, x_train, y_train,
                              x_test, y_test)
    # draw plot of accuracy / number of samples
    dfs = [df1, df2, df3, df4]

    plot = ggplot() + ggtitle('accuracies / samples') + \
           labs(x='number of samples', y='accuracy')
    plot = add_df_points_to_graph(plot, dfs, y_label='accuracy', add_line=True)
    print(plot)
    ggsave(plot, 'q14 accuracies over samples mnist.png')

    plot = ggplot() + ggtitle('time / samples') + \
           labs(x='number of samples', y='time (seconds)')
    plot = add_df_points_to_graph(plot, dfs, y_label='time', add_line=True)
    print(plot)
    ggsave(plot, 'q14 time over samples mnist.png')


if __name__ == '__main__':
    (_x_train, _y_train), (_x_test, _y_test) = load_data()
    question12(_x_train, _y_train)
    _x_train = rearrange_data(_x_train)
    _x_test = rearrange_data(_x_test)
    question14(_x_train, _y_train, _x_test, _y_test)
