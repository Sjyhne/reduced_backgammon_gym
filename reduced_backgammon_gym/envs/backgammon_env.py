import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

from backgammon import Backgammon, WHITE, BLACK

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

    # STARTING AGENT
    self.current_agent = self.gym.starting_agent

    self.round_nr = 1

  # Returns all "possible" actions based on the dice roll
  def get_actions(self):
    return self.gym.generate_actions(self.current_agent, self.dice)

  # Steps through and environment - An agent will be able to step through the environment
  # Several times before it is the other players turn
  def step(self, action):
    """
      Returns True if the action was "accepted" and executed
      Returns False if the action was "declined" and not executed
    """
    return self.gym.execute_action(action)
  
  # Resets the environment/gym
  def reset(self):
    self.gym = Backgammon()
    self.current_agent = self.gym.starting_agent

  # Changes the players turn and increments the round number
  def change_player_turn(self):
    self.round_nr += 1
    self.current_agent = WHITE if self.current_agent == BLACK else BLACK

  def render(self, mode='human'):
    self.gym.render(self.round_nr)

env = BackgammonEnv()

print(env.gym.board)
print(env.observation_space)