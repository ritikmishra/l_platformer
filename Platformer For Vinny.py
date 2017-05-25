import pygame
import sys
import level
from classes import Cloud 
from classes import StartMenuItem

width = 1024
height = 576
screen = pygame.display.set_mode((width, height))
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
    mouse_pos = pygame.mouse.get_pos()
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0
    
    if pygame.mouse.get_pressed()[0] and start.rect.collidepoint(mouse_pos):
        stopgame.clicked(level.main, width, height)
        
    elif pygame.mouse.get_pressed()[0] and stopgame.rect.collidepoint(mouse_pos):
        start.clicked(sys.exit)


    screen.fill(bgcolor)
    cloud1.move()
    cloud2.move()
    cloud3.move()
    
    title.display()
    start.display()
    stopgame.display()
    
    pygame.display.flip()
