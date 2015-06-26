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
    class Helicopter:
        """Contains all the functions and variables that only the helicopter needs"""
        def __init__(self, screen):
            """Creates all the essential variables"""
            self.change = 1
            self.y = 50
            self.x = 25
            self.img = pygame.image.load("Ginger_forward.png")
            self.size = self.img.get_size()
            self.click = 0
            self.screen = screen
            
        def move(self):
            """Moves the helicopter if computer detects left-click"""
            
            self.click = pygame.mouse.get_pressed()[0]
            if self.click == 1:
                self.change = -1
            else:
                self.change = 1
            self.y += self.change
        def blit(self):
            """Displays the helicopter"""
            self.corners = [(self.x, self.y), (self.x, self.y + self.size[1]), (self.x + self.size[0], self.y), (self.x + self.size[0], self.y + self.size[1])] 
            self.screen.blit(self.img, (self.x, self.y))
        

    class Obstacle:
        """Contains all the functions and variables specific to the boxes"""
        def __init__(self, screen):
            self.change = 4
            self.y = random.randrange(0, 560)
            self.x = 999
            self.img = pygame.image.load("Ginger_left.png")
            self.size = self.img.get_size()
            self.screen = screen
            self.perim = []
        def move(self):
            """Moves the murderous obstacle towards its destination's x point"""
            self.x -= self.change
            if self.x <= 1:
                self.x = 999
                self.y = random.randrange(0, 560)
        def blit(self):
            """Makes the user able to see and thus evade the obstacle"""
            #The next two lines are for collision detection
            self.corners = [(self.x, self.y), (self.x, self.y + self.size[1]), (self.x + self.size[0], self.y + self.size[1]), (self.x + self.size[0], self.y)] 
            
            self.screen.blit(self.img, (self.x, self.y))
           
        

    #The user's helicopter
    heli = Helicopter(window)
    obs=[Obstacle(window), Obstacle(window), Obstacle(window)]
    

        
        
    score = 0
    #gameloop
    while running:
         #makes the close button functional
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = 0
        
        #makes the background black 
        window.fill((0, 0, 0))
        
        
        #moves the helicopter
        heli.move()
        obs[0].move()
        obs[1].move()
        obs[2].move()
        
       
        
        #shows the helicopter
        heli.blit()
        obs[0].blit()
        obs[1].blit()
        obs[2].blit()

        if heli.y <= 1 or heli.y >= 500:
            break
        
        for corner in heli.corners:
            if corner[1] in range(obs[0].y, obs[0].y + 40) and corner[0] in range(obs[0].x, obs[0].x + 64):
                exit()
            
            elif corner[1] in range(obs[1].y, obs[1].y + 40) and corner[0] in range(obs[1].x, obs[1].x + 64):
                exit()
            
            elif corner[1] in range(obs[2].y, obs[2].y + 40) and corner[0] in range(obs[2].x, obs[2].x + 64):
                exit()  
        pygame.display.flip()
    print("You lose!")
if __name__ == '__main__':
    print "This file is meant to be a part of Psuedo-Nomed"
