import pygame
import numpy as np
import math
import sys
from pygame.locals import *

pygame.init()

# Colors 
grey = (210, 210, 210) # the grid lines 
black = (0, 0, 0) # alive cells 
white = (255, 255, 255) # dead cells 
green = (0, 200, 0) # start button 
red = (200, 0, 0) # stop button
blue = (30, 144, 255)
bright_green = (0, 255, 0) # to make the buttons light up when the mouse is over them
bright_red = (255, 0, 0)
bright_blue = (0, 191, 255)

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
        elif click[0] == 1 and 0 <= i <= (N - 1): # if clicked and the mouse is on the grid
            if X[i][j] == 0:
                X[i][j] = 1
            elif X[i][j] == 1:
                X[i][j] = 0
            
    # Set the screen background
    screen.fill(grey)
        
    # Draw the grid based on the matrix values
    for i in range(N):
        for j in range(N):
            if X[i, j] == 0:
                color = white
            elif X[i][j] == 1:
                color = black
            pygame.draw.rect(screen, color, ((cell_width + margin) * j + margin, # x-coordinates of the top-left hand corner 
                                             (cell_height + margin) * i + margin, # y-coordinates of the top-left hand corner
                                             cell_width, cell_height))
    
    # Draw the buttons, bright if the mouse is on the button 
    if 50 < mouse[0] < 50 + 100 and 538 < mouse[1] < 538 + 50:
        pygame.draw.rect(screen, bright_green, (50, 538, 100, 50))
    else: 
        pygame.draw.rect(screen, green, (50, 538, 100, 50))
     
    if 215 < mouse[0] < 215 + 100 and 538 < mouse [1] < 538 + 50:
        pygame.draw.rect(screen, bright_red, (215, 538, 100, 50))
    else:
        pygame.draw.rect(screen, red, (215, 538, 100, 50))
        
    if 376 < mouse[0] < 376 + 100 and 538 < mouse [1] < 538 + 50:
        pygame.draw.rect(screen, bright_blue, (376, 538, 100, 50))
    else:
        pygame.draw.rect(screen, blue, (376, 538, 100, 50))
    
    
    # Adding text to the buttons 
    def text_objects(text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

    text = pygame.font.Font("freesansbold.ttf", 20)
    textSurf_1, textRect_1 = text_objects("START", text)
    textSurf_2, textRect_2 = text_objects("PAUSE", text)
    textSurf_3, textRect_3 = text_objects("RESET", text)
    textRect_1.center = ((50 + (100 / 2)), (538 + (50 / 2)))
    textRect_2.center = ((215 + (100 / 2)), (538 + (50 / 2)))
    textRect_3.center = ((376 + (100 / 2)), (538 + (50 / 2)))
    screen.blit(textSurf_1, textRect_1)
    screen.blit(textSurf_2, textRect_2)
    screen.blit(textSurf_3, textRect_3)
    
    # Adding functionality to the buttons
    if 50 < mouse[0] < 50 + 100 and 538 < mouse[1] < 538 + 50 and click[0] == 1:
        for i in range(N):
            for j in range(N):
                # calculating the activation of a cell's 8 neighbors
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
                # applying Conway's 4 rules
                if X[i, j] == 0:
                    if total_activation == 3: # birth 
                        X[i, j] = 1
                    else: 
                        X[i, j] = 0 # loneliness 
                    
                elif X[i, j] == 1:
                    if (total_activation < 2) or (total_activation > 3): # loneliness & overcrowding 
                        X[i, j] = 0
                    else:
                        X[i, j] = 1 # survival 
                        
    elif 376 < mouse[0] < 376 + 100 and 538 < mouse[1] < 538 + 50 and click[0] == 1:
        for i in range(N):
            for j in range(N):
                X[i, j] = 0
    
    # update the screen
    pygame.display.update()

pygame.quit()
quit()