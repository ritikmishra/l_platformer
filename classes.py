import pygame, random, level, sys, time
width = 1024
height = 576
screen = pygame.display.set_mode((width, height))
pygame.mixer.init ()


class Obtainium(pygame.sprite.Sprite):
	"""We'll want a way to increase score or there's no point in telling the score"""
	
	def __init__(self, screen, width, height, img, posX = False, posY = False, rock=False):
		"""Initializes essential variables, loads image, places image, etc..."""
		self.picked = False
	
		super(Level).__init__(Level)
		self.screen = screen
		self.img = pygame.image.load(img)
		self.change = 0
		self.size = self.img.get_size()
		self.mask = pygame.mask.from_surface(self.img)
		self.height = self.size[1]
		self.width = self.size[0]
		self.screen_width = width
		self.rock = rock
		if self.width == 23:
			self.change = 1
		elif self.width == 64:
			self.change = 2
		
		if not posX:
			self.posX = width/2
		else:
			self.posX = posX
		
		if not posY:
			self.posY = height-110
		else:
			self.posY = posY
		self.rect = pygame.Rect((self.posX, self.posY), self.size)
	def display(self, character_obj):
		"""I'm sure that the coin needs to be seen and located before it is obtained"""
		if self.picked == False:
			self.screen.blit(self.img, (self.posX, self.posY))
			
		
		if pygame.sprite.collide_rect(self, character_obj) and (not self.picked):
			if pygame.sprite.collide_mask(self, character_obj):
				if self.rock:
					self.picked = True
					character_obj.rocks += 1
				else:
					self.picked = True
					character_obj.deaths += self.change
					
	def scroll(self, direction):
		"""If the player has triggerred a scroll, we want the coin to move offscreen."""
		if direction == 'right':
			self.posX -= self.screen_width
			self.rect = pygame.Rect((self.posX, self.posY), self.size)
		elif direction == 'left':
			self.posX += self.screen_width		
			self.rect = pygame.Rect((self.posX, self.posY), self.size)


class PowerUp(pygame.sprite.Sprite):
	"""We'll want powerups, or the game will be less fun"""
	
	def __init__(self, screen, width, height, image, posX = False, posY = False):
		"""Initializes essential variables, loads image, places image, etc..."""
		self.picked = False
	
		super(Level).__init__(Level)
		self.screen = screen
		self.img = pygame.image.load(image)
		
		self.size = self.img.get_size()
		self.mask = pygame.mask.from_surface(self.img)
		self.height = self.size[1]
		self.width = self.size[0]
		self.screen_width = width
		
		if not posX:
			self.posX = width/2
		else:
			self.posX = posX
		
		if not posY:
			self.posY = height-110
		else:
			self.posY = posY
		self.rect = pygame.Rect((self.posX, self.posY), self.size)
	def display(self, character_obj):
		"""I'm sure that the coin needs to be seen and located before it is obtained"""
		if self.picked == False:
			self.screen.blit(self.img, (self.posX, self.posY))
		
		if pygame.sprite.collide_rect(self, character_obj) and (not self.picked):
			self.picked = True
			if character_obj.speed > 8:
				character_obj.speed -= 8
			elif character_obj.speed > 0:
				character_obj.speed -= character_obj.speed-1
			else:
				pass
			pygame.key.set_repeat(100, character_obj.speed)
			
	def scroll(self, direction):
		"""If the player has triggerred a scroll, we want the powerup to move offscreen."""
		if direction == 'right':
			self.posX -= self.screen_width
			self.rect = pygame.Rect((self.posX, self.posY), self.size)
		elif direction == 'left':
			self.posX += self.screen_width		
			self.rect = pygame.Rect((self.posX, self.posY), self.size)	
class Level(pygame.sprite.Sprite):
	"""The ground"""
	def __init__(self, screen, width, height, image):
		"""Makes essential variables, loads the image, and sets the initial scroll"""
		super(Level).__init__(Level)
		self.screen = screen
		self.image = pygame.image.load(image)
		self.mask = pygame.mask.from_surface(self.image)
		self.size = self.image.get_size()
		self.height = self.size[1]
		self.width = self.size[0]
		self.screen_width = width
		self.posX=(-576)*2
		self.posY=height - self.height
		self.rect = pygame.Rect((self.posX, self.posY), self.size)
		self.mask = pygame.mask.from_surface(self.image)
		
					
	def display(self):
		"""Shows the ground"""
		self.screen.blit(self.image, (self.posX, self.posY))
		self.rect = pygame.Rect((self.posX, self.posY), self.size)
	def scroll(self, direction):
		"""If the player is far enough to either side, we want to move the ground so the player can see the new ground"""
		if direction == 'right':
			self.posX -= self.screen_width
		elif direction == 'left':
			self.posX += self.screen_width
			
class Character(pygame.sprite.Sprite):
	"""Contains all the functions and variables that only the player needs"""
	def __init__(self, screen, width, height):
		super(Level).__init__(Level)
		"""Creates all the essential variables. Also loads image, which is very important"""
		self.forward_img = pygame.image.load("resources/Ginger_forward.png")
		self.right_img = pygame.image.load("resources/Ginger_right.png")
		self.left_img = pygame.image.load("resources/Ginger_left.png")
		
		self.forward_size = self.forward_img.get_size()
		self.right_size = self.right_img.get_size()
		self.left_size = self.left_img.get_size()
		
		#self.forward_mask = pygame.mask.from_surface(self.forward_img)
		#self.right_mask = pygame.mask.from_surface(self.right_img)
		#self.left_mask = pygame.mask.from_surface(self.left_img)
		self.health = 3
		self.rocks = 0
		self.size = self.forward_size
		self.image = self.forward_img
		#self.mask = self.forward_mask
		
		self.screen = screen
		self.posY = height/2
		self.posX = width/2
		self.screen_width = width
		self.screen_height = height
		self.error_sound = pygame.mixer.Sound("resources/error.mp3")
	
		self.rect = pygame.Rect((self.posX, self.posY), self.size)
		self.deaths = 0
		self.speed = 50
  
		
	def move(self, ground_rect, direction='forward', coin_obj=[], powerup_obj=[]):
		"""We want to be able to move """
		if not pygame.sprite.collide_rect(self, ground_rect):
			if not pygame.sprite.collide_mask(self, ground_rect):
				self.posY +=2
				#self.mask = self.forward_mask
				self.screen.blit(self.image, (self.posX, self.posY))
				self.rect = pygame.Rect((self.posX, self.posY), self.size)
		if direction == 'left':
			self.size = self.left_size
			self.image = self.left_img
			#self.mask = self.left_mask
			self.posX -= 4
			self.screen.blit(self.image, (self.posX, self.posY))
			self.rect = pygame.Rect((self.posX, self.posY), self.size)
		if direction == 'right':
		   self.size = self.right_size
		   self.image = self.right_img
		   #self.mask = self.right_mask
		   self.posX += 4
		   self.screen.blit(self.image, (self.posX, self.posY))
		   self.rect = pygame.Rect((self.posX, self.posY), self.size)
	
		if direction == 'up' and pygame.sprite.collide_mask(self, ground_rect):
			#self.size = self.forward_size
			#self.image = self.forward_img
			#self.mask = self.forward_mask
			self.screen.blit(self.image, (self.posX, self.posY))
			self.rect = pygame.Rect((self.posX, self.posY), self.size)
			for x in list(reversed(range(self.size[0]))):
				self.posY -= x/4

			
		
		
		if pygame.sprite.collide_rect(self, ground_rect):
			if pygame.sprite.collide_mask(self, ground_rect):
				self.screen.blit(self.image, (self.posX, self.posY))
			else:
				self.posY +=1
				self.size = self.forward_size
				self.image = self.forward_img
				#self.mask = self.forward_mask
				self.screen.blit(self.image, (self.posX, self.posY))
				self.rect = pygame.Rect((self.posX, self.posY), self.size)

					
		if self.posY > self.screen_height:
			if self.posX < self.screen_width/2:
				self.posX = self.screen_width-102
				self.posY = self.screen_height/2
			else:
				self.posX = 102
				self.posY = self.screen_height/2
			self.deaths -= 1		
		
		
		
		if self.posX >= self.screen_width:
			self.posX = 3
			ground_rect.scroll('right')
			for obj in coin_obj:
				obj.scroll('right')
			for obj in powerup_obj:
				obj.scroll('right')
		
			self.screen.blit(self.image, (self.posX, self.posY))
			self.rect = pygame.Rect((self.posX, self.posY), self.size)
		elif self.posX <= 0:
			self.posX = self.screen_width-3
			ground_rect.scroll('left')
			for obj in coin_obj:
				obj.scroll('left')
			for obj in powerup_obj:
				obj.scroll('left')
			self.screen.blit(self.image, (self.posX, self.posY))
			self.rect = pygame.Rect((self.posX, self.posY), self.size)
		def shoot(self, rock):
			if self.rocks > 0:
				rock.shoot()
			else:
				self.error_sound.play()
				


class Cloud:
    """ 'And God said 'Let there be clouds!' ' """
    def __init__(self):
        global height, width, screen
        self.img = pygame.image.load("resources/8bit_cloud.png")
        self.size = self.img.get_size()
        self.screen = screen
        self.altitude = random.randint(0, (height/3)/self.size[1]) * self.size[1] 
        self.position = random.randint(0, width)
        
    def move(self):
        global height, width, screen
        self.position += 0.5        
        self.screen.blit(self.img, (self.position,self.altitude))
        
        if self.position == width+self.size[0]:
            self.altitude = random.randint(0, (height/2)/self.size[1]) * self.size[1] 
            self.position = 0-self.size[0]
            
class StartMenuItem(pygame.sprite.Sprite):
    """ God: 'Dammit how do I start this man-damn game?'
        Jeffery: 'Just click that little sprite part of the StartMenuItem Class' """
    def __init__(self, img_location, posY, centered=True, posX=None):
        global height, width, screen
        super(StartMenuItem).__init__(StartMenuItem)
        self.img = pygame.image.load(str(img_location))
        

        self.size = self.img.get_size()
        self.screen = screen
        self.altitude = int(posY)
        if centered:
            self.posX = (width / 2) - (self.size[0] / 2)
        else:
            self.posX = posX
            
        self.rect = pygame.Rect((self.posX, self.altitude), self.size)
    def display(self, buttontype='Text'):
        self.screen.blit(self.img, (self.posX, self.altitude))
        
            
    def clicked(self, buttontype):
        global running, width, height
        if buttontype == 'quit':
            sys.exit()
        elif buttontype == 'start':
            level.main(width, height)
