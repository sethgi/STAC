
class Point2:
  def __init__(self, x = None, y = None):
    self.x = x
    self.y = y

class Pose2:
  def __init__(self, x = None, y = None, theta = None):
    self.x = x
    self.y = y
    self.theta = theta

class State2:
  def __init__(self, x = None, y = None, theta = None, 
               velocity = None, angular_velocity = None):
    self.pose = Pose2(x,y,theta)
    self.velocity = velocity
    self.angular_velocity = angular_velocity
