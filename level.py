def main(width, height):
	#import modules
	import pygame
	import os
	import random
	import time
	
	from classes import PowerUp
	from classes import Level
	from classes import Character
	from classes import Cloud
	from classes import Obtainium
	
	#Death counter
	deaths = 0
	clock = pygame.time.Clock()
	pygame.init()
	font = pygame.font.SysFont("OSP-DIN", 48)
	 
	
	
	#create the screen
	dimensions = (width, height)
	screen = pygame.display.set_mode(dimensions)
	
	#helps with making the close button in the corner work
	running = 1
	
	#The ground
	level = Level(screen, width, height, "resources/Level 1.png")
	
	
	#The character, who's sprite is a gingerbread man
	gingerman = Character(screen, width, height)
	
	
	
	coin_imgs = ["resources/Coin2.png", "resources/Coin.png"]
	#The clouds. We put them into a list so we can iterate through them
	clouds = [Cloud(), Cloud(), Cloud()]
	coins = []
	powerups = []
	rocks = Obtainium(screen, width, height, 'resources/stone.png', width/2, 50, True)
	for x in range(7):
		coins.append(Obtainium(screen, width, height, random.choice(coin_imgs), (random.randint(-400, 4000)) - (10*x) + width, height-150))
		powerups.append(PowerUp(screen, width, height, 'resources/arrow.png', (random.randint(-400, 4000)) - (10*x) + width, height-150))
		
	#If the arrow keys are held down, we want the character to continously move. This helps with that.	
	pygame.key.set_repeat(100, gingerman.speed)



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
					gingerman.move(level, 'left', coins, powerups)
				if event.key == pygame.K_RIGHT:
					gingerman.move(level, 'right', coins, powerups)
				if event.key == pygame.K_SPACE:
					gingerman.move(level, 'up', coins, powerups)
			
	
		
	
		#makes the background blue 
		screen.fill((135, 206, 235))
		
		#Shows the level
		level.display()
		
		for coin in coins:
			coin.display(gingerman)
		for thing in powerups:
			thing.display(gingerman)


		deathtext = font.render("Score:"+ str(gingerman.deaths), 1,(255,255,255))
		rocktext = font.render("Rocks:"+ str(gingerman.rocks), 1,(255,255,255))
		rocks.display(gingerman)
		
				
		#Makes sure physics applies
		gingerman.move(level, 'forward', coins)
		#Shows and moves the cloud
		for cloud in clouds:
			cloud.move()
		
		
		screen.blit(deathtext, (0,0))
		screen.blit(rocktext, (0,48))


		
		#Shows everything
		pygame.display.flip()
		
		clock.tick(120)
		


if __name__ == '__main__':
	main(1024, 576)
