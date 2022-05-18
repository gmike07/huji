"""
===================================================
     Introduction to Machine Learning (67577)
===================================================

Skeleton for the AdaBoost classifier.

Author: Gad Zalcberg
Date: February, 2019

"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import DataFrame
from plotnine import *
from ex4_tools import DecisionStump, generate_data, decision_boundaries


class AdaBoost(object):

    def __init__(self, WL, T):
        """
        Parameters
        ----------
        WL : the class of the base weak learner
        T : the number of base learners to learn
        """
        self.WL = WL
        self.T = T
        self.h = [None] * T  # list of base learners
        self.w = np.zeros(T)  # weights

    def train(self, X, y):
        """
        Parameters
        ----------
        X : samples, shape=(num_samples, num_features)
        y : labels, shape=(num_samples)
        Train this classifier over the sample (X,y)
        After finish the training return the weights of the samples in the last iteration.
        """
        m = X.shape[0]
        D = np.ones(m) / m
        for i in range(self.T):
            # train weak learner
            self.h[i] = self.WL(D, X, y)
            # calculate loss
            prediction = self.h[i].predict(X)
            loss = np.sum(D * (prediction != y))
            # update weights
            self.w[i] = 0.5 * np.log((1 / loss) - 1)
            # update probabilities
            D *= np.exp(-self.w[i] * y * prediction)
            D /= np.sum(D)
        return D

    def predict(self, X, max_t):
        """
        Parameters
        ----------
        X : samples, shape=(num_samples, num_features)
        :param max_t: integer < self.T: the number of classifiers to use for the classification
        :return: y_hat : a prediction vector for X. shape=(num_samples)
        Predict only with max_t weak learners,
        """
        prediction = np.zeros(X.shape[0])
        for i in range(min(max_t, self.T)):
            prediction += self.w[i] * self.h[i].predict(X)
        return np.where(prediction >= 0, 1, -1)

    def error(self, X, y, max_t):
        """
        Parameters
        ----------
        X : samples, shape=(num_samples, num_features)
        y : labels, shape=(num_samples)
        :param max_t: integer < self.T: the number of classifiers to use for the classification
        :return: error : the ratio of the correct predictions when predict only with max_t weak learners (float)
        """
        return np.sum(self.predict(X, max_t) != y) / len(y)


def plot_graph(model, X, y, x_label='x', y_label='y', title=None, t_value=500,
               save_name='', weights=None):
    plt.figure()
    decision_boundaries(model, X, y, num_classifiers=t_value, weights=weights)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    if title is not None:
        plt.title(title)
    plt.savefig(save_name + '.png')
    plt.show()


def draw_error_graph(df, noise=0):
    plot = ggplot(df) + geom_line(aes(x='x', y='y', color='legend')) + \
           labs(x='number of classifiers', y='error of the model') + \
           ggtitle(f'error \ number of classifiers noise = {noise}')
    print(plot)
    ggsave(plot, f'q10_error_over_classifier_noise_{noise}.png')


def q10_11_12_13(t_values, num_train_samples, num_test_samples, T_max, noise=0):
    # ==========================================================================
    # create samples
    X_train, y_train = generate_data(num_train_samples, noise)
    X_test, y_test = generate_data(num_test_samples, 0)
    # ==========================================================================
    # Q10
    train_error = np.array([]).astype(np.float64)
    test_error = np.array([]).astype(np.float64)

    model = AdaBoost(DecisionStump, T_max)
    D = model.train(X_train, y_train)

    x_range = np.arange(T_max) + 1
    for t in x_range:
        train_error = np.append(train_error, model.error(X_train, y_train, t))
        test_error = np.append(test_error, model.error(X_test, y_test, t))
    df = pd.concat([
        DataFrame({'x': x_range, 'y': train_error, 'legend': 'Train error'}),
        DataFrame({'x': x_range, 'y': test_error, 'legend': 'Test error'})
    ])
    draw_error_graph(df, noise=noise)
    # ==========================================================================
    # Q11
    plt.suptitle(f'noise = {noise}')
    for i, T in enumerate(t_values):
        plt.subplot(len(t_values) // 2, 2, i + 1)
        decision_boundaries(model, X_test, y_test, num_classifiers=T)

    plt.savefig(f'q11_boundaries_with_classifiers_noise_{noise}.png')
    plt.show()
    best_index_error = np.argmin(test_error)
    # ==========================================================================
    # Q12
    best_t_value = x_range[best_index_error]
    best_error = test_error[best_index_error]
    title = f'num classifiers = {best_t_value} and error = {best_error} noise = {noise}'
    plot_graph(model, X_train, y_train, title=title, t_value=best_t_value,
               save_name=f'q12_minimal_error_noise_{noise}')
    # ==========================================================================
    # Q13
    last_error = test_error[-1]
    title = f'num classifiers = {T_max} and error = {last_error} noise = {noise}'
    plot_graph(model, X_train, y_train,
               weights=(D / np.max(D) * 10), title=title, t_value=T_max,
               save_name=f'q13_weight_training_noise_{noise}')


if __name__ == '__main__':
    T_values = np.array([5, 10, 50, 100, 200, 500])
    for noise_ratio in [0, 0.01, 0.4]:
        q10_11_12_13(T_values, num_train_samples=5000,
                     num_test_samples=200,
                     T_max=500, noise=noise_ratio)
