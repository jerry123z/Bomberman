"""Jerry Zheng
May 5th 2015
BOMBERMAN Sprites"""

import pygame, random
screen = pygame.display.set_mode((640, 480))

class Player(pygame.sprite.Sprite):
    """The player's charater sprite which they will play as and control"""
    def __init__(self, player_num):
	"""The initializer method that takes the player number as a parameter
	it then loads all of the images sets variables for loading the images, the rect
	for the sprite, the speed variables, the lives, speed, number of bombs,
	explosion radius, a death variable, a movement variable and the sound
	effects"""
	pygame.sprite.Sprite.__init__(self)
	# load images
	self.__downs = [pygame.image.load("Sprites/players/" + str(player_num) +"_down_1.gif"),\
	                pygame.image.load("Sprites/players/" + str(player_num) +"_down_2.gif"),\
	                pygame.image.load("Sprites/players/" + str(player_num) +"_down_3.gif")]
	self.__lefts = [pygame.image.load("Sprites/players/" + str(player_num) +"_left_1.gif"),\
	                pygame.image.load("Sprites/players/" + str(player_num) +"_left_2.gif"),\
	                pygame.image.load("Sprites/players/" + str(player_num) +"_left_3.gif")]
	self.__rights = [pygame.image.load("Sprites/players/" + str(player_num) +"_right_1.gif"),\
	                pygame.image.load("Sprites/players/" + str(player_num) +"_right_2.gif"),\
	                pygame.image.load("Sprites/players/" + str(player_num) +"_right_3.gif")]
	self.__ups = [pygame.image.load("Sprites/players/" + str(player_num) +"_up_1.gif"),\
	                pygame.image.load("Sprites/players/" + str(player_num) +"_up_2.gif"),\
	                pygame.image.load("Sprites/players/" + str(player_num) +"_up_3.gif")]
	self.__deaths = [pygame.image.load("Sprites/players/" + str(player_num) +"_death_1.gif"),\
	                pygame.image.load("Sprites/players/" + str(player_num) +"_death_2.gif"),\
	                pygame.image.load("Sprites/players/" + str(player_num) +"_death_3.gif"),\
	                pygame.image.load("Sprites/players/" + str(player_num) +"_death_4.gif")]
	self.__push_up = [True, pygame.image.load("Sprites/players/" + str(player_num) +"_push_up.gif")]
	
	self.__push_down = [True, pygame.image.load("Sprites/players/" + str(player_num) +"_push_down.gif")]
	self.__push_left = [True, pygame.image.load("Sprites/players/" + str(player_num) +"_push_left.gif")]
	self.__push_right = [True, pygame.image.load("Sprites/players/" + str(player_num) +"_push_right.gif")]
	
	for lists in [self.__downs, self.__lefts, self.__rights, self.__ups]:
	    for img in range(3):
		lists[img].set_colorkey((255,255,255))
		
	for img in range(4):
	    self.__deaths[img].set_colorkey((255,255,255))
	for lists in [self.__push_up, self.__push_down, self.__push_left, self.__push_right]:
	    lists[1].set_colorkey((255,255,255))
	    
	#set the variables for controling animations
	self.__scroll = 1
	self.__current_list = self.__downs
	self.__image_num = 1
        self.image = self.__current_list[self.__image_num]
        self.rect = self.image.get_rect()
	self.__animation_pause = 0
	
	#list of rect values for different characters
	self.__xy_list = [(48,48), (432,48), (48, 432), (432, 432)]
	self.rect.center = self.__xy_list[player_num - 1]
	#more stat attributes
	self.__moving = False
	self.__dx = 0
	self.__dy = 0
        self.__lives = 1
        self.__speed = 2
        self.__bomb_num = 1
        self.__power = 1
        self.__kick = False
	self.__bomb_available = [0, -1, -1, -1]
	self.__num = str(player_num)
	self.__current_dir = (0,0)
	self.__dying = False
	self.__invincible = 0
	#sound effects
	self.__bomb_kick = pygame.mixer.Sound("Sprites/music/bomb_kick.wav")
	self.__bomb_kick.set_volume(0.5)	
	self.__bomb_set = pygame.mixer.Sound("Sprites/music/bomb_set.wav")
	self.__bomb_set.set_volume(0.5)
	self.__item_get = pygame.mixer.Sound("Sprites/music/item_get.wav")
	self.__item_get.set_volume(0.5)
	self.__die_sfx = pygame.mixer.Sound("Sprites/music/PLAYER_OUT.wav")
	self.__die_sfx.set_volume(0.4)
        
    def get_num(self):
	"""returns the player number attribute"""
	return str(self.__num)
    def get_lives(self):
	"""returns the life number variable"""
	return str(self.__lives)
    def get_bomb(self):
	"""returns the number of bombs"""
	return str(self.__bomb_num)
    def get_power(self):
	"""returns the explosion radius value"""
	return str(self.__power)
    def get_speed(self):
	"""returns the spped attribute"""
	return str(self.__speed)
    def get_kick(self):
	"""returns the value 'Yes' when the player obtains a kick power up and
	the label sprite needs to update"""
	return "Yes"
    
    def give_invincible(self):
	"""gives the player 60 frames or 2 seconds of invincibility"""
	self.__invincible = 60
	
    def get_dying(self):
	"""this method returns if the player is currently dying"""
	return self.__dying
    def boost(self, pu_type):
	"""takes the power up type as a parameter and increases the player's 
	corrosponding stat"""
	#max 4 bombs
	if pu_type == "bomb" and self.__bomb_num < 4:
	    self.__bomb_available[self.__bomb_num] = 0
	    self.__bomb_num += 1
	#max 10 power
	elif pu_type == "power" and self.__power < 10:
	    self.__power += 1
	    #max 8 speed
	elif pu_type == "speed" and self.__speed < 8:
	    self.__speed *= 2
	elif pu_type == "kick":
	    self.__kick = True
	elif pu_type == "lives":
	    self.__lives += 1
	self.__item_get.play()
	    
    def move(self, direction, grid, bomb_group):
	"""takes a tupple direction parameter, the game grid and the bomb group
	it then changes direction based on the direction given and if the ajacent
	space is blocked or not. If the ajacent space contains a bomb it checks
	if the player has the kick power up and if the next block is empty
	to let the player kick the bomb"""
	self.__current_dir = direction
	if not self.__moving:
	    if direction == (-1, 0) and grid[(str(self.rect.left -6 - 32) + str(self.rect.top))] == 'empty':
		self.__dx = self.__speed * (-1)
		self.__dy = 0
		self.__moving = True
		self.__current_list = self.__lefts
		self.__image_num = 1
		self.image = self.__current_list[self.__image_num]
	    elif direction == (1, 0) and grid[(str(self.rect.left -6 + 32) + str(self.rect.top))] == 'empty':
		self.__dx = self.__speed
		self.__dy = 0
		self.__moving = True
		self.__current_list = self.__rights
		self.__image_num = 1
		self.image = self.__current_list[self.__image_num]
	    elif direction == (0, -1) and grid[(str(self.rect.left -6) + str(self.rect.top + 32))] == 'empty':
		self.__dx = 0
		self.__dy = self.__speed
		self.__moving = True
		self.__current_list = self.__downs
		self.__image_num = 1
		self.image = self.__current_list[self.__image_num]
	    elif direction == (0, 1) and grid[(str(self.rect.left -6) + str(self.rect.top - 32))] == 'empty':
		self.__dx = 0
		self.__dy = self.__speed * (-1)
		self.__moving = True
		self.__current_list = self.__ups
		self.__image_num = 1
		self.image = self.__current_list[self.__image_num]
	    
	    #the conditions for if the player is able to kick the bomb
	    elif self.__kick == True and direction == (-1, 0)\
	         and grid[(str(self.rect.left -6 - 32) + str(self.rect.top))] == "bomb"\
	         and grid[(str(self.rect.left -6 - 64) + str(self.rect.top))] == "empty":
		for bomb in bomb_group:
		    if (str(bomb.rect.left) + str(bomb.rect.top )) == (str(self.rect.left -6 - 32) + str(self.rect.top)):
			grid[(str(self.rect.left -6 - 32) + str(self.rect.top))] = 'empty'
			self.__current_list = self.__push_left
			self.__image_num = 1			
			self.image = self.__current_list[self.__image_num]
			bomb.kick("left")
			self.__bomb_kick.play()
	    elif self.__kick == True and direction == (1, 0)\
	    and grid[(str(self.rect.left -6 + 32) + str(self.rect.top))] == "bomb"\
	    and grid[(str(self.rect.left -6 + 64) + str(self.rect.top))] == "empty":
		for bomb in bomb_group:
		    if (str(bomb.rect.left) + str(bomb.rect.top )) == (str(self.rect.left -6 + 32) + str(self.rect.top)):
			grid[(str(self.rect.left -6 + 32) + str(self.rect.top))] = 'empty'
			self.__current_list = self.__push_right
			self.__image_num = 1			
			self.image = self.__current_list[self.__image_num]
			bomb.kick("right")
			self.__bomb_kick.play()
	    elif self.__kick == True and direction == (0, 1)\
	         and grid[(str(self.rect.left -6) + str(self.rect.top - 32))] == "bomb"\
	         and grid[(str(self.rect.left -6) + str(self.rect.top - 64))] == "empty":
		for bomb in bomb_group:
		    if (str(bomb.rect.left) + str(bomb.rect.top )) == (str(self.rect.left -6) + str(self.rect.top - 32)):
			grid[(str(self.rect.left -6) + str(self.rect.top - 32))] = 'empty'
			self.__current_list = self.__push_up
			self.__image_num = 1			
			self.image = self.__current_list[self.__image_num]
			bomb.kick("up")
			self.__bomb_kick.play()
	    elif self.__kick == True and direction == (0, -1)\
	         and grid[(str(self.rect.left -6) + str(self.rect.top + 32))] == "bomb"\
	         and grid[(str(self.rect.left -6) + str(self.rect.top + 64))] == "empty":
		for bomb in bomb_group:
		    if (str(bomb.rect.left) + str(bomb.rect.top )) == (str(self.rect.left -6) + str(self.rect.top + 32)):
			grid[(str(self.rect.left -6) + str(self.rect.top + 32))] = 'empty'
			self.__current_list = self.__push_down
			self.__image_num = 1			
			self.image = self.__current_list[self.__image_num]
			bomb.kick("down")
			self.__bomb_kick.play()
	    
    def bomb(self):
	"""This method takes the player's x and y rects and then rounds them
	then returns them and the bomb's blast radius so that the rect for the
	bomb will be in the grid"""
	if self.rect.centerx % 32 < 17:
	    bombx = self.rect.centerx - (self.rect.centerx % 32)
	else:
	    bombx = self.rect.centerx + (32 - self.rect.centerx % 32)
	    
	if self.rect.centery % 32 < 17:
	    bomby = (self.rect.centery - (self.rect.centery % 32))
	else:
	    bomby = (self.rect.centery + (32 - self.rect.centery % 32))
	    
	self.__bomb_set.play()
	return bombx, bomby, self.__power
    
    def die(self):
	"""this method will make it so that the player cannot move, place bombs,
	and makes them go through the death animation"""
	if self.__dying == False:
	    self.__bomb_available = [-1, -1, -1, -1]
	    self.__dying = 38
	    self.__current_list = self.__deaths
	    self.__image_num = 0
	    self.__moving = True
	    self.image = self.__current_list[self.__image_num]
	
    def lose_life(self):
	"""this method makes the player lose a life if they are not invincible 
	and if that life is not the last one give_invincible method is called
	if it is the last one then the die method is called"""
	if self.__invincible == 0:
	    self.__lives -= 1
	    self.give_invincible()
	    if self.get_lives() == '0':
		self.__die_sfx.play()
		self.die()
	    
    def can_bomb(self):
	"""this checks if the player has any bombs available and if they do it
	disables the bomb until it explodes"""
	can_bomb = False
	for num in range(4):
	    if self.__bomb_available[num] == 0:
		can_bomb = True
		self.__bomb_available[num] = 120
		break
	return can_bomb
    
    def update(self, grid):
	"""the update method that takes the game grid as a parameter and changes the
	player's location based on the players speed. Also scrolls through the
	character's images to animate them"""
	#if it is the first or last image in the list then it reverses the animation order
	if self.__image_num == 0 and not self.__dying:
	    self.__scroll = 1
	elif self.__image_num == 2:
	    self.__scroll = -1
	    
	#if the animation is not paused and the player is not dying it goes to the
	#next frame
	if self.__animation_pause == 0 and not self.__dying:
	    if self.__moving == True:
		self.__image_num += self.__scroll
		self.image = self.__current_list[self.__image_num]
		self.__animation_pause = 5
	elif not self.__dying:
	    self.__animation_pause -= 1
	#if the player is invincible it takes one frame off of the invinciblility
	if self.__invincible > 0:
	    self.__invincible -= 1
	    
	#movement control
        self.rect.x += self.__dx
        self.rect.y += self.__dy
	if (str(self.rect.left - 6) + str(self.rect.top)) in grid and self.__current_dir == (0,0) and not self.__dying:
	    self.__dx = 0
	    self.__dy = 0
	    self.__moving = False
	    self.__image_num = 1
	    self.image = self.__current_list[self.__image_num]
	elif (str(self.rect.left - 6) + str(self.rect.top)) in grid and\
	    self.__dx > 0:
	    if grid[(str(self.rect.left - 6 + 32) + str(self.rect.top))] != 'empty' or self.__current_dir != (1,0):
		self.__dx = 0
		self.__dy = 0
		self.__moving = False
		self.__image_num = 1
		self.image = self.__current_list[self.__image_num]
		self.__current_dir = (0,0)
	elif (str(self.rect.left - 6) + str(self.rect.top)) in grid and\
	    self.__dx < 0:
	    if grid[(str(self.rect.left - 6 - 32) + str(self.rect.top))] != 'empty' or self.__current_dir != (-1,0):
		self.__dx = 0
		self.__dy = 0
		self.__moving = False
		self.__image_num = 1
		self.image = self.__current_list[self.__image_num]
		self.__current_dir = (0,0)
	elif (str(self.rect.left - 6) + str(self.rect.top)) in grid and\
	    self.__dy < 0:
	    if grid[(str(self.rect.left - 6) + str(self.rect.top - 32))] != 'empty' or self.__current_dir != (0,1):
		self.__dx = 0
		self.__dy = 0
		self.__moving = False
		self.__image_num = 1
		self.image = self.__current_list[self.__image_num]
		self.__current_dir = (0,0)
	elif (str(self.rect.left - 6) + str(self.rect.top)) in grid and\
	    self.__dy > 0:
	    if grid[(str(self.rect.left - 6) + str(self.rect.top + 32))] != 'empty' or self.__current_dir != (0,-1):
		self.__dx = 0
		self.__dy = 0
		self.__moving = False
		self.__image_num = 1
		self.image = self.__current_list[self.__image_num]
		self.__current_dir = (0,0)

	#makes the bombs available
	for num in range(4):
	    if self.__bomb_available[num] > 0:
		self.__bomb_available[num] -= 1
		
	#scrolls through the death animations
	if self.__dying:
	    self.__dx = 0
	    self.__dy = 0
	    self.__dying -= 1
	    if self.__dying == 0:
		self.kill()
	    elif self.__dying % 10 == 9:
		self.__image_num += 1
		self.image = self.__current_list[self.__image_num]
	    
	
class Wall(pygame.sprite.Sprite):
    """The unbreakable wall sprites"""
    def __init__(self, X, Y):
	"""the initializer method that takes x and y co-ordinate values and
	generates the rect with the values"""
	pygame.sprite.Sprite.__init__(self)
	self.image = pygame.image.load("Sprites/walls/wall.gif")
	self.rect = self.image.get_rect()
	self.rect.top = X
	self.rect.left = Y
	
class Brick(pygame.sprite.Sprite):
    """the breakable brick sprites"""
    def __init__(self, X, Y):
	"""the initializer method that takes x and y co-ordinate values and
	generates the rect with the values"""	
	pygame.sprite.Sprite.__init__(self)
	self.image = pygame.image.load("Sprites/walls/brick.gif")
	self.rect = self.image.get_rect()
	self.rect.top = X
	self.rect.left = Y
		
class Bomb(pygame.sprite.Sprite):
    """the bomb sprites that will explode to produce fire"""
    def __init__(self, rect_x, rect_y, power):
	"""the initializer method that takes x and y co-ordinate values and
	generates the rect with the values it also takes the power of the bomb
	from the player that spawned it"""	
	pygame.sprite.Sprite.__init__(self)
	#images
	self.__image_list = [pygame.image.load("Sprites/bombs/bomb1.gif"),\
	                     pygame.image.load("Sprites/bombs/bomb2.gif"),\
	                     pygame.image.load("Sprites/bombs/bomb3.gif")]
	for img in self.__image_list:
	    img.set_colorkey((255,255,255))
	#animation variables
	self.__scroll = 1
	self.__image_num = 2
	self.image = self.__image_list[self.__image_num]
	
	self.rect = self.image.get_rect()
	self.rect.top = rect_y
	self.rect.left = rect_x
	self.__dx = 0
	self.__dy = 0
	#the timer for the bomb that will control when it explodes
	self.__timer = 90
	self.__power = power
	
    def quick_explode(self):
	"""this method will change the time on the timer to 0. this will be called
	if the bomb is hit b the explosion by another bomb"""
	self.__timer = 0
	
    def get_power(self):
	"""this methodreturns the powervariable"""
	return self.__power
	
    def get_time(self):
	"""this method returns the time left until explosion"""
	return self.__timer
    
    def kick(self, direction):
	"""This method changes the bomb's speed variables based on a direction
	parameter that it recives"""
	if direction == "left":
	    self.__dx = -8
	if direction == 'right':
	    self.__dx = 8
	if direction == 'up':
	    self.__dy = -8
	if direction == "down":
	    self.__dy = 8
	    
    def update(self, grid):
	"""the update method for the bomb that takes the game grid as a parameter"""
	#if it is the first or last image in the list then it reverses the animation order
	if self.__image_num == 0:
	    self.__scroll = 1
	elif self.__image_num == 2:
	    self.__scroll = -1
	self.__timer -= 1
	
	#checks if the bomb is moving then will continue to move it unless it hits
	# a wall, brick or another bomb
	if self.__dx:
	    self.rect.x += self.__dx
	    if (str(self.rect.left) + str(self.rect.top)) in grid:
		if grid [(str(self.rect.left - 32) + str(self.rect.top))] != "empty" or grid [(str(self.rect.left + 32) + str(self.rect.top))] != "empty":
		    self.__dx = 0
		    grid[str(self.rect.left) + str(self.rect.top)] = 'bomb'

	elif self.__dy:
	    self.rect.y += self.__dy
	    if (str(self.rect.left) + str(self.rect.top)) in grid :
		if grid [(str(self.rect.left) + str(self.rect.top - 32))] != "empty" or grid [(str(self.rect.left) + str(self.rect.top + 32))] != "empty":
		    self.__dy = 0
		    grid[str(self.rect.left) + str(self.rect.top)] = 'bomb'

	
	#scrolls through the images
	if self.__timer % 10 == 0:
	    self.__image_num += self.__scroll
	    self.image = self.__image_list[self.__image_num]
	    
	#if the time is up it kills itself and opens up the space on the game grid
	if self.__timer == -1:
	    self.kill()
	    if (str(self.rect.left) + str(self.rect.top)) in grid:
		grid[(str(self.rect.left) + str(self.rect.top))] = 'empty'
		

class Fire(pygame.sprite.Sprite):
    """the fire sprite that is spawned when a bomb explodes"""
    def __init__(self, x, y, side):
	"""the initializer method that takes x,y values and which pictures
	to use as parameters"""
	pygame.sprite.Sprite.__init__(self)
	#images
	self.__image_list = [pygame.image.load("Sprites/explosion/"+side+"_4.gif"), pygame.image.load("Sprites/explosion/"+side+"_5.gif")]
	for img in self.__image_list:
	    img.set_colorkey((255,255,255))	
	self.__scroll = 1
	self.__image_num = 0
	self.image = self.__image_list[self.__image_num]
	self.rect = self.image.get_rect()
	
	self.rect.centerx = x
	self.rect.centery = y
	#timer
	self.__timer = 30
	self.__side = side
    
    def spawn_pu(self):
	"""this method will be called if a power up is spawned it will delete itself
	the return its own rect attributes"""
	self.kill()
	return self.rect.left, self.rect.top
	
    def update(self):
	"""the update method"""
	#timer
	if self.__timer == 0:
	    self.kill()
	self.__timer -= 1
	#animation
	if self.__image_num == 1:
	    self.__scroll = -1
	if self.__timer % 10 == 0:
	    self.__image_num += self.__scroll
	    self.image = self.__image_list[self.__image_num]
	
	    
class HUD(pygame.sprite.Sprite):
    """the hud sprite that will display each player's stats"""
    def __init__(self):
	"""initializer method for the hud"""
	pygame.sprite.Sprite.__init__(self)
	self.image = pygame.image.load("Sprites/HUD.gif")
	self.rect = self.image.get_rect()
	self.rect.right = 640
	self.rect.top = 0
	
class Label(pygame.sprite.Sprite):
    """label sprite to display text"""
    def __init__(self, message, x_y_center):
	"""the initializer method that takes a string variable and x,y co-ordinates"""
        pygame.sprite.Sprite.__init__(self)
        self.__font = pygame.font.SysFont("None", 30)
        self.__text = message
        self.__center = x_y_center
         
    def set_text(self, message):
	"""a method that changes the label's text based on the string arguement passed in"""
        self.__text = message
                 
    def update(self):
	"""the update method that renders the text and re-locates the rect"""
        self.image = self.__font.render(self.__text, 1, (0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.__center
	
class Power_Up(pygame.sprite.Sprite):
    """the powerup sprites that the player will aim to collect"""
    def __init__(self, left_top):
	"""the initializer method that takes an x,y tupple for the rect.left and
	rect.top attributes and generates a random powerup type"""
        pygame.sprite.Sprite.__init__(self)
	number = random.randint(1, 10)
	self.__invincible = 31
	if number in [1,2,3]:
	    self. image = pygame.image.load("Sprites/pu/pu bomb.gif")
	    self.rect = self.image.get_rect()
	    self.rect.left = left_top[0]
	    self.rect.top = left_top[1]
	    self.__type = "bomb"
	elif number in [4,5,6,7]:
	    self. image = pygame.image.load("Sprites/pu/pu power.gif")
	    self.rect = self.image.get_rect()
	    self.rect.left = left_top[0]
	    self.rect.top = left_top[1]
	    self.__type = "power"
	elif number in [8]:
	    self. image = pygame.image.load("Sprites/pu/pu speed.gif")
	    self.rect = self.image.get_rect()
	    self.rect.left = left_top[0]
	    self.rect.top = left_top[1]
	    self.__type = "speed"
	elif number in [9]:
	    self. image = pygame.image.load("Sprites/pu/pu kick.gif")
	    self.rect = self.image.get_rect()
	    self.rect.left = left_top[0]
	    self.rect.top = left_top[1]
	    self.__type = "kick"
	elif number in [10]:
	    self. image = pygame.image.load("Sprites/pu/pu 1-up.gif")
	    self.rect = self.image.get_rect()
	    self.rect.left = left_top[0]
	    self.rect.top = left_top[1]
	    self.__type = "lives"
	    
	    
    def get_invincible(self):
	"""a method that returns whether or not the power up is able to be destroyed"""
	return self.__invincible
    
    def get_type(self):
	"""returns the powerup type attribute"""
	return self.__type
    
    def update(self):
	"""the update method that reduces the power up's invincibility frames"""
	if self.__invincible > 0:
	    self.__invincible -= 1
