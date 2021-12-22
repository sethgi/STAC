from Map import Map
from RandomWalkIntruder import RandomWalkIntruder
from Environmental import Environmental
from Scenario import Handler, Scenario

import pygame
from palettable.matplotlib import Viridis_20
import numpy as np

class Renderer(Handler):
  def __init__(self):
    super().__init__()
    
    self._screen = pygame.display.set_mode([1000,1000])
    self._colormap = Viridis_20.get_mpl_colormap()

  def Do(self, scenario):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self._should_delete = True
        scenario.RequestStop()
        return

    x,y = np.mgrid[0:100:1, 0:100:1]
    pos = np.dstack((x,y))
    pos = np.divide(pos, 10)
    pos = np.subtract(pos, 5)
    values = scenario.GetMap().GetEnvironmentalValues(pos)[0]

    colors = np.multiply(self._colormap(values.flatten())[:,:3], 255)
    colors = np.reshape(colors, (100,100,3))

    surf = pygame.surfarray.make_surface(colors)
    surf = pygame.transform.scale(surf, (1000,1000))
    self._screen.blit(surf, (0,0))
    
    for x,y in scenario.GetMap().GetIntruderLocations():
      x_pixels = (x + 5) * 100
      y_pixels = (y + 5) * 100

      pygame.draw.circle(self._screen, (255, 0, 0), (x_pixels, y_pixels), 10)
       
    pygame.display.update()

if __name__ == "__main__":
  scenario = Scenario()
  renderer = Renderer()

  scenario.AddHandler(renderer)
  scenario.Run()
