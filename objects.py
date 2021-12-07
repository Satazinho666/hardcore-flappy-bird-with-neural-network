import pygame
import sys
import numpy as np
import random as rd

FLAP_FORCE = 6 #How strong are the wings
GROUND_HEIGHT = 100
PIPE_GAP = 75 #Space between upper and bottom pipes

class Bird:

    def __init__(self):
        self.y = 100 #position in y-axis
        self.x = 20 #position in x-axis
        self.speed = 2 #vertical speed of the bird
        self.an_state = 0
        self.spt = pygame.sprite.Sprite()
        random = rd.randrange(0,3)
        if random ==0:
            self.an_images = [
                    pygame.image.load("Assets/bluebird-downflap.png"),
                    pygame.image.load("Assets/bluebird-midflap.png"), 
                    pygame.image.load("Assets/bluebird-upflap.png")
                    ]

        elif  random == 1:
            self.an_images = [
                    pygame.image.load("Assets/redbird-downflap.png"),
                    pygame.image.load("Assets/redbird-midflap.png"), 
                    pygame.image.load("Assets/redbird-upflap.png")
                    ]
        
        elif random == 2:
            self.an_images = [
                    pygame.image.load("Assets/yellowbird-downflap.png"),
                    pygame.image.load("Assets/yellowbird-midflap.png"), 
                    pygame.image.load("Assets/yellowbird-upflap.png")
                    ]

        self.masks = [pygame.mask.from_surface(self.an_images[i]) for i in range(3)]

    def flap(self):
        ''' 
            When this function is called, the speed will be set to FLAP_FORCE
        '''
        self.speed = -FLAP_FORCE

    def draw(self,surface):
        '''
            Draw the bird in the surface (mostly a display)
        '''
        surface.blit(self.an_images[self.an_state],(self.x,self.y))

class Pipe:
    def __init__(self):
        self.x = 400 #position in x-axis. Starts outside the screen
        center_y = rd.randrange(50,360) #position in y-axis
        self.y = (center_y+PIPE_GAP/2, center_y-PIPE_GAP/2-320) # pair of heights for the pair of pipes
        random = rd.randrange(0,2) #randomizer for the color
        if random == 0:
            self.images = (pygame.image.load("Assets/pipe-red.png"),
            pygame.transform.flip(pygame.image.load("Assets/pipe-red.png"),False,True))
        elif random ==1:
            self.images = (pygame.image.load("Assets/pipe-green.png"),
            pygame.transform.flip(pygame.image.load("Assets/pipe-green.png"),False, True))
    # notice the .flip function above, which makes sure we have one of the pipes of each pair fliped

        self.masks = [ pygame.mask.from_surface(self.images[i]) for i in range(2)]


class Ground:
    def __init__(self,x_pos):
        self.y = 512-GROUND_HEIGHT
        self.x = x_pos
        self.image = pygame.image.load("Assets/base.png")
        self.mask = pygame.mask.from_surface(self.image)
