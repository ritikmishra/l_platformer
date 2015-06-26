import pygame, random, level

width = 1024
height = 576
screen = pygame.display.set_mode((width, height))
bgcolor = 135, 206, 235
running = 1

class Cloud:
	""" 'And God said 'Let there be clouds!' ' """
	def __init__(self):
		global height, width, screen
		self.img = pygame.image.load("8bit_cloud.png")
		self.size = self.img.get_size()
		self.screen = screen
		self.altitude = random.randint(0, (height/3)/self.size[1]) * self.size[1] 
		self.position = random.randint(0, width)
		
	def move(self):
		self.position += 0.5
		
		self.screen.blit(self.img, (self.position,self.altitude))
		if self.position == 480+self.size[0]:
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
			running = 0
		elif buttontype == 'start':
			level.main(width, height)
class Character:
	def __init__(self):
		global height, width, screen
		self.posX = width/2
		self.posY = height/2
		
		
cloud1 = Cloud()
cloud2 = Cloud()
cloud3 = Cloud()

title = StartMenuItem("Title.png", 212)
start = StartMenuItem("start.png", 306)
stopgame = StartMenuItem("quit.png", 363)

pygame.display.set_caption('Psuedo-nomed')
while running:
	mouse_pos = pygame.mouse.get_pos()
	event = pygame.event.poll()
	if event.type == pygame.QUIT:
		running = 0
	
	if  pygame.mouse.get_pressed()[0] and start.rect.collidepoint(mouse_pos):
		start.clicked('start')
		
	elif pygame.mouse.get_pressed()[0] and stopgame.rect.collidepoint(mouse_pos):
		stopgame.clicked('quit')

	screen.fill(bgcolor)
	cloud1.move()
	cloud2.move()
	cloud3.move()
	
	title.display()
	start.display()
	stopgame.display()
	
	pygame.display.flip()
