'''Topology generation: Given an initial width*height room entirely
constituted by wall blocks, the topology generation consists in creating the ‘empty’ spaces (i.e.
corridors) where boxes, targets and the player can be placed. For this simple random walk algorithm
with a configurable number of steps is applied: a random initial position and direction are chosen.
Afterwards, for every step, the position is updated and, with a probability p = 0.35, a new random
direction is selected. Every ‘visited’ position is emptied together with a number of surrounding wall
blocks, selected by randomly choosing one of the following patterns indicating the adjacent room
blocks to be removed (the darker square represents the reference position, that is, the position being
visited). Note that the room ‘exterior’ walls are never emptied, so from a width×height room only
a (width-2)×(height-2) space can actually be converted into corridors. The random walk approach
guarantees that all the positions in the room are, in principle, reachable by the player. A relatively
small probability of changing the walk direction favours the generation of longer corridors, while
the application of a random pattern favours slightly more convoluted spaces. 
Defaul parameters:
• A maximum of 10 room topologies and for each of those 10 boxes/player positioning are
retried in case a given combination doesn’t produce rooms with a score > 0.
• The room configuration tree is by default limited to a maximum depth of 300 applied actions.
• The total number of visited positions is by default limited to 1000000.
• Default random-walk steps: 1.5× (room width + room height).
'''

'''
1-l
2-r
3-u
4-d

'''

import numpy as np
import random as rn

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class BoxAndEmptySpaceError(Error):
	def __init__(self, message):
		self.message = message


class Box:
	def __init__(self, x, y):
		self.x=x
		self.y=y
		self.is_solved=False
		
	def placed(self):
		self.is_solved=True
	
class Player:
	init_x=-1
	init_y=-1
	def __init__(self, x=None, y=None, direction=None):
		self.x=x
		self.y=y
		self.d=direction
		
	'''place a player anywhere in the room'''	
	def place_player(self, x_new, y_new, d_new):
		self.x=x_new
		self.y=y_new
		self.d=d_new
			
	'''move the player 1 position in the direction given'''		
	def move_player(self, d, width, height):
		if(d==1):
			self.x=self.x-1
		elif(d==2):
			self.x=self.x+1
		elif(d==3):
			self.y=self.y-1
		elif(d==4):
			self.y=self.y+1
		'''for handling walls'''	
		if(self.x==0): 
			self.x=1
			self.move_player(2,width, height)
		elif(self.x==width-1): 
			self.x=width-2
			self.move_player(1,width, height) 
		elif(self.y==0): 
			self.y=1
			self.move_player(4,width, height)
		elif(self.y==height-1): 
			self.y=width-2
			self.move_player(3,width, height)
		

class Room:
	boxes=[]
	player=Player()  '''why do i need this? Player only comes in the picture 
	when we want to do reverse playing or real playing. This object is most 
	probably only useful to reuse the moving code. For reverse playing, 
	if there's a different function then it'll have it's own object for 
	room and player and box. currently the only reason these objects exist 
	in this class is to create a room with certain topology.'''
	empty_spaces=0
	empty_space_list=[]
	target_tile_list=[]
	
	def __init__(self, height, width, box_num):
		self.width=width
		self.height=height
		self.box_num=box_num
		self.room = np.full((height,width), 'W')
				
	def get_tile(self, x, y):
		return self.room[x][y]
	
	def set_tile(self, x, y, c):
		self.room[x][y]=c


	def choose_random_dir(self, d):
		'''select a new direction and then check yes(35%) and no(65%). 
		If yes, change, else dont'''
		d1=np.random.randint(1,4)
		b = [0,1]
		c=np.random.choice(b,1,p=[0.65,0.35])
		if(c):
			return d1
		else:
			return d
	
	def update_space(self, x, y, sym):	
		if(x==0 or x==self.width-1 or y==0 or y==self.height-1):
			pass
		else:
			self.set_tile(x,y,sym)
	
	def print_room(self):
		print(self.room)
	
	def find_empty_spaces(self):
		for i in range(self.height):
			for j in range(self.width):
				if(self.get_tile(i,j) == 'E'):
					self.empty_spaces+=1
					self.empty_space_list.append((i,j))
	
	def get_random_empty_space(self,n):
		return rn.sample(self.empty_space_list,n)
	
	def player_initpos(self,x,y):
		self.player.init_x=x
		self.player.init_y=y
		self.player.place_player(x,y,np.random.randint(1,4))
		
	def topology_gen(self):
		p=self.player
		p.x=np.random.randint(1,self.width-2) 
		p.y=np.random.randint(1,self.height-2)
		p.d=np.random.randint(1,4)
		self.set_tile(p.x, p.y, 'E')
		
		
		for i in range(int(1.5*(self.width+self.height))):
			t=np.random.randint(1,5)
			if(t==1):
				self.update_space(p.x-1, p.y, 'E')
				self.update_space(p.x+1, p.y, 'E')
			elif(t==2):
				self.update_space(p.x, p.y+1, 'E')
				self.update_space(p.x, p.y-1, 'E')
			elif(t==3):
				self.update_space(p.x-1, p.y, 'E')
				self.update_space(p.x, p.y-1, 'E')
			elif(t==4):
				self.update_space(p.x, p.y-1, 'E')
				self.update_space(p.x-1, p.y-1, 'E')
				self.update_space(p.x-1, p.y, 'E')
			elif(t==5):
				self.update_space(p.x+1, p.y, 'E')
				self.update_space(p.x, p.y-1, 'E')
			
			p.d=self.choose_random_dir(p.d)
			p.move_player(p.d, self.width, self.height)
			self.set_tile(p.x, p.y, 'E')
		
		self.find_empty_spaces()
	
		
		
	def position_configuration(self):
		if(self.empty_spaces <= self.box_num):
			raise BoxAndEmptySpaceError("Number of boxes should be more than number of empty spaces")
			
		b_list=self.get_random_empty_space(self.box_num)
		for i in range(self.box_num):
			self.boxes.append(Box(b_list[i][0],b_list[i][1]))
			self.update_space(b_list[i][0],b_list[i][1],'B')
		
		self.player_initpos(np.random.randint(1,self.width-2), np.random.randint(1,self.height-2))
	
	'''i think that reverse playing is a completly different function
	as it needs to create 10 diiferent topologies for a given room and 
	select best from them as the output after doing reverse playing on 
	each configuration and calculation scores for eac of them '''
			
			
				
				
				
print(int(1.5*16))			
r=Room(8,8,2)
r.topology_gen()
r.print_room()
r.position_configuration()
r.print_room()

	


		
		
	


