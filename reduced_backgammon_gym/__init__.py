from gym.envs.registration import register

register(
    id='reducedBackgammonGym-v0',
    entry_point='reduced_backgammon_gym.envs:BackgammonEnv',
)