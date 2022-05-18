import numpy as np
import pandas as pd
from pandas import DataFrame
from plotnine import *
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn import datasets


def mse(model, x, y):
    return np.mean((model.predict(x) - y) ** 2)


def cross_validation(model, x, y, lambdas, cv, param_name):
    train_errors = []
    validation_errors = []
    kf = KFold(n_splits=cv)
    for lam in lambdas:
        train_error, validation_error = 0, 0
        for train_indexes, validation_indexes in kf.split(x):
            model.set_params(**{param_name: lam})
            model.fit(x[train_indexes], y[train_indexes])

            err = mse(model, x[train_indexes], y[train_indexes])
            train_error += err

            err = mse(model, x[validation_indexes], y[validation_indexes])
            validation_error += err

        train_errors.append(train_error / cv)
        validation_errors.append(validation_error / cv)
    return train_errors, validation_errors


def plot_validation(model, x_train, y_train, lambdas, cv, model_name):
    train_errors, validation_errors = cross_validation(model, x_train, y_train,
                                                       lambdas, cv, 'alpha')
    df = DataFrame({'lambda': lambdas, 'train error': train_errors,
                    'validation error': validation_errors})
    df = pd.melt(df, id_vars='lambda')
    plot = ggplot(df) + \
           geom_line(aes(x='lambda', y='value', color='variable')) + \
           labs(x='lambda', y='error',
                title=f'error / lambda with k-fold={cv} with {model_name}')
    print(plot)
    ggsave(plot, f'validation_train_regularization_model_{model_name}.png')
    return lambdas[np.argmin(validation_errors)]


def get_data(train_size=50):
    X, y = datasets.load_diabetes(return_X_y=True)
    test_size = 1 - (train_size / len(X))
    return train_test_split(X, y, test_size=test_size)


def q5():
    # part a
    lambdas = np.linspace(0.01, 1, 1000)
    x_train, x_test, y_train, y_test = get_data()
    # part b-e
    model = Lasso()
    best_l1_lambda = plot_validation(model, x_train, y_train, lambdas, 5,
                                     'Lasso')
    best_l1_model = Lasso(alpha=best_l1_lambda).fit(x_train, y_train)
    best_l1_error = mse(best_l1_model, x_test, y_test)

    model = Ridge()
    best_l2_lambda = plot_validation(model, x_train, y_train, lambdas, 5,
                                     'Ridge')
    best_l2_model = Lasso(alpha=best_l2_lambda).fit(x_train, y_train)
    best_l2_error = mse(best_l2_model, x_test, y_test)

    best_no_l_model = LinearRegression().fit(x_train, y_train)
    best_no_l_error = mse(best_no_l_model, x_test, y_test)

    df = DataFrame({'best lasso error': [best_l1_error],
                    'best ridge error': best_l2_error,
                    'best no regularization error': best_no_l_error})
    print(df)


if __name__ == '__main__':
    q5()
