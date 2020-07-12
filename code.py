import pygame
import numpy as np
import math
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
window_width = 400
window_height = 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Game of Life")

# The cells 
cell_width = 20
cell_height = 20
margin = 1

# Matrix to store on/off values (can't generalize to non-square lattices)
total_pixels = window_width * window_height 
cell_pixels = cell_width * cell_height 
n_cells = total_pixels / cell_pixels
nrow = int(math.sqrt(n_cells))
ncol = nrow 
X = np.zeros((nrow, ncol))

running = True 
while running:
    mouse = pygame.mouse.get_pos() # always track the mouse position
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: # stop the loop if the user closes the window 
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN: # if the user clicks
            #change the x/y screen coordinates to grid coordinates
            i = mouse[0] // (cell_width + margin) # row number 
            j = mouse[1] // (cell_height + margin) # column number 
            # set the clicked cell to 1
            X[i][j] = 1
            
    # Set the screen background
    screen.fill(black)
        
    # Draw the grid based on the matrix values
    for i in range(nrow):
        for j in range(ncol):
            color = white
            if X[i][j] == 1:
                color = black
            pygame.draw.rect(screen, color, ((cell_width + margin) * i + margin, # x-coordinates of the top-left hand corner 
                                             (cell_height + margin) * j + margin, # y-coordinates of the top-left hand corner
                                             cell_width, cell_height))
    
    # Draw the buttons, bright if the mouse is on the button 
    if 70 < mouse[0] < 70 + 100 and 525 < mouse[1] < 525 + 50:
        pygame.draw.rect(screen, bright_green, (70, 525, 100, 50))
    else: 
        pygame.draw.rect(screen, green, (70, 525, 100, 50))
        
    if 230 < mouse[0] < 230 + 100 and 525 < mouse [1] < 525 + 50:
        pygame.draw.rect(screen, bright_red, (230, 525, 100, 50))
    else:
        pygame.draw.rect(screen, red, (230, 525, 100, 50))
        
    def text_objects(text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects("START", smallText)
    textRect.center = ((70 + (100 / 2)), (525 + (50 / 2)))
    screen.blit(textSurf, textRect)
 
    # update the screen
    pygame.display.flip()

pygame.quit()
quit()