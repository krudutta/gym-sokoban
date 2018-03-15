import numpy as np
import random
import gym
from gym import error, spaces, utils
# from gym.utils import seeding

U = lambda arr, x, y: arr[x, y-1]
D = lambda arr, x, y: arr[x, y+1]
L = lambda arr, x, y: arr[x-1, y]
R = lambda arr, x, y: arr[x+1, y]

def generate_level(height=5, width=5, boxes=2):
    world = np.full((height,width), 'W')
    pos_x, pos_y = random.randint(1,height-1), random.randint(1,width-1)
    world[pos_x, pos_y] = 'E'
    while True:
        
    #.. TODO
    return world

class SokobanEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    """ This gym implements a simple Sokoban environment. """
    
    def __init__(self):
        
        # general variables
        self.MAX_STEPS = 120
        self.curr_step = -1
        self.is_finish = False
        self.world = None
        self.past_world = None
        
        # action and observation spaces
        self.action_space = None
        self.observation_space = None
        
        
    def step(self, action):
        if self.is_finish:
            raise RuntimeError("Episode is done")
        self.curr_step += 1
        self._take_action(action)
        reward = self._get_reward()
        observation = self._get_state()
        info = {}
        return observation, reward, self.is_finish, info
    
    def reset(self, h, w, b):
        #.. TODO
        self.world = generate_level(height=h, width=w, boxes=b)
        pass
    
    def render(self, mode='human', close=False):
        #.. TODO
        return
    
    def _take_action(self, action):
        #.. TODO
        # change the matrix representation according to the action specified
        return
    
    def _check_state(self):
        #.. TODO
        # return integer associated with reward/punishment states after comparing current and previous states
        return
    
    def _get_state(self):
        #.. TODO
        # return the current state observation
        return
    
    def _get_reward(self):
        if _check_state() == 1:
            return 10
        elif _check_state() == 2:
            return 1
        elif _check_state() == 3:
            return -1
        else:
            return -0.1