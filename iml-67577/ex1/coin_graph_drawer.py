# coding=utf-8
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    data = np.random.binomial(1, 0.25, (100000, 1000))

    x_coords = np.arange(1, 1 + data.shape[1])
    summed_data = np.cumsum(data, axis=1)
    # expection = sum data / number of data
    expected_value = summed_data / x_coords
    # plot expected value
    for i in range(5):
        plt.plot(x_coords, expected_value[i])

    plt.title('the expected value of the coin toss')
    plt.xlabel('the number of samples (m)')
    plt.ylabel('the guess of expectation (and probability)')
    plt.savefig('Q16 a.png')
    plt.show()

    # the difference from the real expectation
    normalized_expectation = np.abs(expected_value - 0.25)
    helper_f = lambda x: 'upper right' if x != 0.001 else 'lower right'
    # for some reason the epsilon character can't be seen in the pdf while
    # still being in the code, just made this comment to clarify why the title
    # and the name of the file looks weird in the pdf
    for epsilon in [0.5, 0.25, 0.1, 0.01, 0.001]:
        # plot the real bound
        plt.plot(x_coords, np.sum(normalized_expectation >= epsilon, axis=0)
                 / (1.0 * expected_value.shape[0]),
                 label='real bound')
        # plot the Chebyshev bound
        plt.plot(x_coords,
                 np.clip(1.0 / (4.0 * x_coords * (epsilon ** 2)), 0, 1),
                 label='Chebyshev bound')
        # plot the Hoeffding bound
        plt.plot(x_coords,
                 np.clip(2.0 * np.exp(-2.0 * x_coords * (epsilon ** 2)), 0, 1),
                 label='Hoeffding bound')
        plt.legend(loc=helper_f(epsilon))
        plt.title('the upper bound of P[|X-E[X]|>=ε] for ε={}'.format(epsilon))
        plt.xlabel('number of samples (m)')
        plt.ylabel('probability')
        plt.savefig('Q16 b with ε={}.png'.format(epsilon))
        plt.show()
