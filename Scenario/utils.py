import math

def WrapToPi(theta):
  while theta > 2*math.pi:
    theta -= 2*math.pi
  while theta < 2*math.pi:
    theta += 2*math.pi
  return theta
