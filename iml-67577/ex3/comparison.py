import numpy as np
from models import Perceptron, SVM, LDA
from pandas import DataFrame
import pandas as pd
from plotnine import *


def draw_points(m):
    # choose random points
    mean = [0, 0]
    cov = np.eye(2)
    X = np.random.multivariate_normal(mean, cov, m).T
    # create labels for the data
    w, b = np.array([0.3, -0.5]), 0.1
    y = np.sign(X.T @ w + b)
    y[y == 0] = 1
    return X, y.astype(np.int)


def add_line_gplot(plot, y_coef, x_coef, bias_coef, legend, x_min, x_max,
                   count=100):
    x_range = np.linspace(x_min, x_max, count)
    y_range = -x_coef / y_coef * x_range - bias_coef / y_coef
    return plot + geom_line(aes(x='x', y='y', color='legend'),
                            data=DataFrame({'x': x_range, 'y': y_range,
                                            'legend': [legend] * len(x_range)}))


def add_ones_matrix(X):
    return np.vstack([np.ones(X.shape[1]), X])


def question9_add_perceptron_plot(plot, X, y, min_x, max_x):
    # train the perceptron and plot its hyperplane, values are stored as
    # bias, x ,y
    model = Perceptron()
    x = add_ones_matrix(X)
    model.fit(x, y)
    bias_coef, x_coef, y_coef = model.model
    return add_line_gplot(plot, y_coef, x_coef, bias_coef,
                          'perceptron hyperplane', min_x, max_x)


def question9_add_SVM_plot(plot, X, y, min_x, max_x):
    model = SVM()
    model.fit(X, y)
    w = model.model.coef_[0]
    y_coef, x_coef, bias_coef = w[1], w[0], model.model.intercept_[0]

    return add_line_gplot(plot, y_coef, x_coef, bias_coef,
                          'svm hyperplane', min_x, max_x)


def question9():
    for m in [5, 10, 15, 25, 70]:
        # get data and figure the x range to plot the hyperplanes at
        X, y = get_good_training_points(m)
        min_x, max_x = np.min(X[0]), np.max(X[0])

        # plot points with correct colors
        df = DataFrame({'x': X[0], 'y': X[1], 'label': y.astype(str)})
        plot = ggplot() + ggtitle(f'hyperplanes with {m} samples') + \
               geom_point(aes(x='x', y='y', fill='label'), size=1.5, data=df) + \
               labs(x='x', y='y')

        # plot hyperplanes
        plot = add_line_gplot(plot, -0.5, 0.3, 0.1, 'real hyperplane', min_x,
                              max_x)

        plot = question9_add_perceptron_plot(plot, X, y, min_x, max_x)

        plot = question9_add_SVM_plot(plot, X, y, min_x, max_x)
        # show & save plot
        ggsave(plot, f'question 9 plot with {m} samples.png')
        print(plot)


def get_good_training_points(m):
    X, y = draw_points(m)
    while np.all(y == 1) or np.all(y == -1):
        X, y = draw_points(m)
    return X, y


def question10_test_a_model(model, samples, k=10000, repeat_constant=500,
                            add_bias=False):
    mean_accuracy = np.array([])
    for m in samples:
        current_accuracy = 0
        for _ in range(repeat_constant):
            # choose points
            X_train, y_train = get_good_training_points(m)
            X_test, y_test = draw_points(k)
            if add_bias:
                X_train = add_ones_matrix(X_train)
                X_test = add_ones_matrix(X_test)

            model.fit(X_train, y_train)
            acc = model.score(X_test, y_test)['accuracy']
            current_accuracy += acc
        # add to the mean accuracy the current test
        mean_accuracy = np.append(mean_accuracy,
                                  current_accuracy / repeat_constant)
    return mean_accuracy


def add_df_points_to_graph(plot, dfs, x_label='samples', y_label='accuracy',
                           legend='legend', add_line=False):
    for df in dfs:
        plot += geom_point(aes(x=x_label, y=y_label, color=legend),
                           data=df, alpha=0.7, size=1.5)
        if add_line:
            plot += geom_line(aes(x=x_label, y=y_label, color=legend),
                              data=df, alpha=0.5, size=0.8)
    return plot


def create_df_for_model(model, samples, legend, add_bias=False):
    accuracy = question10_test_a_model(model, samples, add_bias=add_bias)
    return DataFrame({'samples': samples, 'accuracy': accuracy,
                      'legend': [legend] * len(samples)})


def question10():
    samples = np.array([5, 10, 15, 25, 70])

    # draw plot of accuracy / number of samples
    df1 = create_df_for_model(Perceptron(), samples, 'Perceptron accuracy',
                              add_bias=True)
    df2 = create_df_for_model(SVM(), samples, 'SVM accuracy')
    df3 = create_df_for_model(LDA(), samples, 'LDA accuracy')
    dfs = [df1, df2, df3]

    plot = ggplot() + ggtitle('accuracies / samples') + \
           labs(x='number of samples', y='accuracy')
    plot = add_df_points_to_graph(plot, dfs, add_line=True)

    print(plot)
    ggsave(plot, 'q10 accuracies over samples.png')


if __name__ == '__main__':
    question9()
    question10()
