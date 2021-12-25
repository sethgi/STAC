from Map import Map
from RandomWalkIntruder import RandomWalkIntruder
from Environmental import Environmental
from Scenario import Handler, Scenario
from Sampler import Sampler

import pygame
from palettable.matplotlib import Viridis_20
import numpy as np

class Renderer(Handler):
  def __init__(self):
    super().__init__()
    
    self._screen = pygame.display.set_mode([1900,1000])
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
       
    for gauss in scenario._map._environmentals[0]._gaussians:
      x,y = gauss.mean
      x_pixels = (x + 5) * 100
      y_pixels = (y + 5) * 100
      pygame.draw.circle(self._screen, (0,255,255), (x_pixels, y_pixels), 5)

    sampler = scenario.GetHandler("sampler")

    for s in sampler._buffer:
      x_pixels = (s.x + 5) * 100
      y_pixels = (s.y + 5) * 100
      pygame.draw.circle(self._screen, (255,255,0), (x_pixels, y_pixels), 5)

    current_estimate, current_uncertainty = sampler.GetCurrentModel()
    projection, projection_uncertainty =  sampler.GetProjectionOfNow()
   
    def plot_gp(estimate, uncertainty, x_pos, y_pos):
      if estimate is None:
        return
      
      estimate_colors = np.multiply(self._colormap(estimate.flatten())[:,:3],255)
      estimate_colors = np.reshape(estimate_colors, (100,100,3))

      estimate_surf = pygame.transform.scale(
        pygame.surfarray.make_surface(estimate_colors),
        (400,400))

      uncertainty_colors = np.multiply(self._colormap(uncertainty.flatten())[:,:3],255)
      uncertainty_colors = np.reshape(uncertainty_colors, (100,100,3))

      uncertainty_surf = pygame.transform.scale(
        pygame.surfarray.make_surface(uncertainty_colors),
        (400,400))
      
      self._screen.blit(estimate_surf, (x_pos + 50, y_pos + 50))
      self._screen.blit(uncertainty_surf, (x_pos + 500, y_pos + 50))
    
    plot_gp(current_estimate, current_uncertainty, 1000, 0)
    plot_gp(projection, projection_uncertainty, 1000, 500)

    pygame.display.update()

if __name__ == "__main__":
  scenario = Scenario()
  renderer = Renderer()
  sampler = Sampler(scenario)

  scenario.AddHandler(renderer, "renderer")
  scenario.AddHandler(sampler, "sampler")
  scenario.Run()
