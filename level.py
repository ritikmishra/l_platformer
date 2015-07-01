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
    class Level(pygame.sprite.Sprite):
        def __init__(self, screen, width, height, img):
            super(Level).__init__(Level)
            self.screen = screen
            self.img = pygame.image.load(img)
            self.size = self.img.get_size()
            self.height = self.size[1]
            self.width = self.size[0]
            self.screen_width = width
            self.posX=0
            self.posY=height - self.height
            self.rect = pygame.Rect((self.posX, self.posY), self.size)
            print self.rect
        def display(self):
            self.screen.blit(self.img, (self.posX, self.posY))
            self.rect = pygame.Rect((self.posX, self.posY), self.size)
        def scroll(self, distance):
			if distance > 0:
				self.posX= 0-self.screen_width + distance
			elif distance <0:
				self.posX= self.screen_width + distance
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
            
            self.size = self.forward_size
            self.img = self.forward_img
            
            self.screen = screen
            self.posY = height/2
            self.posX = width/2
            self.screen_width = width
            
            self.rect = pygame.Rect((self.posX, self.posY), self.size)
   
        
        def move(self, ground_rect, direction='forward'):
            
            if not pygame.sprite.collide_rect(self, ground_rect):
                self.posY +=1
                self.size = self.forward_size
                self.img = self.forward_img
                self.screen.blit(self.img, (self.posX, self.posY))
                self.rect = pygame.Rect((self.posX, self.posY), self.size)
        
            elif direction == 'left':
                self.size = self.left_size
                self.img = self.left_img
                self.posX -= 10
                self.screen.blit(self.img, (self.posX, self.posY))
                self.rect = pygame.Rect((self.posX, self.posY), self.size)
            elif direction == 'right':
               self.size = self.right_size
               self.img = self.right_img
               self.posX += 10
               self.screen.blit(self.img, (self.posX, self.posY))
               self.rect = pygame.Rect((self.posX, self.posY), self.size)
            else:
                self.screen.blit(self.img, (self.posX, self.posY))
            
            if self.posX >= self.screen_width - 100:
                self.posX = 101
                ground_rect.scroll(101)
                self.screen.blit(self.img, (self.posX, self.posY))
                self.rect = pygame.Rect((self.posX, self.posY), self.size)
            elif self.posX <= 100:
                self.posX = self.screen_width -101
                ground_rect.scroll(-101)
                self.screen.blit(self.img, (self.posX, self.posY))
                self.rect = pygame.Rect((self.posX, self.posY), self.size)



    #The user's helicopter
    level = Level(window, width, height, "Level 1.png")
    gingerman = Character(window, width, height)

        
        
    score = 0
    #gameloop
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
        #makes the background blue 
        window.fill((135, 206, 235))
        level.display()
        window.blit(level.img, (level.posX, level.posY))
        gingerman.move(level)
        print pygame.sprite.collide_rect(gingerman, level)
        
      
        pygame.display.flip()

if __name__ == '__main__':
    main(1204, 576)
