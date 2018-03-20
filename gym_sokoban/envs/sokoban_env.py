import numpy as np
import random
import tkinter
import gym
from gym import error, spaces, utils

class SokobanEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    """ This gym implements a simple Sokoban environment. """
    
    def __init__(self):
        
        # general variables
        self.MAX_STEPS = 120
        self.curr_step = -1
        self.player_pos = (-1,-1)
        self.is_finish = False
        self.world = None
        self.past_world = None
        
        # action and observation spaces
        self._action_set = [1, 2, 3, 4]
        self.action_space = spaces.Discrete(len(self._action_set))
        self.observation_space = None
        
        #rendering
        self.root = tkinter.Tk()
        
        
    def step(self, a):
        action = self._action_set[a]
        if self.is_finish:
            raise RuntimeError("Episode is done")
        self.curr_step += 1
        self._take_action(action)
        reward = self._get_reward()
        observation = self._get_state()
        info = {}
        if self.curr_step == self.MAX_STEPS:
            self.is_finish = True
        return observation, reward, self.is_finish, info
    
    def reset(self):
        #.. TODO
        self.world = generate_level(height=h, width=w, boxes=b)
        self.root.destroy()
        pass
    
    def render(self, mode='human', close=False):
        #function to visualise the problem
        CODE = {'W':'#808000',
       'E':'#FFFFFF',
       'T':'#008000',
       'B':'#00FFFF',
       'P':'#FFFF00',
       'X':'#808000'}
        r = lambda x: CODE[x]
        x, y = self.world.shape
        [tkinter.Label(self.root, text=self.world[i,j], bg=r(self.world[i,j])).grid(row=i,column=j)\
         for i in range(0,x) for j in range(0,x)]
        self.root.mainloop()
    
    def _move_y(self, x, y, aux=None, option=1):
        # move the player in upward/downward direction
        if option == 2 and aux != None: #encountered a box
            op = self._get_opt(x,aux)
            if op == 1 or op == 2: #encountered a box or a wall at auxilliary position
                pass
            elif op == 3 or op == 4: #encountered an empty tile or a target tile at auxilliary position
                self._update_player()
                self.world[aux,x] = 'B'
                self.world[y,x] = 'P'
                self.player_pos = (x,y)
        elif option == 3: #encountered an empty tile
            self._update_player()
            self.world[y,x] = 'P'
            self.player_pos = (x,y)
        elif option == 4: #encountered a target tile
            self._update_player()
            self.world[y,x] = 'X'
            self.player_pos = (x,y)
    
    def _move_x(self, x, y, aux=None, option=1):
        # move the player in left/right direction
        if option == 2 and aux != None: #encountered a box
            op = self._get_opt(aux,y)
            if op == 1 or op == 2: #encountered a box or a wall at auxilliary position
                pass
            elif op == 3 or op == 4: #encountered an empty tile or a target tile at auxilliary position
                self._update_player()
                self.world[y,aux] = 'B'
                self.world[y,x] = 'P'
                self.player_pos = (x,y)
        elif option == 3: #encountered an empty tile
            self._update_player()
            self.world[y,x] = 'P'
            self.player_pos = (x,y)
        elif option == 4: #encountered a target tile
            self._update_player()
            self.world[y,x] = 'X'
            self.player_pos = (x,y)
    
    def _update_player(self):
        # update the player position
        x, y = self.player_pos
        if self.world[y,x] == 'P': #pure player tile
            self.world[y,x] = 'E'
        elif self.world[y,x] == 'X': #player standing on a target tile
            self.world[y,x] = 'T'
    
    def _get_opt(self,x,y):
        # for any action, return the code for the next tile encountered
        if self.world[y,x] == 'W':  #encounters a wall at (x,y)
            return 1
        elif self.world[y,x] == 'B': #encounters  a box at (x,y)
            return 2
        elif self.world[y,x] == 'E': #encounters an empty tile at (x,y)
            return 3
        elif self.world[y,x] == 'T': #encounters a target tile at (x,y)
            return 4
    
    def _take_action(self, action):
        # change the matrix representation according to the action specified
        self.past_world = self.world
        new_x, new_y = self.player_pos
        # MOVE LEFT
        if action == 1: 
            new_x = new_x-1
            opt = self._get_opt(new_x, new_y)
            if opt == 2: #encountered a box, do a push-ahead mechanism
                x2 = new_x-1
                self._move_x(new_x, new_y, aux=x2, option=opt)
            elif opt == 3 or opt == 4: #encountered an empty tile or a target tile
                self._move_x(new_x, new_y, option=opt)
        # MOVE RIGHT
        elif action == 2:
            new_x = new_x+1
            opt = self._get_opt(new_x, new_y)
            if opt == 2: #encountered a box, do a push-ahead mechanism
                x2 = new_x+1
                self._move_x(new_x, new_y, aux=x2, option=opt)
            elif opt == 3 or opt == 4: #encountered an empty tile or a target tile
                self._move_x(new_x, new_y, option=opt)
        # MOVE UP
        elif action == 3:
            new_y = new_y-1
            opt = self._get_opt(new_x, new_y)
            if opt == 2: #encountered a box, do a push-ahead mechanism
                y2 = new_y-1
                self._move_y(new_x, new_y, aux=y2, option=opt)
            elif opt == 3 or opt == 4: #encountered an empty tile or a target tile
                self._move_y(new_x, new_y, option=opt)
        # MOVE DOWN
        else:
            new_y = new_y+1
            opt = self._get_opt(new_x, new_y)
            if opt == 2: #encountered a box, do a push-ahead mechanism
                y2 = new_y+1
                self._move_y(new_x, new_y, aux=y2, option=opt)
            elif opt == 3 or opt == 4: #encountered an empty tile or a target tile
                self._move_y(new_x, new_y, option=opt)
    
    def _check_state(self):
        # return integer associated with reward/punishment states after comparing current and previous states
        unique_p, counts_p = numpy.unique(self.past_world, return_counts=True)
        unique_c, counts_c = numpy.unique(self.world, return_counts=True)
        info_p = dict(zip(unique_p, counts_p))
        info_c = dict(zip(unique_c, counts_c))
        
        past_targets = info_p['T']
        try:    
            curr_targets = info_c['T']
            if 'X' in info_c.keys():
                curr_targets = curr_targets + info_c['X']
            if 'X' in info_p.keys():
                past_targets = past_targets + info_p['X']
            if past_targets > curr_targets:
                return 2
            if past_targets < curr_targets:
                return 3
            elif past_targets == curr_targets:
                return 4
        except KeyError:
            self.is_finish = True
            return 1
            
        return -1
    
    def _get_state(self):
        # return the current state observation
        return 
    
    def _get_reward(self):
        if _check_state() == 1: #all the boxes are placed
            return 10
        elif _check_state() == 2: #a box was placed on a target
            return 1
        elif _check_state() == 3: #a box was removed from the target
            return -1
        elif _check_state() == -1: #undefined state
            return 0
        else: #player changes its position without any consequence
            return -0.1