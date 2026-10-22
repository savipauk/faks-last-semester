import numpy as np
from math import *

ginverse = np.array([[ 0.722, -0.035,  0.005, -0.018, -0.018],
                     [-0.035,  0.01,       0,  0.001,  0.001],
                     [ 0.005,     0,   0.009,      0, -0.002],
                     [-0.018, 0.001,       0,  0.003, -0.001],
                     [-0.018, 0.001,  -0.002, -0.001,  0.002]])

fi = np.array([[1,  1,  5,  1, 25],
               [1,  2, -2,  4,  4],
               [1,  3,  1,  9,  1],
               [1, -5,  6, 25, 36]])

y = np.array([-2, 5, 3, -3])

weights = ginverse @ (fi.T @ y)
print(weights)

i = 0
norma = 0
for i in range(1, len(weights)):
    norma += weights[i]**2

i = 0
suma = 0

for i in range(0, 4):
    suma += (weights.T @ fi[i] - y[i])**2

suma *= 0.5
print(suma)
print(norma)
print(suma + norma * 50)
