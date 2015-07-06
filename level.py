def main(width, height):
	#import modules
	import pygame
	import os
	import random
	import time
	#create the screen
	dimensions = (width, height)
	window = pygame.display.set_mode(dimensions)
	no_heli_y = []
	no_heli_x = []
	
		
	#helps with making the close button in the corner work
	running = 1
	class PowerUp(pygame.sprite.Sprite):
		def __init__(self, screen, width, height, image, version, posX = False, posY = False):
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
			self.screen.blit(self.image, (self.posX, self.posY))
		def speedup(self, character_obj):
			if pygame.sprite.collide_rect(self, character_obj):
				character_obj.posX += self.size[0]

		def __str__(self):
			return "Type: " +  str(self.version) + "\n Location: " +  str(self.rect)
			
			
	class Level(pygame.sprite.Sprite):
		def __init__(self, screen, width, height, image):
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
			self.screen.blit(self.image, (self.posX, self.posY))
			self.rect = pygame.Rect((self.posX, self.posY), self.size)
		def scroll(self, direction,distance):
			
			if direction == 'right':
				self.posX -= self.screen_width + distance
			elif direction == 'left':
				self.posX += self.screen_width - distance
	class Character(pygame.sprite.Sprite):
		"""Contains all the functions and variables that only the helicopter needs"""
		def __init__(self, screen, width, height):
			super(Level).__init__(Level)
			"""Creates all the essential variables"""
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



	#The user's helicopter
	level = Level(window, width, height, "Level 1a.png")
	gingerman = Character(window, width, height)
	speedup = PowerUp(window, width, height, 'arrow.png', 'Launcher', False, 125)
	
		
	score = 0
	#gameloop
	pygame.key.set_repeat(100, 50)
	while running:
		#makes the close button functional
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				running = 0
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					gingerman.move(level, 'left')
				if event.key == pygame.K_RIGHT:
					gingerman.move(level, 'right')
				if event.key == pygame.K_SPACE:
					gingerman.move(level, 'up')

		#makes the background blue 
		window.fill((135, 206, 235))
		level.display()
		#speedup.display()
		
	
		
		#speedup.speedup(gingerman)
		gingerman.move(level)
		pygame.display.flip()

if __name__ == '__main__':
	main(1204, 576)
