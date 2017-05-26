import pygame
import sys
import level
from classes import Cloud 
from classes import StartMenuItem

global_width = 1024
global_height = 576
global_screen = pygame.display.set_mode((global_width, global_height))
bgcolor = 135, 206, 235
running = 1

cloud1 = Cloud()
cloud2 = Cloud()
cloud3 = Cloud()

title = StartMenuItem("resources/Title.png", 212)
start = StartMenuItem("resources/start.png", 306)
stopgame = StartMenuItem("resources/quit.png", 363)

pygame.display.set_caption('Psuedo-nomed')
while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0
    
    if stopgame.clicked():
        sys.exit()

    elif start.clicked():
        level.main(global_width, global_height)

    global_screen.fill(bgcolor)
    cloud1.move()
    cloud2.move()
    cloud3.move()
    
    title.display()
    start.display()
    stopgame.display()
    
    pygame.display.flip()
