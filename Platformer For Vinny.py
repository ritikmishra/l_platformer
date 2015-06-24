import pygame, random

width = 640
height = 400
screen = pygame.display.set_mode((width, height))
bgcolor = 135, 206, 235
running = 1

class Cloud:
	def __init__(self):
		global height, width, screen
		self.img = pygame.image.load("8bit_cloud.png")
		self.size = self.img.get_size()
		self.screen = screen
		self.altitude = random.randint(0, (height/2)/self.size[1]) * self.size[1] 
		self.position = random.randint(0, width)
		
	def move(self):
		self.position += 0.5
		
		self.screen.blit(self.img, (self.position,self.altitude))
		if self.position == 480+self.size[0]:
			self.altitude = random.randint(0, (height/2)/self.size[1]) * self.size[1] 
			self.position = 0-self.size[0]
			
cloud1 = Cloud()
cloud2 = Cloud()
cloud3 = Cloud()

while running:
	event = pygame.event.poll()
	if event.type == pygame.QUIT:
		running = 0
	
	screen.fill(bgcolor)
	cloud1.move()
	cloud2.move()
	cloud3.move()
	pygame.display.flip()
