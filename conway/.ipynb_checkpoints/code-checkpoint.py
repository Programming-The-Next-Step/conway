import pygame
import numpy as np
import math
import sys
from pygame.locals import *

pygame.init()

# Colors 
black = (0, 0, 0) # alive cells 
white = (255, 255, 255) # dead cells 
green = (0, 200, 0) # start button 
red = (200, 0, 0) # stop button
bright_green = (0, 255, 0) # to make the buttons light up when the mouse is over them
bright_red = (255, 0, 0)

# The window
window_width = 526
window_height = 600 # leave some space below to add start and stop buttons
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Game of Life")

# The cells 
cell_width = 20
cell_height = 20
margin = 1 # the margin between cell-cell and cell-window

# Matrix to store on/off values
N = 25 # found the number by trial and error 
X = np.zeros((N, N))

running = True 
while running:
    
    # always track the mouse position
    mouse = pygame.mouse.get_pos() 
    click = pygame.mouse.get_pressed()
    
    # change the screen coordinates to grid coordinates
    i = mouse[1] // (cell_height + margin) # row number
    j = mouse[0] // (cell_width + margin) # column number 
    
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: # stop the loop if the user closes the window 
            running = False

        # to change from dead to alive and alive to dead 
        elif click[0] == 1 and 0 <= i <= N: # if clicked and the mouse is on the grid
            if X[i][j] == 0:
                X[i][j] = 1
            elif X[i][j] == 1:
                X[i][j] = 0
            
    # Set the screen background
    screen.fill(black)
        
    # Draw the grid based on the matrix values
    for i in range(N):
        for j in range(N):
            color = white
            if X[i][j] == 1:
                color = black
            pygame.draw.rect(screen, color, ((cell_width + margin) * j + margin, # x-coordinates of the top-left hand corner 
                                             (cell_height + margin) * i + margin, # y-coordinates of the top-left hand corner
                                             cell_width, cell_height))
    
    # Draw the buttons, bright if the mouse is on the button 
    if 150 < mouse[0] < 150 + 100 and 538 < mouse[1] < 538 + 50:
        pygame.draw.rect(screen, bright_green, (150, 538, 100, 50))
    else: 
        pygame.draw.rect(screen, green, (150, 538, 100, 50))
        
    if 275 < mouse[0] < 275 + 100 and 538 < mouse [1] < 538 + 50:
        pygame.draw.rect(screen, bright_red, (275, 538, 100, 50))
    else:
        pygame.draw.rect(screen, red, (275, 538, 100, 50))
    
    # Adding text to the buttons 
    def text_objects(text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

    text = pygame.font.Font("freesansbold.ttf", 20)
    textSurf_1, textRect_1 = text_objects("START", text)
    textSurf_2, textRect_2 = text_objects("STOP", text)
    textRect_1.center = ((150 + (100 / 2)), (538 + (50 / 2)))
    textRect_2.center = ((275 + (100 / 2)), (538 + (50 / 2)))
    screen.blit(textSurf_1, textRect_1)
    screen.blit(textSurf_2, textRect_2)
    
    # Add functionality to the buttons and applying Conway's rules
    if 150 < mouse[0] < 150 + 100 and 538 < mouse[1] < 538 + 50:
        if click[0] == 1:
             for i in range(N):
                for j in range(N):
                    total_activation = int(
                        (X[i, (j - 1) % N] + 
                         X[i, (j + 1) % N] + 
                         X[(i - 1) % N, j] + 
                         X[(i + 1) % N, j] + 
                         X[(i - 1) % N, (j - 1) % N] + 
                         X[(i - 1) % N, (j + 1) % N] + 
                         X[(i + 1) % N, (j - 1) % N] + 
                         X[(i + 1) % N, (j + 1) % N])
                    ) 
                    if (total_activation < 2) or (total_activation > 3): 
                        X[i, j] = 0 
                    elif total_activation == 3:
                        X[i, j] = 1 
            
            #playing = True
        
    #elif 275 < mouse[0] < 275 + 100 and 538 < mouse[1] < 538 + 50:
        #if click[0] == 1:
            #playing = False 
            

    # update the screen
    pygame.display.flip()

pygame.quit()
quit()