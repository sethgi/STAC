import matplotlib.pyplot as plt
from Types import *
import numpy as np
import tqdm

class Map:

  def __init__(self, x_range = (-5, 5), y_range=(-5, 5)):
    self._x_min, self._x_max = x_range
    self._y_min, self._y_max = y_range

    self._intruders = []
    self._environmentals = []

  def GetBounds(self):
    return ((self._x_min, self._x_max), (self._y_min, self._y_max))

  def RegisterIntruder(self, intruder, current_time):
    self._intruders.append(intruder)
    intruder._last_update_time = current_time

  def RemoveIntruder(self, id):
    self._intruders.pop(id)

  def RegisterEnvironmental(self, environmental, current_time):
    self._environmentals.append(environmental)
    environmental._last_update_time = current_time

  def RenderFrame(self):

    plt.xlim([self._x_min, self._x_max])
    plt.ylim([self._y_min, self._y_max])

    for intruder in self._intruders:
      intruder.Render()

    plt.show()

  def Update(self, current_time):
    delete_indexes = []

    for idx, intruder in enumerate(self._intruders):
      if intruder.IsDead():
        delete_indexes.append(idx)
      
      if intruder.NeedsUpdate(current_time):
        intruder.Update(current_time)

    num_deleted = 0
    for idx in delete_indexes:
      self._intruders.pop(idx - num_deleted)
      num_deleted += 1

    for idx, environmental in enumerate(self._environmentals):
      if environmental.IsDead():
        delete_indexes.append(idx)
      
      if environmental.NeedsUpdate(current_time):
        environmental.Update(current_time)

    num_deleted = 0
    for idx in delete_indexes:
      self._environmentals.pop(idx - num_deleted)
      num_deleted += 1
  
  def GetIntruderLocations(self):
    return ((intruder._state.pose.x, intruder._state.pose.y) for intruder in self._intruders)

  def GetEnvironmentalValues(self, positions):
    result = []
    for env in self._environmentals:
      result.append(env.GetValues(positions))
    return result

"""
if __name__ == '__main__':
  intruder = RandomWalkIntruder()
  prev_node = None
  last_valid_node = None
  for i in tqdm.tqdm(range(10000)):
    node = intruder.Update(0.1)

    if node is None and prev_node is not None:
      graph = prev_node.BuildDict()
      for parent in graph:
        for child in graph[parent]:
          plt.plot([parent.state.pose.x, child.state.pose.x],[parent.state.pose.y, child.state.pose.y], color='red')
    
    prev_node = node
    if prev_node is not None:
      last_valid_node = prev_node
  

  if node is None:
    graph = last_valid_node.BuildDict()
    for parent in graph:
      for child in graph[parent]:
        plt.plot([parent.state.pose.x, child.state.pose.x],[parent.state.pose.y, child.state.pose.y], color='red')

  map = Map()
  map.RegisterIntruder(intruder)
  map.RenderFrame()

"""
