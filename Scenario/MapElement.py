import matplotlib.pyplot as plt
from Types import Point2, Pose2
from Map import Map

class MapElement:
  def __init__(self, global_map):
    self._should_delete = False

    self._last_update_time = None
    self._update_interval = 0.1
    self._map = global_map

  def NeedsUpdate(self, current_time):
    if self._last_update_time is None:
      return True
    
    time_passed = current_time - self._last_update_time

    return time_passed >= self._update_interval

  def Kill(self):
    self._should_delete = True

  def IsDead(self):
    return self._should_delete

  def Update(self, current_time):
    dt = current_time - self._last_update_time
    self._last_update_time = current_time
    
    self.DoUpdate(current_time, dt)
  
  def DoUpdate(self, dt):
    raise Exception("Not Implemented")

