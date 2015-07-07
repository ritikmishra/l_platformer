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
	from classes import Coin
	
	#Death counter
	deaths = 0
	
	pygame.init()
	font = pygame.font.SysFont("OSP-DIN", 48)
	 
	text = font.render("Score: Nil" , True ,(255,255,255))
	
	
	#create the screen
	dimensions = (width, height)
	screen = pygame.display.set_mode(dimensions)
	
	#helps with making the close button in the corner work
	running = 1
	
	#The ground
	level = Level(screen, width, height, "resources/Level 1.png")
	
	
	#The character, who's sprite is a gingerbread man
	gingerman = Character(screen, width, height)
	
	#The powerup
	speedup = PowerUp(screen, width, height, 'resources/arrow.png', 'Launcher', False, 125)
	
	#If the arrow keys are held down, we want the character to continously move. This helps with that.	
	pygame.key.set_repeat(100, 50)
	
	
	#The clouds. We put them into a list so we can iterate through them
	clouds = [Cloud(), Cloud(), Cloud()]
	coins = [Coin(screen, width, height, )]
	
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
		screen.fill((135, 206, 235))
		
		#Shows the level
		level.display()
		
		for coin in coins:
			coin.display(gingerman)

		deathtext = font.render("Score:"+ str(gingerman.deaths), 1,(255,255,255))
		
		
				
		#speedup.display() #|This is commented because the speedup is glitchy
		
		#speedup.speedup(gingerman) # |This is commented because the speedup is glitchy
		
		#Makes sure physics applies
		gingerman.move(level)
		
		#Shows and moves the cloud
		for cloud in clouds:
			cloud.move()
		
		
		screen.blit(deathtext, (0,0))


		
		#Shows everything
		pygame.display.flip()

if __name__ == '__main__':
	main(1024, 576)
