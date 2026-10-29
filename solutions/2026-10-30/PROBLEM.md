# Problem: How can I fix my perceptron to recognize numbers?

**Date:** 2026-10-30

**Source:** Stack Overflow

**Category:** data

**Why Selected:** Trending problem in data category

## Description

My exercise is to train 10 perceptrons to recognize numbers (0 - 9). Each perceptron should learn a single digit. As training data, I've created 30 images (5x7 bmp). 3 variants per digit. I've got a perceptron class: import numpy as np def unit_step_func(x): return np.where(x > 0, 1, 0) def sigmoid(x): return 1 / (1 + np.exp(-x)) class Perceptron: def __init__(self, learning_rate=0.01, n_iters=1000): self.lr = learning_rate self.n_iters = n_iters self.activation_func = unit_step_func self.weight

## Original URL

https://stackoverflow.com/questions/77594625/how-can-i-fix-my-perceptron-to-recognize-numbers
