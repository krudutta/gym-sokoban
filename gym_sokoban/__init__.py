from gym.envs.registration import register

register(
    id='sokoban-v0',
    entry_point='gym_sokoban.envs:SokobanEnv',
)