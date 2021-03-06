import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import random

from reduced_backgammon_gym.envs.backgammon import Backgammon

class BackgammonEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self, max_episodes=10_000):

    self.gym = Backgammon(n_spots=7, n_home_positions=2, n_pieces=4, dice_sides=2, max_n_stack=4, double_chance=0.3)

    self.max_episodes = max_episodes
    
    # OBSERVATION
    obs_nvec = self.gym.get_observation_space()
    self.observation_space = spaces.MultiDiscrete(nvec=np.array(obs_nvec, dtype=np.int8))

    # ACTION
    action_nvec = self.gym.get_action_space()
    self.action_space = spaces.MultiDiscrete(nvec=np.array(action_nvec, dtype=np.int8))

    # STARTING AGENT
    self.current_agent = self.gym.starting_agent

    self.round_nr = 1

  # Returns all "possible" actions based on the dice roll
  def get_actions(self):
    return self.gym.alternate_generate_actions(self.current_agent)

  def get_n_actions(self):
    return len(self.gym.non_used_dice)

  # Steps through and environment - An agent will be able to step through the environment
  # Several times before it is the other players turn
  def step(self, action):
    """
      Returns True if the action was "accepted" and executed
      Returns False if the action was "declined" and not executed
    """

    src, dst = action

    reward = 0

    done = False

    winner = None

    executed = False

    all_valid_actions = self.gym.get_valid_actions(self.current_agent)
    # [(1, (0, 7)), (2, (0, 7)), ..]

    a_actions = [i[1] for i in all_valid_actions]
    # [(0, 7), (2, 1),]
    # Sender inn (0, 7)
    
    idxs = [i for i, x in enumerate(a_actions) if x == action]

    # action = all_actions[idxs[0]]
    if len(idxs) > 0:
      action = all_valid_actions[idxs[0]]


    if len(idxs) > 0:
      #print(action)
      executed = self.gym.alternate_execute_action(self.current_agent, action)
    else:
      reward = -1 

    current_observation = self.gym.get_current_observation()
    
    if self.round_nr == self.max_episodes:
      done = True
    elif self.gym.off[self.current_agent] == self.gym.n_pieces:
      winner = self.current_agent
      done = True
      reward = 1

    return tuple(current_observation), reward, done, winner, executed

  def get_valid_actions(self):
    return self.gym.get_valid_actions(self.current_agent)
  
  # Resets the environment/gym
  def reset(self):
    self.gym = Backgammon()
    self.current_agent = self.gym.starting_agent
    self.round_nr = 0
    return tuple(self.gym.get_current_observation(self.current_agent)), self.current_agent

  # Changes the players turn and increments the round number
  def change_player_turn(self):
    self.round_nr += 1
    self.current_agent = self.gym.white if self.current_agent == self.gym.black else self.gym.black
    self.gym.roll()

  # Renders the game, only mode is "human"
  def render(self, mode='human'):
    self.gym.render(self.round_nr)
    print()
    

  def set_starting_state_and_player(self, state):
    player_spots = state[:7]
    bar_count = state[7:9]
    dice = state[9:]

    board = []

    for i in range(self.gym.n_spots):
        count = None
        color = None
        if player_spots[i] > self.gym.n_pieces:
            count = player_spots[i] - self.gym.n_pieces
            color = 1
        else:
            count = player_spots[i]
            color = 0
        
        board.append({"count": count, "color": color})
        self.gym.board[i].update({"count": count, "color": color})

    self.gym.bar[0] = bar_count[0]
    self.gym.bar[1] = bar_count[1]

    self.gym.off[0] = self.gym.n_pieces - sum([i["count"] if i["color"] == 0 else 0 for i in board]) - self.gym.bar[0]
    self.gym.off[1] = self.gym.n_pieces - sum([i["count"] if i["color"] == 1 else 0 for i in board]) - self.gym.bar[1]

    if dice == [1, 0]:
        self.gym.non_used_dice = [1, 1, 1, 1]
    elif dice == [1, 1]:
        self.gym.non_used_dice = [1, 2]
    else:
        self.gym.non_used_dice = [2, 2, 2, 2]

    self.current_agent = 1

if __name__ == '__main__':
    bg = BackgammonEnv()
    bg.render()

    bg.set_starting_state_and_player([1, 0, 5, 5, 2, 6, 0, 1, 0, 1, 0])
