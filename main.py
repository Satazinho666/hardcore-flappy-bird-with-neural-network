import pygame
from pygame.locals import *
import sys
import numpy as np
import random as rd
from objects import Bird, Pipe, Ground

##--------------- CONSTANTS AND CREATION OF CLOCK STUFF ---------------------

SPEED = 2 #set the speed in which pipes and the ground move
PIPE_GAP = 10 #Space between upper and bottom pipes
PIPE_H_SIZE = 52 #horizontal size of a pipe
DIST_BETWEEN_PIPES = 140 #distance between consecutive pairs of pipes
GRAVITY = 0.5 #gravity's acceleration
FPS = 40 #game fps (for controling frames flow)
tck = pygame.time.Clock() # Initialize the clock as "tck"
#----------------------------------------------------------------------------

##----------- INITIALIZE SOME IMPORTANT STUFF OUTSIDE GAME LOOP -------------
# Creates a background:
BACKGROUND = pygame.image.load("Assets/background-day.png")

# Creates the grounds, from class in "objects.py":
ground1 = Ground(0)
ground2 = Ground(336)
grounds=[ground1,ground2]

#list of pipes to control their spawn:
pipes=[]

#initialize pygame:
pygame.init()

#sets "display" as the display surface for the game:
display = pygame.display.set_mode((288,512))

# Names the window of the game:
pygame.display.set_caption("Flappy Bird")

Birds_list=[Bird()] #only one right now, more to be implemented soon!

#----------------------------------------------------------------------------

##-------------------------- GAME LOOP --------------------------------------
while True:
    
    # Allows you to quit the game: 
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type ==pygame.KEYDOWN:
            for bird in Birds_list:  
                bird.flap()

    # Draws background in display (screen):
    display.blit(BACKGROUND,BACKGROUND.get_rect())

    # Move both grounds:
    ground1.x -= SPEED
    ground2.x -= SPEED
    for ground in grounds:
        if ground.x<-336:
            ground.x = 236

    time = pygame.time.get_ticks()

    # Creates and move the Pipes:
    if  time >500 and pipes == []:
        #waits 500ms to spawn first pipe
        pipes.append(Pipe())
    elif time > 500 and pipes != []:
        #if there is some pipe already, uses the following rule:
        for pipe in pipes:
            if pipe.x <-PIPE_H_SIZE:
                pipes.remove(pipe)
            if 400-pipes[-1].x > DIST_BETWEEN_PIPES:
                pipes.append(Pipe())
    for pipe in pipes:
        display.blit(pipe.images[0],(pipe.x,pipe.y[0]))
        display.blit(pipe.images[1],(pipe.x,pipe.y[1]))
        pipe.x -= SPEED
    
    # Draw the grounds
    for ground in grounds:
        display.blit(ground.image,(ground.x,ground.y))
   
    #Draws the bird(s) and control its movements:
    for bird in Birds_list:
        bird.y += bird.speed
        bird.draw(display)
        bird.speed += GRAVITY 
        if (time//120)%3 == 0:
            bird.an_state = 0
        elif (time//120)%3 == 1:
            bird.an_state = 1
        else:
            bird.an_state = 2

        #Collision detection:
        for pipe in pipes:
            offset1 = (int(bird.x-pipe.x),int(bird.y - pipe.y[0]))
            offset2 = (int(bird.x-pipe.x),int(bird.y - pipe.y[1]))
            if pipe.masks[0].overlap(bird.masks[bird.an_state],offset1)!=None:
                Birds_list.remove(bird)
            elif pipe.masks[1].overlap(bird.masks[bird.an_state],offset2)!=None:
                Birds_list.remove(bird)

    # Updates the screen and makes the game move on
    pygame.display.update()
    tck.tick(FPS)
