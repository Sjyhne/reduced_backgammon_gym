import gym
import random

class RandomAgent:
    def __init__(self, color):
        self.color = color

    def apply_random_action(self, environment):
        n_actions = environment.get_n_actions()
        executed = False
        actions = environment.get_actions()
        for _ in actions:
            action = random.choice(actions)
            next_observation, reward, done, winner, executed = env.step(action)
            if executed:
                break
            else:
                actions.remove(action)
        
        return next_observation, done, winner

if __name__ == '__main__':

    env = gym.make('reduced_backgammon_gym:reducedBackgammonGym-v0')
    observation = env.reset()

    agents = {env.gym.white: RandomAgent(env.gym.white), env.gym.black: RandomAgent(env.gym.black)}

    agent = agents[env.current_agent]

    for _ in range(env.max_episodes):

        env.render()
        
        next_observation, done, winner = agent.apply_random_action(env)
        observation = next_observation
        print(observation)
        if done == True:
            if winner != None:
                print("AGENT:", agent.color, "WON")
                env.render()
            break


        
        env.change_player_turn()