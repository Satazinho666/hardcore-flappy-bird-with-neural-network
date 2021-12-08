import pygame
from pygame.locals import *
import sys
import numpy as np
import random as rd
from objects import Bird, Pipe, Ground
from IntuitionAI import AI

def start(Birds_list, still_playing=0, Mutation=False):
    # Start N_AI_PLAYERS birds controlled by AIs
    if Mutation == False:
        for i in range(still_playing, N_AI_PLAYERS):
            Birds_list+=[(Bird(),AI())]
    else:
        for i in range(still_playing,N_AI_PLAYERS):
            new_b = Birds_list[i%still_playing][1]
            new_b.mutation()
            Birds_list+[Bird(),new_b]

##--------------- CONSTANTS AND CREATION OF CLOCK STUFF ---------------------
N_AI_PLAYERS = 100
SPEED = 2 #set the speed in which pipes and the ground move
PIPE_GAP = 35 #Space between upper and bottom pipes
PIPE_H_SIZE = 52 #horizontal size of a pipe
DIST_BETWEEN_PIPES = 240 #distance between consecutive pairs of pipes
GRAVITY = 0.5 #gravity's acceleration
FPS = 80 #game fps (for controling frames flow)
GENERATIONS = 5
#----------------------------------------------------------------------------

should_mutate = False

def one_play(Lst_of_birds = []):
    global should_mutate

    ##----------- INITIALIZE SOME IMPORTANT STUFF OUTSIDE GAME LOOP ---------
    
    tck = pygame.time.Clock() # Initialize the clock as "tck"
    white = (255,255,255)
    black = (0,0,0)
    time_var = 0

    # Creates a background:
    BACKGROUND = pygame.image.load("Assets/background-day.png")

    #initialize pygame:
    pygame.init()

    #sets "display" as the display surface for the game:
    display = pygame.display.set_mode((288,512))

    # Names the window of the game:
    pygame.display.set_caption("Flappy Bird")

    # Creates the grounds, from class in "objects.py":
    ground1 = Ground(0)
    ground2 = Ground(336)
    grounds=[ground1,ground2]

    # Initialize the bird list
    Birds_list = Lst_of_birds
    pipes=[]

    start(Birds_list, should_mutate)
    should_mutate = True

    # Points and text:
    Points = 0
    font = pygame.font.Font("freesansbold.ttf",15)
    text = font.render(f"{Points}",True, white)
    #-------------------------------------------------------------------------

    ##-------------------------- GAME LOOP -----------------------------------
    while True:
        
        # Allows you to quit the game: 
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

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
        if  pygame.time.get_ticks()-time_var >500 and pipes == []:
            #waits 500ms to spawn first pipe
            pipes.append(Pipe())
        elif pygame.time.get_ticks()-time_var > 500 and pipes != []:
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
        
        if pipes!=[]:
            if pipes[0].x==20+PIPE_GAP:
                Points+=1
        

        # Draw the grounds
        for ground in grounds:
            display.blit(ground.image,(ground.x,ground.y))
       
        #Draws the bird(s) and control its movements:
        for bird in Birds_list:
            bird[0].y += bird[0].speed
            bird[0].draw(display)
            bird[0].speed += GRAVITY 
            if (time//120)%3 == 0:
                bird[0].an_state = 0
            elif (time//120)%3 == 1:
                bird[0].an_state = 1
            else:
                bird[0].an_state = 2

            #Collision detection:
            for pipe in pipes:
                offset1 = (int(bird[0].x-pipe.x),int(bird[0].y - pipe.y[0]))
                offset2 = (int(bird[0].x-pipe.x),int(bird[0].y - pipe.y[1]))
                if pipe.masks[0].overlap(bird[0].masks[bird[0].an_state],offset1)!=None:
                    Birds_list.remove(bird)
                elif pipe.masks[1].overlap(bird[0].masks[bird[0].an_state],offset2)!=None:
                    Birds_list.remove(bird)

        for bird in Birds_list:
            if bird[0].y < 0:  # bird above ceiling
                Birds_list.remove(bird)
                continue
            for ground in grounds:  # bird collide floor
                off = (int(bird[0].x - ground.x), int(bird[0].y-ground.y))
                if ground.mask.overlap(bird[0].masks[bird[0].an_state],off) != None:
                    Birds_list.remove(bird)

        for bird in Birds_list:
            # AI plays here:
            if pipes != []:
                if pipes[0].x>20+PIPE_H_SIZE:
                    if bird[1].Output(bird[0].x-pipes[0].x, bird[0].y-pipes[0].y[0])==True:
                        bird[0].flap()
                else:
                    if bird[1].Output(bird[0].x-pipes[1].x,bird[0].y-pipes[0].y[0])==True:
                        bird[0].flap()

        text = font.render(f'Points: {Points}', True,  white)
        display.blit(text,(200,30))
        display.blit(font.render(f"Birds alive",True,black),(200,50))
        display.blit(font.render(f"{len(Birds_list)}", True, black), (230,70))
         
        if len(Birds_list) < 5:
            return Birds_list

        # Updates the screen and makes the game move on
        pygame.display.update()
        tck.tick(FPS)

def main(gen):
    current_birds = []

    for i in range(gen):
        current_birds = one_play(current_birds)    

main(GENERATIONS)
