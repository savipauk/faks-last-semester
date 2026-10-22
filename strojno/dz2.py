import numpy as np


w = np.array([[ 3, -1, -1, 2],
              [ 2, -4, -2, 1],
              [ 3, -4,  6, 1],
              [-3,  0,  2, 1]])

alpha = np.array([1, 2, -3, -6])


print(np.matmul(alpha, w))

