import matplotlib.pyplot as plt
import copy
from Intruder import Intruder
from Types import State2, Pose2
import numpy as np
import utils

ANG_ACCEL_MAGNITUDE = 0.15
ACCEL_MAGNITUDE = 0.025
MIN_VEL = 0
MAX_VEL = 0.22
MIN_ANG_VEL = -1
MAX_ANG_VEL = 1

DIST_THRESHOLD = 1

"""
Todo: Pass map to intruder and don't hardcode

Plan on longer horizon than update so we can update arbitrarily small while also planning longer horizon
  - move planning to its own thread and only replan when close to the end of an existing plan

"""

class IdGen:
  def __init__(self):
    self.count = 0

  def GetId(self):
    self.count += 1
    return self.count - 1

class Node:
  def __init__(self, state, parent, depth, new_id):
    self.state = state
    self.parent = parent
    self.children = []
    self.depth = depth
    self.id = new_id

  def BuildDictHelper(self, node, tree):
    tree[node] = node.children
    for n in node.children:
      self.BuildDictHelper(n, tree)

  def BuildDict(self):
    tree = {}
    self.BuildDictHelper(self, tree)
    return tree


class RandomWalkIntruder(Intruder):
  
  def __init__(self, global_map):
    super().__init__(global_map)
    
    x = 0
    y = 0
    theta = np.pi * np.random.rand()
    vel = 0.5
    ang_vel = 0.1
    self._state = State2(x,y,theta,vel,ang_vel)
    self._trajectory = []

    self._id_gen = IdGen()

  def Predict(self, pose, velocity, angular_velocity, dt):
    new_theta = utils.WrapToPi(pose.theta + angular_velocity * dt)

    if angular_velocity == 0:
      new_x = pose.x + velocity * np.cos(pose.theta)
      new_y = pose.y + velocity * np.sin(pose.theta)
    else:
      new_x = pose.x + (velocity / angular_velocity) * \
              (np.sin(pose.theta + angular_velocity * dt) -\
                np.sin(pose.theta))

      new_y = pose.y + (velocity / angular_velocity) * \
              (np.cos(pose.theta) - np.cos(pose.theta +\
                angular_velocity * dt))

    return Pose2(new_x, new_y, new_theta)

  def BFS(self, dt):
    
    start_node = Node(copy.deepcopy(self._state), None, 0,self._id_gen.GetId())

    search_queue = [start_node]

    while len(search_queue) > 0:
      active_node = search_queue.pop(0)
      if active_node.depth >= 5:
        break
      ang_accels = np.random.permutation(np.linspace(-ANG_ACCEL_MAGNITUDE, ANG_ACCEL_MAGNITUDE, 2))
      for ang_accel in ang_accels:
        new_ang_vel = active_node.state.angular_velocity + ang_accel
      
        if new_ang_vel < MIN_ANG_VEL or new_ang_vel > MAX_ANG_VEL:
          continue

        new_pose = self.Predict(active_node.state.pose, active_node.state.velocity, new_ang_vel, dt) 
        new_state = State2(new_pose.x, new_pose.y, new_pose.theta, active_node.state.velocity, new_ang_vel)
        # TODO: Better map handling
        if new_pose.x > 5 or new_pose.x < -5 or new_pose.y > 5 or new_pose.y < -5:
          continue

        search_queue.append(Node(new_state, active_node, active_node.depth + 1, self._id_gen.GetId()))
        active_node.children.append(search_queue[-1])
  
    # Breadcrumbs
    chosen_angular_vel = None
    while active_node.parent is not None:
      chosen_angular_vel = active_node.state.angular_velocity
      active_node = active_node.parent

    return active_node, chosen_angular_vel

  def DoUpdate(self, current_time, dt):

    active_node, chosen_angular_vel = self.BFS(dt)
    if chosen_angular_vel is None:
      self._state.pose.theta = np.arctan2(-self._state.pose.y, -self._state.pose.x)
      chosen_angular_vel = np.random.rand()*ANG_ACCEL_MAGNITUDE * 2 - ANG_ACCEL_MAGNITUDE

    new_pose = self.Predict(self._state.pose, self._state.velocity, chosen_angular_vel, dt)

    self._trajectory.append(self._state)
    self._state = State2(new_pose.x, new_pose.y, new_pose.theta, self._state.velocity, chosen_angular_vel)

    return active_node
  def Render(self):
    plt.plot(self._state.pose.x, self._state.pose.y, marker='o', markersize=15)

    if len(self._trajectory) != 0:
      x_locs = [t.pose.x for t in self._trajectory]
      y_locs = [t.pose.y for t in self._trajectory]

      plt.plot(x_locs, y_locs)

