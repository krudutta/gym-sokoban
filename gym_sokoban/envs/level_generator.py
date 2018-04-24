import numpy as np
import random as rn
from collections import deque
from math import log

class Error(Exception):
    '''Base class for exceptions in this module.'''
    pass

class BoxAndEmptySpaceError(Error):
	def __init__(self, message):
		self.message = message
	
class Room:
	
	
	def __init__(self, height, width, box_num):
		self.boxes=[]
		self.target_tile_list=[]
		self.player_curpos=[]
		self.width=width
		self.height=height
		self.box_num=box_num
		self.room = np.full((height,width), 'W')
		
	def print_room(self):
		print(self.room)

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
			
	def get_tile(self, x, y):
		return self.room[y][x]
	
	def set_tile(self, x, y, c):
		self.room[y][x]=c
	
	def update_space(self, x, y, sym):	
		if(x<=0 or x>=self.width-1 or y<=0 or y>=self.height-1):
			return False
		else:
			self.set_tile(x,y,sym)
			return True
		
	def topology_gen(self, walk_steps):
		dirn=[1,2,3,4]
		x=np.random.randint(1,self.width-2) 
		y=np.random.randint(1,self.height-2)
		d=np.random.randint(1,4)
		self.update_space(x,y,'E')
		for i in range(walk_steps):
			t=np.random.randint(1,5)
			if(t==1):
				self.update_space(x-1, y, 'E')
				self.update_space(x+1, y, 'E')
			elif(t==2):
				self.update_space(x, y+1, 'E')
				self.update_space(x, y-1, 'E')
			elif(t==3):
				self.update_space(x-1, y, 'E')
				self.update_space(x, y-1, 'E')
			elif(t==4):
				self.update_space(x, y-1, 'E')
				self.update_space(x-1, y-1, 'E')
				self.update_space(x-1, y, 'E')
			elif(t==5):
				self.update_space(x+1, y, 'E')
				self.update_space(x, y-1, 'E')
			d=self.choose_random_dir(d)
			if(d==1):
				x=x-1
			elif(d==2):
				x=x+1
			elif(d==3):
				y=y-1
			elif(d==4):
				y=y+1
			if(self.update_space(x,y,'E')):
				continue
			else:
				if(d==1):
					x=x+1
				elif(d==2):
					x=x-1
				elif(d==3):
					y=y+1
				elif(d==4):
					y=y-1	
				i-=1

	def position_configuration(self):
		#boxes config	
		for i in range(self.box_num):
			while(True):
				x=np.random.randint(1,self.width-2) 
				y=np.random.randint(1,self.height-2)
				if(self.get_tile(x,y)=='E'):
					self.target_tile_list.append((x,y))
					self.set_tile(x,y,'X') #setting this as X cuz initially B is on T. S
					self.boxes.append([x,y])
					break
				else:
					continue
		#player config
		while(True):
			x=np.random.randint(1,self.width-2) 
			y=np.random.randint(1,self.height-2)
			if(self.get_tile(x,y)=='E'):
				self.set_tile(x,y,'P')
				self.set_player_curpos(x,y)
				break
			else:
				continue
	
	def is_target_tile(self, x, y):
		for i in range(self.box_num):
			if self.target_tile_list[i][0]==x and self.target_tile_list[i][1]==y:
				return True
		return False
	
	def which_box(self, x, y):
		for i in range(self.box_num):
			if self.boxes[i][0]==x and self.boxes[i][1]==y:
				return i
		raise Exception("NO BOX FOUND")
				
	def set_player_curpos(self,x,y):
		self.player_curpos=[]
		self.player_curpos.append(x)
		self.player_curpos.append(y)
	
	def update_box_pos(self, i, x, y):
		self.boxes[i][0]=x
		self.boxes[i][1]=y
	
	def make_move(self,x,y, m):
		if(m==1):
			if(self.get_tile(x-1,y)=='E'):
				self.set_tile(x,y,'E')
				self.set_tile(x-1,y,'P')
				self.set_player_curpos(x-1,y)
				return True
		elif(m==2):
			if(self.get_tile(x+1,y)=='E'):
				self.set_tile(x,y,'E')
				self.set_tile(x+1,y,'P')
				self.set_player_curpos(x+1,y)
				return True
		elif(m==3):
			if(self.get_tile(x,y+1)=='E'):
				self.set_tile(x,y,'E')
				self.set_tile(x,y+1,'P')
				self.set_player_curpos(x,y+1)
				return True
		elif(m==4):
			if(self.get_tile(x,y-1)=='E'):
				self.set_tile(x,y,'E')
				self.set_tile(x,y-1,'P')
				self.set_player_curpos(x,y-1)
				return True
		elif(m==5):
			if((self.get_tile(x+1,y)=='B' or self.get_tile(x+1,y)=='X') and self.get_tile(x-1,y)=='E'):
				bi=self.which_box(x+1,y)
				if(self.get_tile(x+1,y)=='X'):
					self.set_tile(x+1,y,'T')
				else:
					self.set_tile(x+1,y,'E')
				if self.is_target_tile(x,y):
					self.set_tile(x,y,'X')
				else:
					self.set_tile(x,y,'B')
				self.update_box_pos(bi, x,y)
				self.set_tile(x-1,y,'P')
				self.set_player_curpos(x-1,y)
				return True	
			else:
				return False	
		elif(m==6):
			if((self.get_tile(x-1,y)=='B' or self.get_tile(x-1,y)=='X') and self.get_tile(x+1,y)=='E'):
				bi=self.which_box(x-1,y)
				if(self.get_tile(x-1,y)=='X'):
					self.set_tile(x-1,y,'T')
				else:
					self.set_tile(x-1,y,'E')
				if self.is_target_tile(x,y):
					self.set_tile(x,y,'X')
				else:
					self.set_tile(x,y,'B')
				self.update_box_pos(bi, x,y)
				self.set_tile(x+1,y,'P')
				self.set_player_curpos(x+1,y)
				return True
			else:
				return False
		elif(m==7):#down
			if((self.get_tile(x,y-1)=='B' or self.get_tile(x,y-1)=='X') and self.get_tile(x,y+1)=='E'):
				bi=self.which_box(x,y-1)
				if(self.get_tile(x,y-1)=='X'):
					self.set_tile(x,y-1,'T')
				else:
					self.set_tile(x,y-1,'E')
				if self.is_target_tile(x,y):
					self.set_tile(x,y,'X')
				else:
					self.set_tile(x,y,'B')
				self.update_box_pos(bi, x,y)
				self.set_tile(x,y+1,'P')
				self.set_player_curpos(x,y+1)
				return True
		elif(m==8):
			if((self.get_tile(x,y+1)=='B' or self.get_tile(x,y+1)=='X') and self.get_tile(x,y-1)=='E'):
				bi=self.which_box(x,y+1)
				if(self.get_tile(x,y+1)=='X'):
					self.set_tile(x,y+1,'T')
				else:
					self.set_tile(x,y+1,'E')
				if self.is_target_tile(x,y):
					self.set_tile(x,y,'X')
				else:
					self.set_tile(x,y,'B')
				self.update_box_pos(bi, x,y)
				self.set_tile(x,y-1,'P')
				self.set_player_curpos(x,y-1)
				return True
		elif(m==-5):
			bi=self.which_box(x+1,y)
			if self.is_target_tile(x,y):
				self.set_tile(x,y,'T')
			else:
				self.set_tile(x,y,'E')
			self.set_tile(x+1,y,'P')
			if self.is_target_tile(x+2,y):
				self.set_tile(x+2,y,'X')
			else:
				self.set_tile(x+2,y,'B')
			self.set_player_curpos(x+1,y)
			self.update_box_pos(bi,x+2,y)
			
		elif(m==-6):
			bi=self.which_box(x-1,y)
			if self.is_target_tile(x,y):
				self.set_tile(x,y,'T')
			else:
				self.set_tile(x,y,'E')
			self.set_tile(x-1,y,'P')
			if self.is_target_tile(x-2,y):
				self.set_tile(x-2,y,'X')
			else:
				self.set_tile(x-2,y,'B')
			self.set_player_curpos(x-1,y)
			self.update_box_pos(bi,x-2,y)
			
		elif(m==-7):
			bi=self.which_box(x,y-1)
			if self.is_target_tile(x,y):
				self.set_tile(x,y,'T')
			else:
				self.set_tile(x,y,'E')
			self.set_tile(x,y-1,'P')
			if self.is_target_tile(x,y-2):
				self.set_tile(x,y-2,'X')
			else:
				self.set_tile(x,y-2,'B')
			self.set_player_curpos(x,y-1)
			self.update_box_pos(bi,x,y-2)
			
		elif(m==-8):
			bi=self.which_box(x,y+1)
			if self.is_target_tile(x,y):
				self.set_tile(x,y,'T')
			else:
				self.set_tile(x,y,'E')
			self.set_tile(x,y+1,'P')
			if self.is_target_tile(x,y+2):
				self.set_tile(x,y+2,'X')
			else:
				self.set_tile(x,y+2,'B')
			self.set_player_curpos(x,y+1)
			self.update_box_pos(bi,x,y+2)	
			
	def reset_position_configuration(self):
		for i in range(self.box_num):
			self.set_tile(self.boxes[i][0],self.boxes[i][1], 'E')
		for i in range(self.box_num):	
			self.set_tile(self.target_tile_list[i][0], self.target_tile_list[i][1], 'T')
		self.set_tile(self.player_curpos[0],self.player_curpos[1], 'E')
		 	
	def set_position_configuration(self, c):
		j=0
		for i in range(self.box_num):
			self.boxes[i][0]=c[j]
			j+=1
			self.boxes[i][1]=c[j]
			if self.is_target_tile(c[j-1], c[j]):
				self.set_tile(self.boxes[i][0],self.boxes[i][1], 'X')
			else:
				self.set_tile(self.boxes[i][0],self.boxes[i][1], 'B')
			j+=1

		self.player_curpos[0]=c[j]
		j+=1
		self.player_curpos[1]=c[j]
		self.set_tile(c[j-1],c[j],'P')
	
	def create_config_obj(self):
		pos_conf=[]
		for i in range(self.box_num):
			pos_conf.append(self.boxes[i][0])
			pos_conf.append(self.boxes[i][1])
		pos_conf.append(self.player_curpos[0])
		pos_conf.append(self.player_curpos[1])
		return tuple(pos_conf) 				

class Tree:
	def __init__(self):
		self.child=[]
		self.data=()
	
	def create_child(self):
		self.child.append(Tree())

def create_config_tree(room):  #it takes a single position config and creates a move tree for it. 
	moves=[1,2,3,4,5,6,7,8]
	depth=0
	explored=set()
	conf_tree=Tree()
	conf_tree.data=room.create_config_obj()
	explored.add(room.create_config_obj())
	rn.shuffle(moves)
	child_q=deque()
	nodes_num=0
	i=0
	for m in moves:
		nodes_num+=1
		mm=False
		mm=room.make_move(room.player_curpos[0],room.player_curpos[1],m) #mm: move made bool
		c=room.create_config_obj()
		if c not in explored:  
			explored.add(c)
			conf_tree.create_child()
			conf_tree.child[i].data=c
			child_q.append(conf_tree.child[i])
			i+=1
		#reverse the move made	
		if m<5 and m%2==0 and mm:
			m-=1
			room.make_move(room.player_curpos[0],room.player_curpos[1],m)
		elif m<5 and mm:
			m+=1
			room.make_move(room.player_curpos[0],room.player_curpos[1],m)
		elif mm:
			m=m*-1
			room.make_move(room.player_curpos[0],room.player_curpos[1],m)	

	while((len(child_q)!=0) and (depth<=300)):
		rn.shuffle(moves)
		ch=child_q.popleft()
		room.reset_position_configuration()
		room.set_position_configuration(ch.data)
		i=0
		t=0
		depth=log(nodes_num,8)
		for m in moves:
			nodes_num+=1
			mm=False
			mm=room.make_move(room.player_curpos[0],room.player_curpos[1],m) #mm: move made bool
			c=room.create_config_obj()
			if c not in explored:  
				explored.add(c)
				ch.create_child()
				ch.child[i].data=c
				child_q.append(ch.child[i])
				i+=1
			if m<5 and m%2==0 and mm:
				m-=1
				room.make_move(room.player_curpos[0],room.player_curpos[1],m)
			elif m<5 and mm:
				m+=1
				room.make_move(room.player_curpos[0],room.player_curpos[1],m)
			elif mm:
				m=m*-1
				room.make_move(room.player_curpos[0],room.player_curpos[1],m)
		
	return conf_tree	

#-------------score calculator-----------------------------------------

root_data=()

def calc_score( tup1, tup2, swaps, cur_box, num_b ):
	for j in range(num_b):
		t=j
		if(j!=cur_box and (tup1[j+t] != tup2[j+t] or 
		   tup1[j+t+1] != tup2[j+t+1])):
			if cur_box==-1:
				cur_box=j
			else:
				cur_box=j
				swaps+=1		
	manh_d=0
	for j in range(num_b*2):
		manh_d+= abs(tup1[j]-tup2[j])
	score_gen = swaps*(manh_d)
	return score_gen, cur_box

#for depth first traversal of a tree
def tree_dfs(conf_tree, max_score, swaps, cur_box, parent_d, num_b, max_config=(0,0,0,0)):
	if parent_d==-1:
		pass
	else:
		score_gen, cur_box = calc_score(root_data, conf_tree.data, swaps, cur_box, num_b)
		if score_gen>max_score:
			max_score=score_gen
			max_config=conf_tree.data	
	for i in range(len(conf_tree.child)):
		parent_d=conf_tree.data
		max_score, max_config = tree_dfs(conf_tree.child[i], max_score, swaps, cur_box, parent_d, num_b, max_config)
	
	return max_score, max_config		
	
#calculates score for one tree
def score_controller(conf_tree):
	if conf_tree.child==[]:
		return 0, 0
	global root_data
	root_data=conf_tree.data
	num_b=int((len(conf_tree.data)-2)/2)
	score=0
	max_config=()
	score, max_config = tree_dfs(conf_tree, 0, 0, -1, -1, num_b)
	return score, max_config

def level_generator(width, height, num_box):
	for i in range(10):
		rm=Room(height, width, num_box)
		rm.topology_gen(int(1.5*(height+width)))
		rm.position_configuration()
		tre=create_config_tree(rm)			
		score, max_config = score_controller(tre)
		if score>0:
			rm.reset_position_configuration()
			rm.set_position_configuration(max_config)
			return rm.room
		del rm
		del tre
