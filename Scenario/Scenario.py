from Map import Map
from RandomWalkIntruder import RandomWalkIntruder
from Environmental import Environmental
import pygame

class Handler:
  # Action is a function taking a scenario and returning None
  def __init__(self):
    self._should_delete = False

  def Do(self, scenario):
    raise Exception("Not Implemented")
  
  def __call__(self, scenario):
    self.Do(scenario)
    
  def Kill(self):
    self._should_delete = True

  def IsDead(self):
    return self._should_delete

class Scenario:
  def __init__(self):
    self._clock = pygame.time.Clock()
    self._map = Map()
    
    intruder = RandomWalkIntruder(self._map) 
    environmental = Environmental(self._map) 
    
    self._map.RegisterIntruder(intruder, 0)
    self._map.RegisterEnvironmental(environmental, 0)
    
    self._running = False

    self._handlers = []
    self._rate = 30

    self._stop_requested = False
    
    self._prev_time = 0
    self._game_time = 0

  def GetMap(self):
    return self._map

  def AddHandler(self, handler):
    if not isinstance(handler, Handler):
      raise Exception("Tried to add handler of invalid type")
    self._handlers.append(handler)

  # Stops the simulation after the current iteration ends.
  def RequestStop(self):
    self._stop_requested = True

  # Generally use RequestStop instead
  def _Stop(self):
    self._running = False

  def Start(self):
    self._running = True

  def GetTime(self):
    dt = self._clock.get_time() * 1e-3
    self._game_time += dt
    return self._game_time

  def __del__(self):
    pygame.quit()

  def Run(self):
    self._prev_time = 0
    self._game_time = 0
   
    self.Start()
    while self._running:
      if self._stop_requested:
        self._Stop()

      self._game_time = self.GetTime()
      self._map.Update(self._game_time)
      self._prev_time = self._game_time
    
      # Delete dead handlers
      self._handlers = list(filter(
        lambda h: not h.IsDead(), self._handlers
      ))

      for handler in self._handlers: 
        handler(self)
      
      self._clock.tick(self._rate)
      
