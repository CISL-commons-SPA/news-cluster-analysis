import numpy as np
from markov_stability.stability import calculate_full_stability
from markov_stability.stability import calculate_linear_stability


adjacency = np.array([[0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0]])

timesteps = np.logspace(-2,2,5)

result = calculate_full_stability(adjacency,timesteps)