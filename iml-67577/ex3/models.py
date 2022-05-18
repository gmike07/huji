import numpy as np
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier


def classifier_score(model, X, y):
    prediction = model.predict(X)
    tp = np.sum((prediction == 1) & (y == 1))
    fp = np.sum((prediction == 1) & (y != 1))
    tn = np.sum((prediction != 1) & (y != 1))
    fn = np.sum((prediction != 1) & (y == 1))
    p = tp + fn
    n = fp + tn
    return {
                'num_samples': p + n,
                'error': (fp + fn) / (p + n),
                'accuracy': (tp + tn) / (p + n),
                'TPR': tp / p,
                'FPR': fp / n,
                'precision': tp / (tp + fp),
                'recall': tp / p
            }


class Perceptron:
    def __init__(self):
        self.model = 0

    def fit(self, X, y):
        X_T = X.T
        self.model = np.zeros(X.shape[0])
        while True:
            mask = (y * (X_T @ self.model)) > 0
            if np.all(mask):
                return
            index = np.nonzero(~mask)[0][0]
            self.model += y[index] * X[:, index]

    def predict(self, X):
        mask = (X.T @ self.model) <= 0
        prediction = np.ones(X.shape[1])
        prediction[mask] = -1
        return prediction

    def score(self, X, y):
        return classifier_score(self, X, y)


class LDA:
    def __init__(self):
        self.model = None

    def fit(self, X, y):
        positive = X[:, y == 1]
        negative = X[:, y == -1]
        # probability
        p1 = positive.shape[1] / len(y)
        p_minus1 = negative.shape[1] / len(y)
        # expectation
        mu1 = np.mean(positive, axis=1).reshape(-1, 1)
        mu_minus1 = np.mean(negative, axis=1).reshape(-1, 1)
        # sigma calculation
        pos = (positive - mu1) @ (positive - mu1).T
        neg = (negative - mu_minus1) @ (negative - mu_minus1).T
        sigma_inv = np.linalg.pinv((pos + neg) / (X.shape[1] - 2))
        # store the data as model ((mat1, const1), (mat-1, const-1))
        # when the prediction is X.T @ mat + constant
        self.model = (LDA.convert_matrix(sigma_inv, mu1, p1),
                      LDA.convert_matrix(sigma_inv, mu_minus1, p_minus1))

    @staticmethod
    def convert_matrix(sigma_inv, mu, p):
        matrix = sigma_inv @ mu
        return matrix, -0.5 * mu.T @ matrix + np.log(p)

    def predict(self, X):
        ((mat1, const1), (mat_minus1, const_minus1)) = self.model
        negative = X.T @ mat_minus1 + const_minus1
        positive = X.T @ mat1 + const1
        prediction = np.ones(X.shape[1])
        prediction[positive.ravel() < negative.ravel()] = -1
        return prediction

    def score(self, X, y):
        return classifier_score(self, X, y)


class SVM:

    def __init__(self):
        self.model = SVC(C=1e10, kernel='linear')

    def fit(self, X, y):
        return self.model.fit(X.T, y)

    def predict(self, X):
        return self.model.predict(X.T)

    def score(self, X, y):
        return classifier_score(self, X, y)


class Logistic:

    def __init__(self):
        self.model = LogisticRegression(solver='liblinear')

    def fit(self, X, y):
        return self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def score(self, X, y):
        return classifier_score(self, X, y)


class DecisionTree:

    def __init__(self):
        self.model = DecisionTreeClassifier()

    def fit(self, X, y):
        return self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def score(self, X, y):
        return classifier_score(self, X, y)


class KNN:

    def __init__(self, n_neighbors=3):
        self.model = KNeighborsClassifier(n_neighbors=n_neighbors)

    def fit(self, X, y):
        return self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def score(self, X, y):
        return classifier_score(self, X, y)


class Soft_SVM:

    def __init__(self):
        self.model = SVC(C=0.01, kernel='linear')

    def fit(self, X, y):
        return self.model.fit(X, y)

    def predict(self, X):
        return self.model.predict(X)

    def score(self, X, y):
        return classifier_score(self, X, y)
