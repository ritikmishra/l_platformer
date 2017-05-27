import pygame
import random

global_width = 1024
global_height = 576
global_screen = pygame.display.set_mode((global_width, global_height))
pygame.mixer.init()

G = 147


class ItemOnGround(pygame.sprite.Sprite):
    """We'll want a way to increase score or there's no point in telling the score"""

    def __init__(self, screen, width, height, img, posX=global_width / 2, posY=50, rock=False):
        """
        :param screen: Instance of the screen 
        :param width: Width of the scren
        :param height: Height of the screen
        :param img: Path to coin image
        :param posX: X position of coin
        :param posY: Y position of coin
        :param rock: If i am a rock instead of a coin
        """
        self.picked = False

        super(Level).__init__(Level)
        self.screen = screen
        self.img = pygame.image.load(img)
        self.change = 0
        self.size = self.img.get_size()
        self.mask = pygame.mask.from_surface(self.img)
        self.height = self.size[1]
        self.width = self.size[0]
        self.screen_width = width
        self.rock = rock
        if self.width == 23:
            self.change = 1
        elif self.width == 64:
            self.change = 2

        if not posX:
            self.posX = width / 2
        else:
            self.posX = posX

        if not posY:
            self.posY = height - 110
        else:
            self.posY = posY
        self.rect = pygame.Rect((self.posX, self.posY), self.size)

    def display(self, character_obj, level):
        """
        :param character_obj: The instance of the character so we can tell if we're picked up by it 
        :param level: The instance of the level so that we can make sure we are staying above groind
        """

        if pygame.sprite.collide_rect(self, character_obj) and (not self.picked):
            if pygame.sprite.collide_mask(self, character_obj):
                if self.rock:
                    self.picked = True
                    character_obj.rocks += 1
                else:
                    self.picked = True
                    character_obj.deaths += self.change

        if not pygame.sprite.collide_rect(self, level):
            if not pygame.sprite.collide_mask(self, level):
                self.posY += 2
        elif pygame.sprite.collide_rect(self, level):
            if pygame.sprite.collide_mask(self, level):
                self.posY -= 2

        if not self.picked:
            self.screen.blit(self.img, (self.posX, self.posY))
            self.rect = pygame.Rect((self.posX, self.posY), self.size)

    def scroll(self, direction):
        """
        :param direction: Move the coin offscreen if the player scrolled the screen
        """
        if direction == 'right':
            self.posX -= self.screen_width
            self.rect = pygame.Rect((self.posX, self.posY), self.size)
        elif direction == 'left':
            self.posX += self.screen_width
            self.rect = pygame.Rect((self.posX, self.posY), self.size)

    def shoot(self, velocity):
        while 0 < self.posX < self.width:
            if self.rock:
                self.posX += velocity
                self.screen.blit(self.img, (self.posX, self.posY))
                self.rect = pygame.Rect((self.posX, self.posY), self.size)
            else:
                break


class PowerUp(pygame.sprite.Sprite):
    """We'll want powerups, or the game will be less fun"""

    def __init__(self, screen, width, height, image, posX=False, posY=False):
        """Initializes essential variables, loads image, places image, etc..."""
        self.picked = False

        super(Level).__init__(Level)
        self.screen = screen
        self.img = pygame.image.load(image)

        self.size = self.img.get_size()
        self.mask = pygame.mask.from_surface(self.img)
        self.height = self.size[1]
        self.width = self.size[0]
        self.screen_width = width

        if not posX:
            self.posX = width / 2
        else:
            self.posX = posX

        if not posY:
            self.posY = height - 110
        else:
            self.posY = posY
        self.rect = pygame.Rect((self.posX, self.posY), self.size)

    def display(self, character_obj, level):
        """I'm sure that the coin needs to be seen and located before it is obtained"""
        if not self.picked:
            self.screen.blit(self.img, (self.posX, self.posY))
            self.rect = pygame.Rect((self.posX, self.posY), self.size)

        if pygame.sprite.collide_rect(self, character_obj) and (not self.picked):
            self.picked = True
            if character_obj.speed > 8:
                character_obj.speed -= 8
            elif character_obj.speed > 0:
                character_obj.speed -= character_obj.speed - 1
            else:
                pass
            pygame.key.set_repeat(100, character_obj.speed)

        if not pygame.sprite.collide_rect(self, level):
            if not pygame.sprite.collide_mask(self, level):
                self.posY += 2
        elif pygame.sprite.collide_rect(self, level):
            if pygame.sprite.collide_mask(self, level):
                self.posY -= 2

    def scroll(self, direction):
        """If the player has triggerred a scroll, we want the powerup to move offscreen."""
        if direction == 'right':
            self.posX -= self.screen_width
            self.rect = pygame.Rect((self.posX, self.posY), self.size)
        elif direction == 'left':
            self.posX += self.screen_width
            self.rect = pygame.Rect((self.posX, self.posY), self.size)


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
        self.posX = (-576) * 2
        self.posY = height - self.height
        self.rect = pygame.Rect((self.posX, self.posY), self.size)
        self.mask = pygame.mask.from_surface(self.image)

    def display(self):
        """Shows the ground"""
        self.screen.blit(self.image, (self.posX, self.posY))
        self.rect = pygame.Rect((self.posX, self.posY), self.size)

    def scroll(self, direction):
        """If the player is far enough to either side
           we want to move the ground so the player can see the new ground"""
        if direction == 'right':
            self.posX -= self.screen_width
        elif direction == 'left':
            self.posX += self.screen_width


class Projectile(pygame.sprite.Sprite):
    def __init__(self, screen, level_instance, screen_width, screen_height, image_path, posx, posy, speed=15):
        """
        :param screen: Instance of the screen to blit onto 
        :param level_instance: Instance of the level to detect collisions
        :param screen_width: Width of screen
        :param screen_height: Height of screen
        :param image_path: Path to image of projectile
        :param speed: How fast the projectile should go in pixels/millisecond. 
        """

        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.image.load(image_path)
        self.size = self.image.get_size()
        self.mask = pygame.mask.from_surface(self.image)
        self.height = self.size[1]
        self.width = self.size[0]
        self.posX = posx
        self.posY = posy - (self.height * 2)
        self.initial_time = pygame.time.get_ticks()
        self.crashed = False
        self.speed = speed
        self.level = level_instance

    @staticmethod
    def __get_vertical_speed(vinit, millis):
        """
        :param millis: Milliseconds since we started flying 
        :return: The vertical speed in pixels/millisecond
        """
        return vinit + (G * millis / 1000)

    def fly(self):
        dt = pygame.time.get_ticks() - self.initial_time
        dy = self.__get_vertical_speed(4, dt)
        self.posY += dy
        if self.speed > 0:
            self.posX += self.speed
        elif self.speed < 0:
            self.posX -= self.speed

        self.__blit()

    def __blit(self):
        self.rect = pygame.Rect((self.posX, self.posY), self.size)
        if not self.crashed:
            self.screen.blit(self.image, (self.posX, self.posY))
        if pygame.sprite.collide_rect(self, self.level):
            if pygame.sprite.collide_mask(self, self.level):
                self.crashed = True

    def __str__(self):
        print("PosX: " + str(self.posX))
        print("PosY: " + str(self.posY))
        print("Speed: " + str(self.speed))
        print("Size: ", self.size)
        print("Crashed: " + str(self.crashed))
        return ""


class Character(pygame.sprite.Sprite):
    def __init__(self, screen, screen_width, screen_height):
        """
        Makes a character dude
        :param screen: An instance of the screen to blit the gingerman onto
        :param screen_width: The width of the screen
        :param screen_height: The height of the screen
        """
        super(Level).__init__(Level)

        self.forward_img = pygame.image.load("resources/Ginger_forward.png")
        self.right_img = pygame.image.load("resources/Ginger_right.png")
        self.left_img = pygame.image.load("resources/Ginger_left.png")

        self.forward_size = self.forward_img.get_size()
        self.right_size = self.right_img.get_size()
        self.left_size = self.left_img.get_size()

        # self.forward_mask = pygame.mask.from_surface(self.forward_img)
        # self.right_mask = pygame.mask.from_surface(self.right_img)
        # self.left_mask = pygame.mask.from_surface(self.left_img)
        self.health = 3
        self.rocks = 10
        self.size = self.forward_size
        self.image = self.forward_img
        # self.mask = self.forward_mask

        self.screen = screen
        self.posY = screen_height / 2
        self.posX = screen_width / 2
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.error_sound = pygame.mixer.Sound("resources/error.mp3")
        self.direction = None

        self.initial_time = 0

        self.rect = pygame.Rect((self.posX, self.posY), self.size)
        self.deaths = 0
        self.speed = 50

        self.initial_time = None
        self.jumping = False
        self.landed = True
        self.dy = 0
        self.initvel = 0

        self.surrounded_by = None
        self.overlap = None
        self.vertical_overlap = None
        self.lateral_overlap = None

    @staticmethod
    def __get_vertical_speed(vinit, millis):
        """
        :param millis: Milliseconds since we started flying 
        :return: The vertical speed in pixels/millisecond
        """
        return ((G * millis) / 1000) - vinit

    def __horizontalMoveLeft(self):
        """
        Move the character left. Does not blit or update rectangle.
        """
        self.size = self.left_size
        self.image = self.left_img
        self.posX -= 4

    def __horizontalMoveRight(self):
        """
        Move the character right. Does not blit or update rectangle.
        """
        self.size = self.right_size
        self.image = self.right_img
        # self.mask = self.right_mask
        self.posX += 4

    def __vertical_movement(self, ground_rect):
        if not self.surrounded_by['bottom'] or self.initvel != 0:
            initvel = self.initvel
            if self.landed:
                self.initial_time = pygame.time.get_ticks()
                self.landed = False

            dt = pygame.time.get_ticks() - self.initial_time
            dy = self.__get_vertical_speed(initvel, dt)
            self.posY += dy

            print("dt: " + str(dt))
            print("dy: " + str(dy))
            print("Initial Velocity: " + str(initvel))
            print("Jumping: " + str(self.jumping))
            print("Landed: " + str(self.landed))
            print("\n")

            if pygame.sprite.collide_rect(self, ground_rect):
                if pygame.sprite.collide_mask(self, ground_rect):
                    # self.jumping = False
                    self.landed = True
                    self.initial_time = None

    def __display(self):
        """Blit and update the rectangle."""
        self.screen.blit(self.image, (self.posX, self.posY))
        self.rect = pygame.Rect((self.posX, self.posY), self.size)

    def move(self, ground_rect, direction='forward', coin_obj=[], powerup_obj=[], rock_obj=[]):
        """
        Move the gingerman
        :param ground_rect: The rectangle representing the ground
        :param direction: The direction to move. Can be 'left', 'right', or 'up'
        :param coin_obj: A list of coin objects. We need this list so we can shove them to the side of the screen when 
        we move too far.
        :param rock_obj: A list of rock object so that we can scroll them.
        :param powerup_obj: A list of powerup objects so that we can scroll them.
        """

        self.direction = direction
        self.surrounded_by = {'left': False, 'right': False, 'top': False, 'bottom': False, 'all': False}

        mask = pygame.mask.from_surface(self.image)
        self.overlap = ground_rect.mask.overlap_area(mask, (int(-ground_rect.posX + self.posX), int(-ground_rect.posY + self.posY)))

        total = 0

        # Overlap is shifted right by one pixel
        self.lateral_overlap = ground_rect.mask.overlap_area(mask, (int(-ground_rect.posX + self.posX + 1), int(-ground_rect.posY + self.posY)))

        # Overlap is shifted down by one pixel
        self.vertical_overlap = ground_rect.mask.overlap_area(mask, (int(-ground_rect.posX + self.posX), int(-ground_rect.posY + self.posY + 1)))

        if self.lateral_overlap < self.overlap:
            # If we move the gingerman right and there is less overlap, he is surrounded on his left
            self.surrounded_by['left'] = True

        elif self.lateral_overlap > self.overlap:
            # If we move the gingerman right and there is more overlap, he is surrounded on his right
            self.surrounded_by['right'] = True

        else:
            total += 1

        if self.vertical_overlap < self.overlap:
            # If we move the gingerman down and there is less overlap, he is surrounded on his top
            self.surrounded_by['top'] = True

        elif self.vertical_overlap > self.overlap:
            # If we move the gingerman down and there is more overlap, he is surrounded on his bottom
            self.surrounded_by['bottom'] = True

        else:
            total += 1

        if self.overlap >= 274 and total == 2:
            self.surrounded_by['all'] = True

        print("Overlap: " + str(self.overlap))  # place mask at regular origin

        if pygame.sprite.collide_mask(self, ground_rect):
            self.landed = True
            if self.landed and self.overlap >= 22:
                self.initvel = 0

        if direction == 'left':
            self.__horizontalMoveLeft()

        if direction == 'right':
            self.__horizontalMoveRight()

        if direction == 'up' and pygame.sprite.collide_mask(self, ground_rect):
            self.initvel = 25
            # move up

        # If we fell off the map
        if self.posY > self.screen_height:
            if self.posX < self.screen_width / 2:
                self.posX = self.screen_width - 102
                self.posY = self.screen_height / 2
            else:
                self.posX = 102
                self.posY = self.screen_height / 2
            self.deaths -= 1

        # Scroll everything over when appropriate
        if self.posX >= self.screen_width:
            self.posX = 3
            ground_rect.scroll('right')
            for obj in coin_obj + powerup_obj + rock_obj:
                obj.scroll('right')

        elif self.posX <= 0:
            self.posX = self.screen_width - 3
            ground_rect.scroll('left')
            for obj in coin_obj + powerup_obj + rock_obj:
                obj.scroll('left')

        if self.surrounded_by['bottom'] or self.surrounded_by['all']:
            while self.overlap is not 0:
                self.posY -= 2  # go up
                self.overlap = ground_rect.mask.overlap_area(mask, (int(-ground_rect.posX + self.posX), int(-ground_rect.posY + self.posY)))

        print(self.surrounded_by)

        self.__vertical_movement(ground_rect)

        self.__display()

    def shoot(self, ground_rect, direction):
        speed = 25
        if self.rocks > 0:
            self.rocks -= 1
            if direction == 'left':
                return Projectile(self.screen, self.screen_width, self.screen_height, 'resources/stone.png', self.posX,
                                  self.posY, -speed)
            else:
                return Projectile(self.screen, ground_rect, self.screen_width, self.screen_height,
                                  'resources/stone.png', self.posX, self.posY, speed)
        else:
            self.error_sound.play()
            return None

    def __str__(self):
        posx = "PosX: " + str(self.posX)
        posy = "PosY: " + str(self.posY)
        return posx + "\n" + posy



class Cloud:
    def __init__(self):
        """
        Create an instance of a cloud to go high in the sky
        """
        global global_height, global_width, global_screen
        self.img = pygame.image.load("resources/8bit_cloud.png")
        self.size = self.img.get_size()
        self.screen = global_screen
        self.altitude = random.randint(0, (global_height / 3) / self.size[1]) * self.size[1]
        self.position = random.randint(0, global_width)

    def move(self):
        """
        Move the cloud
        """
        global global_height, global_width, global_screen
        self.position += 0.5
        self.screen.blit(self.img, (self.position, self.altitude))

        if self.position == global_width + self.size[0]:
            self.altitude = random.randint(0, (global_height / 2) / self.size[1]) * self.size[1]
            self.position = 0 - self.size[0]


class StartMenuItem(pygame.sprite.Sprite):
    def __init__(self, img_path, posY, centered=True, posX=None):
        """
        Make a start menu item ex settings button
        :param img_path: Path to the image
        :param posY: Y position of the menu item
        :param centered: Should the menu item be centered? Defaults to True.
        :param posX: X position of the menu item if you don't want it centered. Defaults to None. 
        """
        global global_height, global_width, global_screen
        super(StartMenuItem).__init__(StartMenuItem)
        self.img = pygame.image.load(str(img_path))

        self.size = self.img.get_size()
        self.screen = global_screen
        self.altitude = int(posY)
        if centered and posX is not None:
            raise ValueError("Start menu item is supposed to be centered and the posX parameter is given!")
        elif centered:
            self.posX = (global_width / 2) - (self.size[0] / 2)
        else:
            self.posX = posX

        self.rect = pygame.Rect((self.posX, self.altitude), self.size)

    def display(self):
        """Display the button"""
        self.screen.blit(self.img, (self.posX, self.altitude))

    def clicked(self):
        """
        :return If I am being clicked
        """
        return pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos())
