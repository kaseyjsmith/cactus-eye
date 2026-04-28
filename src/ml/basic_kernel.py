"""
Author: Kasey Smith
Date: 2026-03-30
Goal:
    Implement a simple sliding kernel that computes the weighted sum of each
    position as it slides across an NxN tensor.

    This file demonstrates a 3x3 weighted sum kernel application to a 6x6 input
    with a stride of 1.
"""

import numpy as np


class Kernel:
    def __init__(self, dim=(3, 3)):
        pass


np.random.seed(42)
stride = 1

# 6x6 input
input = np.random.randint(255, size=(6 * 6)).reshape((6, 6))

# 3x3 kernel
kernel = np.array([[1, 1, 1], [1, 5, 1], [1, 1, 1]])
# see notes for formula
output_size = int((input.shape[0] - kernel.shape[0]) / stride + 1)

# pre-allocate array of known output dimensions
out = np.zeros((output_size, output_size))

# implements a sliding window that maps the whole input
for i in range(0, input.shape[1] - kernel.shape[1] + 1):
    for j in range(0, input.shape[0] - kernel.shape[0] + 1):
        ## shows the sliding in action
        # print(input[i : i + kernel.shape[1], j : j + kernel.shape[0]])
        weighted_sum = np.sum(
            kernel * input[i : i + kernel.shape[1], j : j + kernel.shape[0]]
        )
        # print(weighted_sum)
        out[i, j] = weighted_sum


print(f"out: {out}")
