class RandomAgent:
    def __init__(self):
        ...

    def apply_random_action(self, environment):
        num_actions = environment.get_n_actions()
        executed = False
        obs = environment.get_current_observation()

        done = False
        winner = None

        n_actions_exec = 0

        #print("ROLL:", environment.gym.non_used_dice)

        for _ in range(num_actions):
            actions = environment.gym.get_valid_actions(environment.current_agent)
            acts = [i[1] for i in actions]
            #print(environment.get_valid_actions())
            c = 0
            if len(actions) > 0:
                for _ in actions:
                    action = random.choice(acts)
                    next_observation, reward, done, winner, executed = environment.step(action)
                    if executed:
                        obs = next_observation
                        #print("R EXECUTED:", action)
                        n_actions_exec += 1
                        break
                    else:
                        acts.remove(action)
                        c += 1

                if c == len(acts):
                    break

        return obs, done, winner, n_actions_exec
