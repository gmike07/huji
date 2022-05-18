import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.linalg import qr

def get_orthogonal_matrix(dim):
    H = np.random.randn(dim, dim)
    Q, R = qr(H)
    return Q


def plot_3d(x_y_z):
    '''
    plot points in 3D
    :param x_y_z: the points. numpy array with shape: 3 X num_samples (first dimension for x, y, z
    coordinate)
    '''
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_y_z[0], x_y_z[1], x_y_z[2], s=1, marker='.', depthshade=False)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_zlim(-5, 5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')


def plot_2d(x_y):
    '''
    plot points in 2D
    :param x_y_z: the points. numpy array with shape: 2 X num_samples (first dimension for x, y
    coordinate)
    '''
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x_y[0], x_y[1], s=1, marker='.')
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_xlabel('x')
    ax.set_ylabel('y')


if __name__ == '__main__':
    #question 11 code
    mean = [0, 0, 0]
    cov = np.eye(3)
    x_y_z = np.random.multivariate_normal(mean, cov, 50000).T
    plot_3d(x_y_z)
    plt.title('Q11')
    plt.savefig('Q11.png')
    plt.show()

    #question 12 code
    scalar_matrix = np.array([[0.1, 0, 0], [0, 0.5, 0], [0, 0, 2]])
    x_y_z_scaled = scalar_matrix @ x_y_z
    plot_3d(x_y_z_scaled)
    plt.title('Q12')
    plt.savefig('Q12.png')
    plt.show()
    print(np.cov(x_y_z_scaled))

    #question 13 code
    orthogonal = get_orthogonal_matrix(3)
    x_y_z_rotated = (orthogonal @ x_y_z_scaled)
    plot_3d(x_y_z_rotated)
    plt.title('Q13')
    plt.savefig('Q13.png')
    plt.show()
    print(np.cov(x_y_z_rotated))

    #question 14 code
    plot_2d(x_y_z_rotated)
    plt.title('Q14')
    plt.savefig('Q14.png')
    plt.show()

    #question 15 code
    mask = (x_y_z_rotated[2] > -0.4) & (x_y_z_rotated[2] < 0.1)
    plot_2d(x_y_z_rotated[0: 2, mask])
    plt.title('Q15')
    plt.savefig('Q15.png')
    plt.show()
