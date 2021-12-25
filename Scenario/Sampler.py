from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

import numpy as np

from Scenario import Handler

class Sample:
  def __init__(self, t, x, y, value):
    self.time = t
    self.x = x
    self.y = y
    self.value = value

class Sampler(Handler):
  def __init__(self, scenario):
    super().__init__()
    self._bounds = scenario.GetMap().GetBounds()
    self._buffer_time = 5
    self._rate = 1
    self._num_points = 5

    self._buffer_size = self._num_points * self._buffer_time * self._rate
    self._buffer = []

    self._prediction_buffer_size = self._rate * self._buffer_time
    self._prediction_buffer = []

    self._kernel = C(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))
    self._gp = GaussianProcessRegressor(kernel = self._kernel, n_restarts_optimizer=3)

    x,y = np.mgrid[-5:5:0.1,-5:5:0.1]
    self._prediction_points = np.dstack((x,y))

    self._current_gp = None

    
  def Do(self, scenario):
    (x_min, x_max),(y_min,y_max) = self._bounds

    xs = np.random.rand(self._num_points) * (x_max - x_min) + x_min
    ys = np.random.rand(self._num_points) * (y_max - y_min) + y_min

    locs = np.dstack((xs, ys))

    # TODO: Don't hardcode this just being one factor
    measurements = list(scenario.GetMap().GetEnvironmentalValues(locs)[0][0])
    samples = [Sample(scenario.GetTime(),x,y,m) for (x,y),m in  zip(zip(xs, ys), measurements)]
    self._buffer += samples

    if len(self._buffer) > self._buffer_size:
      blocks_to_remove = np.ceil((len(self._buffer) - self._buffer_size)/self._num_points)
      num_to_remove = int(blocks_to_remove * self._num_points)
      self._buffer = self._buffer[num_to_remove:]
    
    self.FitModel(scenario.GetTime())

  def GetCurrentModel(self):
    if self._current_gp is None:
      return None,None
    return self._current_gp

  def GetProjectionOfNow(self):
    if len(self._prediction_buffer) == self._prediction_buffer_size:
      return self._prediction_buffer[0]
    return None,None

  def FitModel(self, current_time):
    points = np.array([np.array([s.x, s.y, s.time]) for s in self._buffer])
    values = np.array([s.value for s in self._buffer])
   
    x,y = np.mgrid[-5:5:0.1,-5:5:0.1]
    sample_points = np.dstack((x,y)).reshape(10000,2)
    times = np.reshape(np.repeat(current_time, sample_points.shape[0]), 
                       (sample_points.shape[0],1))

    future_times = np.reshape(np.repeat(current_time + 5, sample_points.shape[0]), 
                       (sample_points.shape[0],1))
   
    current_samples = np.concatenate((sample_points, times), axis=1)
    future_samples = np.concatenate((sample_points, future_times), axis=1)
    
    self._gp.fit(points, values)
   
    self._current_gp = self._gp.predict(current_samples, return_std=True)
    self._prediction_buffer.append(self._gp.predict(future_samples, return_std=True))

    if len(self._prediction_buffer) > self._prediction_buffer_size:
      self._prediction_buffer = self._prediction_buffer[1:]
  
