import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

POSITIVES = ['price', 'bedrooms', 'bathrooms', 'floors', 'sqft_lot', 'grade',
             'sqft_living', 'sqft_above', 'sqft_living15', 'sqft_lot15',
             'condition', 'yr_built']
NON_NEGATIVES = ['sqft_basement', 'view', 'waterfront', 'yr_renovated', 'lat']


def fit_linear_regression(X, y):
    return np.linalg.pinv(X.T) @ y, np.linalg.svd(X, compute_uv=False)


def predict(X, w):
    return X.T @ w


def mse(y, w):
    return np.sum((y - w) ** 2) / len(y)


def plot_helper(x, y, title='', x_label='', y_label='', is_log=False,
                is_points=False, to_save=False, save_file_name=''):
    plt.figure()

    if is_points:
        plt.plot(x, y, 'o', color='black', markersize=2, linewidth=0)
    else:
        plt.plot(x, y)
    if is_log:
        plt.yscale('log')

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if to_save:
        plt.savefig(save_file_name + '.png')
    plt.show()


def plot_singular_values(singular_values):
    singular_values = np.sort(singular_values)[::-1]
    x = np.arange(1, len(singular_values) + 1)
    print(singular_values)
    plot_helper(x, singular_values,
                title='the scree graph of the singular values',
                x_label='Number of singular value', y_label='singular value',
                is_points=True, is_log=True, to_save=True,
                save_file_name='singular values plot')


def calc_correlation(vec1, vec2):
    cov_matrix = np.cov(vec1, vec2)
    sigma1 = cov_matrix[0, 0]
    sigma2 = cov_matrix[1, 1]
    cov = cov_matrix[0, 1]
    return cov / np.sqrt((sigma1 * sigma2))


def convert_df_matrix(df, output_col='price', ones='ones'):
    output_vec = df[output_col]
    df = df.drop(labels=[output_col], axis=1)
    df.insert(0, ones, np.ones((df.shape[0])))
    return df.T, output_vec


def plot_scatter_graph(feature, response, feature_name='', to_save=False):
    corr = round(calc_correlation(feature, response), 3)
    title = f'scatter graph, price and {feature_name}, correlation {corr}'
    plot_helper(feature, response, title=title,
                x_label=f'{feature_name} values', y_label='response values',
                is_points=True, is_log=True, to_save=to_save,
                save_file_name=f'{feature_name} scatter')


def load_data():
    # read file
    data = pd.read_csv('kc_house_data.csv')
    # remove not important values
    data = data.dropna().drop(labels=['id', 'date'], axis=1)
    for feature in POSITIVES:
        data = data[data[feature] > 0]
    for feature in NON_NEGATIVES:
        data = data[data[feature] >= 0]
    # https://www.slideshare.net/PawanShivhare1/predicting-king-county-house-prices
    data = data[
        (data['grade'] <= 13) & (data['condition'] <= 5) & (data['view'] <= 4)]

    data = data.drop_duplicates()
    # change zip to categorical
    data['zipcode'] = np.round(data['zipcode']).astype(np.int)
    # https://chrisalbon.com/python/data_wrangling/pandas_convert_categorical_to_dummies/
    data = pd.get_dummies(data, columns=['zipcode'])

    return convert_df_matrix(data)


def combine_first_part():
    X, y = load_data()
    data = X.T.drop('ones', axis=1).T
    w, singular_values = fit_linear_regression(data, y)
    plot_singular_values(singular_values)
    return X, y


def combine_second_part(X, y):
    X, y = X.values, y.values
    num = X.shape[1]
    train_indexes = np.random.choice(num, int(num * 3.0 / 4.0), replace=False)
    test_indexes = np.setdiff1d(np.arange(num), train_indexes)
    x_train, x_test = X[:, train_indexes], X[:, test_indexes]
    y_train, y_test = y[train_indexes], y[test_indexes]
    mse_error = []
    for p in range(1, 101):
        size = int(num * p / 100.0)
        w, s = fit_linear_regression(x_train[:, :size], y_train[:size])
        mse_error.append(mse(predict(x_test, w), y_test))
    plot_helper(np.arange(1, 101), mse_error,
                title='mse of test data per % trained',
                x_label='% of train data', y_label='mse on test data',
                is_log=True, is_points=True, to_save=True,
                save_file_name='mse plot')


def feature_evaluation(X, response):
    data = X.T
    cols = [column for column in data.columns if
            'zipcode' not in column and
            'ones' != column and 'date' not in column]
    for feature in cols:
        plot_scatter_graph(data[feature], response, feature_name=feature,
                           to_save=feature in ['sqft_living', 'grade', 'long'])


if __name__ == '__main__':
    (matrix, vec) = combine_first_part()
    combine_second_part(matrix, vec)
    feature_evaluation(matrix, vec)
