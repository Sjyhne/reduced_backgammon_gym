import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

from backgammon import Backgammon

class BackgammonEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    self.gym = Backgammon()
    
    # OBSERVATION
    obs_low, obs_high = self.gym.get_observation_space()
    obs_low = np.array(obs_low)
    obs_high = np.array(obs_high)
    self.observation_space = spaces.Box(low=obs_low, high=obs_high, dtype=np.int8)

    # ACTION
    action_low, action_high = self.gym.get_action_space()
    action_low = np.array(action_low)
    action_high = np.array(action_high)
    self.action_space = spaces.Box(low=action_low, high=action_high, dtype=np.int8)


  def step(self, action):
    ...
  def reset(self):
    ...
  def render(self, mode='human', close=False):
    ...

env = BackgammonEnv()

print(env.gym.board)
print(env.observation_space)