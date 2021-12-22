import matplotlib.pyplot as plt
from Types import Point2, Pose2
from MapElement import MapElement

class Intruder(MapElement):
  def __init__(self, global_map):
    super().__init__(global_map)
    self._position = Pose2()
    self._trajectory = []

  def Render(self):
    plt.plot(self._position.x, self._position.y, marker='o', markersize=3)

    if len(self._trajectory) != 0:
      x_locs = [t.x for t in self._trajectory]
      y_locs = [t.y for t in self._trajectory]

      plt.plot(x_locs, y_locs)
 
