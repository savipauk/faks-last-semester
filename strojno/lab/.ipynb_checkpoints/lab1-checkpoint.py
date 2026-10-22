import numpy as np
import sklearn
import matplotlib.pyplot as plt


X = np.array([[0], [1], [2], [4]])
y = np.array([4, 1, 2, 5])


from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree=1, include_bias=True)
matrix = poly.fit_transform(X)
print(matrix)


from numpy import linalg
weights = linalg.matmul(
        linalg.matmul(
            linalg.inv(
                linalg.matmul(
                    linalg.matrix_transpose(matrix),
                    matrix
                )
            ), 
            linalg.matrix_transpose(matrix)
        ),
    y
)
weights_pinv = linalg.matmul(linalg.pinv(matrix), y)
print("weigths: ", weights)
print("weigths_pinv: ", weights_pinv)


from sklearn.metrics import mean_squared_error



