import gym
import random

class RandomAgent:
    def __init__(self, color):
        self.color = color

    def choose_random_action(self, actions):
        return random.choice(actions)

if __name__ == '__main__':

    env = gym.make('reduced_backgammon_gym:reducedBackgammonGym-v0')
    observation = env.reset()

    agents = {env.gym.white: RandomAgent(env.gym.white), env.gym.black: RandomAgent(env.gym.black)}

    agent = agents[env.current_agent]

    env.render(0)
    
    for _ in range(env.max_episodes):

        env.render()
        
        n_actions = env.get_n_actions()
        
        for a in range(n_actions):
            executed = False
            actions = env.get_actions()
            for _ in actions:
                action = agent.choose_random_action(actions)
                next_observation, reward, done, winner, executed = env.step(action)
                if executed == True:
                    break
                else:
                    actions.remove(action)

        if done == True:
            if winner != None:
                print("AGENT:", agent.color, "WON")
                env.render()
            break
        
        env.change_player_turn()