import numpy as np
import pandas as pd
from pandas import DataFrame
from plotnine import *
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split


def mse(model, x, y):
    return np.mean((model.predict(x.reshape(-1, 1)) - y) ** 2)


def cross_validation(x, y, degrees, cv):
    train_errors = []
    validation_errors = []
    kf = KFold(n_splits=cv)
    for degree in degrees:
        train_error, validation_error = 0, 0
        for train_indexes, validation_indexes in kf.split(x):
            model = make_pipeline(PolynomialFeatures(degree),
                                  LinearRegression())
            model.fit(x[train_indexes].reshape(-1, 1), y[train_indexes])

            err = mse(model, x[train_indexes], y[train_indexes])
            train_error += err

            err = mse(model, x[validation_indexes], y[validation_indexes])
            validation_error += err

        train_errors.append(train_error / cv)
        validation_errors.append(validation_error / cv)
    return train_errors, validation_errors


def plot_validation(x_train, y_train, degrees, cv, noise):
    train_errors, validation_errors = cross_validation(x_train, y_train,
                                                       degrees, cv)
    df = DataFrame({'degree': degrees, 'train error': train_errors,
                    'validation error': validation_errors})
    df = pd.melt(df, id_vars='degree')
    plot = ggplot(df) + \
           geom_line(aes(x='degree', y='value', color='variable')) + \
           labs(x='degree', y='error',
                title=f'error / degree with k-fold={cv} and noise {noise}')
    print(plot)
    ggsave(plot, f'validation_train_polyfit_noise{noise}_cv{cv}.png')
    return degrees[np.argmin(validation_errors)]


def real_function(x):
    return (x + 3) * (x + 2) * (x + 1) * (x - 1) * (x - 2)


def get_data(noise_sigma, low_bound=-3.2, high_bound=2.2, size=1500,
             test_size=500):
    # sample 1500 from x uniformly
    x = np.random.uniform(low_bound, high_bound, size)
    # calculate polynomial + noise
    y = real_function(x) + np.random.normal(0, noise_sigma ** 2, x.shape)
    # split data and return it
    return train_test_split(x, y, test_size=test_size / size)


def plot_best_degree(model, x_train, y_train, x_test, y_test, noise, test_error,
                     best_degree, low_bound=-3.2, high_bound=2.2, h=100):
    x_range = np.linspace(low_bound, high_bound, h)
    # a df with 2 function the real one and the prediction
    df_f1 = DataFrame({'x': x_range, 'y': real_function(x_range),
                       'type': 'real function'})
    df_f2 = DataFrame({'x': x_range, 'y': model.predict(x_range.reshape(-1, 1)),
                       'type': 'model prediction'})
    df_f = pd.concat([df_f1, df_f2])
    # a df with the train and test points for the final model
    df_p = DataFrame({'x': x_train, 'y': y_train, 'type': 'train points'})
    df_p = pd.concat([df_p, DataFrame({'x': x_test, 'y': y_test,
                                       'type': 'test points'})])
    plot = ggplot() + \
           geom_point(aes(x='x', y='y', color='type'), data=df_p, size=0.2) + \
           geom_line(aes(x='x', y='y', color='type'), data=df_f, size=1.1) + \
           labs(x='x', y='y') + \
           ggtitle(f'noise={noise} test_error={round(test_error, 3)} best_degree={best_degree}')
    print(plot)
    ggsave(plot, f'best_degree_polyfit_noise{noise}.png')


def q4(degrees, noise):
    # part a get the data
    x_train, x_test, y_train, y_test = get_data(noise)
    # part b-c do 2 k-fold and plot it, ignore the return value
    plot_validation(x_train, y_train, degrees, 2, noise)
    # part d-e do 5 k-fold and plot it
    best_degree = plot_validation(x_train, y_train, degrees, 5, noise)
    # train best degree on all of D and check on test data
    model = make_pipeline(PolynomialFeatures(best_degree), LinearRegression())
    model.fit(x_train.reshape(-1, 1), y_train)
    test_error = mse(model, x_test, y_test)
    plot_best_degree(model, x_train, y_train, x_test, y_test, noise, test_error,
                     best_degree)


if __name__ == '__main__':
    params = np.arange(16)
    q4(params, 1)
    q4(params, 5)
