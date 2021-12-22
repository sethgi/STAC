from Map import Map
from MapElement import MapElement
from scipy.stats import multivariate_normal
import numpy as np

NUM_GAUSSIANS = 5

class Environmental(MapElement):
  def __init__(self, global_map):
    super().__init__(global_map)

    self._gaussians = []
    self._time = 0

    # (A, phi, theta)
    # coefficient = A * cos(phi * t + theta) 
    self._sinusuoids = [(np.random.rand() * 2 + 1, 
                        np.random.rand() / 5, 
                        np.random.rand() * 2*np.pi) for _ in range(NUM_GAUSSIANS)]

    self._coefficients = [1 for _ in range(NUM_GAUSSIANS)]

    for _ in range(NUM_GAUSSIANS):
      # Choose mean
      (x_min, x_max), (y_min, y_max) = self._map.GetBounds()
      
      x_mean = np.random.rand() * (x_max - x_min) + x_min 
      y_mean = np.random.rand() * (y_max - y_min) + y_min 

      x_variance = 6 * np.random.rand() + 3
      y_variance = 6 * np.random.rand() + 3

      self._gaussians.append(multivariate_normal([x_mean, y_mean],[[x_variance,0],[0,y_variance]]))

  def EvaluatePoint(self, x, y):
    return sum(g.pdf(np.dstack(x,y)) for g in self._gaussians)
 
  def GetValues(self, positions):
    result = np.zeros((positions.shape[0],positions.shape[1]))

    for c,g in zip(self._coefficients, self._gaussians):
      result = np.add(result, np.multiply(g.pdf(positions), c))

    return result
    

  def DoUpdate(self, current_time, dt):
    self._time = current_time 

    for idx, sinusoid in enumerate(self._sinusuoids):
      A,phi,theta = sinusoid
      coeff = A * np.cos(phi * current_time + theta)
      self._coefficients[idx] = coeff



