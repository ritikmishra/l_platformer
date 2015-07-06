def main(width, height):
	#import modules
	import pygame
	import os
	import random
	import time
	
	#create the screen
	dimensions = (width, height)
	window = pygame.display.set_mode(dimensions)
	
	#helps with making the close button in the corner work
	running = 1
	
	class PowerUp(pygame.sprite.Sprite):
		"""We'll want powerups, or the game will be less fun"""
		
		def __init__(self, screen, width, height, image, version, posX = False, posY = False):
			"""Initializes essential variables, loads image, places image, etc..."""
		
			super(Level).__init__(Level)
			self.version = version
			self.screen = screen
			self.preimg = pygame.image.load(image)
			

			self.size = self.preimg.get_size()
			self.image = pygame.transform.scale(self.preimg, ( int(self.size[0]/18), int(self.size[1]/18) ) )
			self.mask = pygame.mask.from_surface(self.image)
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
			
		
		def display(self):	
			"""Shows image"""
			self.screen.blit(self.image, (self.posX, self.posY))
		def speedup(self, character_obj):
			"""Applies powerup. In this case, a speedup."""
			if pygame.sprite.collide_rect(self, character_obj):
				character_obj.posX += self.size[0]

		def __str__(self):
			"""If we want to print the function, the print statement will output important info"""
			return "Type: " +  str(self.version) + "\n Location: " +  str(self.rect)
			
			
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
			self.posX=-731
			self.posY=height - self.height
			self.rect = pygame.Rect((self.posX, self.posY), self.size)
			self.mask = pygame.mask.from_surface(self.image)
			
		def display(self):
			"""Shows the ground"""
			self.screen.blit(self.image, (self.posX, self.posY))
			self.rect = pygame.Rect((self.posX, self.posY), self.size)
		def scroll(self, direction,distance):
			"""If the player is far enough to either side, we want to move the ground so the player can see the new ground"""
			if direction == 'right':
				self.posX -= self.screen_width + distance
			elif direction == 'left':
				self.posX += self.screen_width - distance
				
	class Character(pygame.sprite.Sprite):
		"""Contains all the functions and variables that only the player needs"""
		def __init__(self, screen, width, height):
			super(Level).__init__(Level)
			"""Creates all the essential variables. Also loads image, which is very important"""
			self.forward_img = pygame.image.load("Ginger_forward.png")
			self.right_img = pygame.image.load("Ginger_right.png")
			self.left_img = pygame.image.load("Ginger_left.png")
			
			self.forward_size = self.forward_img.get_size()
			self.right_size = self.right_img.get_size()
			self.left_size = self.left_img.get_size()
			
			#self.forward_mask = pygame.mask.from_surface(self.forward_img)
			#self.right_mask = pygame.mask.from_surface(self.right_img)
			#self.left_mask = pygame.mask.from_surface(self.left_img)
			
			self.size = self.forward_size
			self.image = self.forward_img
			#self.mask = self.forward_mask
			
			self.screen = screen
			self.posY = height/2
			self.posX = width/2
			self.screen_width = width
			
			self.rect = pygame.Rect((self.posX, self.posY), self.size)
   
		
		def move(self, ground_rect, direction='forward'):
			"""We want to be able to move """
			if not pygame.sprite.collide_rect(self, ground_rect):
				if not pygame.sprite.collide_mask(self, ground_rect):
					self.posY +=1
					self.size = self.forward_size
					self.image = self.forward_img
					#self.mask = self.forward_mask
					self.screen.blit(self.image, (self.posX, self.posY))
					self.rect = pygame.Rect((self.posX, self.posY), self.size)
			if direction == 'left':
				self.size = self.left_size
				self.image = self.left_img
				#self.mask = self.left_mask
				self.posX -= 10
				self.screen.blit(self.image, (self.posX, self.posY))
				self.rect = pygame.Rect((self.posX, self.posY), self.size)
			if direction == 'right':
			   self.size = self.right_size
			   self.image = self.right_img
			   #self.mask = self.right_mask
			   self.posX += 10
			   self.screen.blit(self.image, (self.posX, self.posY))
			   self.rect = pygame.Rect((self.posX, self.posY), self.size)
		
			if direction == 'up':
				self.posY -=5
				self.size = self.forward_size
				self.image = self.forward_img
				#self.mask = self.forward_mask
				self.screen.blit(self.image, (self.posX, self.posY))
				self.rect = pygame.Rect((self.posX, self.posY), self.size)
			
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

					
				
			if self.posX >= self.screen_width - 100:
				self.posX = 101
				ground_rect.scroll('right', 101)
				self.screen.blit(self.image, (self.posX, self.posY))
				self.rect = pygame.Rect((self.posX, self.posY), self.size)
			elif self.posX <= 100:
				self.posX = self.screen_width -101
				ground_rect.scroll('left', 101)
				self.screen.blit(self.image, (self.posX, self.posY))
				self.rect = pygame.Rect((self.posX, self.posY), self.size)



	#The ground
	level = Level(window, width, height, "Level 1a.png")
	
	#The character, who's sprite is a gingerbread man
	gingerman = Character(window, width, height)
	
	#The powerup
	speedup = PowerUp(window, width, height, 'arrow.png', 'Launcher', False, 125)
	
	#If the arrow keys are held down, we want the character to continously move. This helps with that.	
	pygame.key.set_repeat(100, 50)
	
	#Gameloop, executes all the actions
	while running:
		
		#Gets a list of what's happening
		events = pygame.event.get()
		
		#Reads the list of what's happening
		for event in events:
			
			#Exits program if red X cliked
			if event.type == pygame.QUIT:
				running = 0
			
			#Moves the character if the keys are pressed
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					gingerman.move(level, 'left')
				if event.key == pygame.K_RIGHT:
					gingerman.move(level, 'right')
				if event.key == pygame.K_SPACE:
					gingerman.move(level, 'up')

		#makes the background blue 
		window.fill((135, 206, 235))
		
		#Shows the level
		level.display()
		
		#speedup.display() |This is commented because the speedup is glitchy
		
		
	
		
		#speedup.speedup(gingerman) |This is commented because the speedup is glitchy
		
		#Makes sure physics applies
		gingerman.move(level)
		
		#Shows everything
		pygame.display.flip()

if __name__ == '__main__':
	main(1204, 576)
