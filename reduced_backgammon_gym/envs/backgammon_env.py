import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

from backgammon import Backgammon

class BackgammonEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    self.gym = Backgammon()
    
    low, high = self.gym.get_observation_space()
    low = np.array(low)
    high = np.array(high)
    self.observation_space = spaces.Box(low=low, high=high, dtype=np.int8)

  def step(self, action):
    ...
  def reset(self):
    ...
  def render(self, mode='human', close=False):
    ...

env = BackgammonEnv()

print(env.gym.board)
print(env.observation_space)