from gym.envs.registration import register

register(
    id='backgammon_gym-v0',
    entry_point='gym_foo.envs:BackgammonEnv',
)