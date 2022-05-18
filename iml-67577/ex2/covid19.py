import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from linear_model import fit_linear_regression, predict

COVID_EXCEL = 'covid19_israel.csv'


def convert_df_matrix(df, output_col='price', ones='ones'):
    output_vec = df[output_col]
    df = df.drop(labels=[output_col], axis=1)
    df.insert(0, ones, np.ones((df.shape[0])))
    return df.T, output_vec


def plot_graph(x, y1, y2, title='', x_label='', y_label='',
               y_label1='', y_label2='', to_save=False, save_file_name='',
               point_size=2.0):
    plt.figure()

    plt.plot(x, y2, color='red', label=y_label2)
    plt.plot(x, y1, color='black', label=y_label1)

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend(loc='upper left')
    plt.plot(x, y2, 'o', color='red', markersize=point_size, linewidth=0)
    plt.plot(x, y1, 'o', color='black', markersize=point_size, linewidth=0)
    if to_save:
        plt.savefig(save_file_name + '.png')
    plt.show()


if __name__ == '__main__':
    data = pd.read_csv(COVID_EXCEL)
    data['log_detected'] = np.log(data['detected'])
    matrix, vec = convert_df_matrix(data[['day_num', 'log_detected']],
                                    output_col='log_detected')
    w, s = fit_linear_regression(matrix, vec)
    data['log_prediction'] = predict(matrix, w)
    data['prediction'] = np.exp(data['log_prediction'])

    plot_graph(data['day_num'], data['log_detected'], data['log_prediction'],
               title='log of sick people per day', x_label='day number',
               y_label='log number of people sick', y_label1='real number',
               y_label2='prediction', to_save=True, save_file_name='covid_log',
               point_size=1.3)
    plot_graph(data['day_num'], data['detected'], data['prediction'],
               title='sick people per day', x_label='day number',
               y_label='number of people sick', y_label1='real number',
               y_label2='prediction', to_save=True, save_file_name='covid',
               point_size=1.3)
