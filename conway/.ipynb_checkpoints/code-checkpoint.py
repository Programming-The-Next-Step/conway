import pygame
import numpy as np
import math
import sys
from pygame.locals import *

####### The constants #######

# Colors 
grey = (210, 210, 210) # the grid lines 
black = (0, 0, 0) # alive cells 
white = (255, 255, 255) # dead cells 
green = (0, 200, 0) # start button 
red = (200, 0, 0) # pause button
blue = (30, 144, 255) # reset button
bright_green = (0, 255, 0) # to make the buttons light up when the mouse is over them
bright_red = (255, 0, 0)
bright_blue = (0, 191, 255)

# The window
window_width = 526
window_height = 600 # leave some space below to add start and stop buttons

# The cells 
cell_width = 20
cell_height = 20
margin = 1 # the margin between cell-cell and cell-window

class Life: 
    def __init__(self):
        self.running = True
        self.iterate = False
        pygame.init()
        screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Game of Life")
        clock = pygame.time.Clock()
        
        # Matrix to store on/off values
        self.N = 25 # found the number by trial and error 
        self.grid = np.zeros((self.N, self.N))    
        
        while self.running == True:
            clock.tick(60)
            self.update()
            self.draw(screen)
            # always track the mouse position
            mouse = pygame.mouse.get_pos() 
            click = pygame.mouse.get_pressed()

            # change the screen coordinates to grid coordinates
            i = mouse[1] // (cell_height + margin) # row number
            j = mouse[0] // (cell_width + margin) # column number

            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: # stop the loop if the user closes the window 
                    running = False
                    pygame.quit()
                    quit()

                # change between dead-alive by clicking on the cells 
                elif click[0] == 1:
                    
                    if 0 <= i <= (self.N - 1): 
                        if self.grid[i][j] == 0:
                            self.grid[i][j] = 1
                        elif self.grid[i][j] == 1:
                            self.grid[i][j] = 0

                    elif 50 < mouse[0] < 50 + 100 and 538 < mouse[1] < 538 + 50:
                        self.iterate = True 
                        
                    elif 215 < mouse[0] < 215 + 100 and 538 < mouse[1] < 538 + 50:
                        self.iterate = False

                    # if the reset button is pressed, empty the grid 
                    elif 376 < mouse[0] < 376 + 100 and 538 < mouse[1] < 538 + 50:
                        self.iterate = False 
                        for i in range(self.N):
                            for j in range(self.N):
                                self.grid[i, j] = 0

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
            # update the screen
            pygame.display.update()
            

    def game(self):
        """ Applies Conway's rules to the initial pattern and 
        returns the updated grid. 
        """
        X = self.grid.copy()
        for i in range(self.N):
            for j in range(self.N):
                    # calculating the activation of a cell's 8 neighbors
                    total_activation = int(
                        (X[i, (j - 1) % self.N] + 
                         X[i, (j + 1) % self.N] + 
                         X[(i - 1) % self.N, j] + 
                         X[(i + 1) % self.N, j] +
                         X[(i - 1) % self.N, (j - 1) % self.N] + 
                         X[(i - 1) % self.N, (j + 1) % self.N] + 
                         X[(i + 1) % self.N, (j - 1) % self.N] + 
                         X[(i + 1) % self.N, (j + 1) % self.N])
                    )
                    # implementing Conway's 4 rules
                    if X[i, j] == 0:
                        if total_activation == 3: # birth 
                            self.grid[i, j] = 1
                        else: 
                            self.grid[i, j] = 0 # loneliness 

                    elif X[i, j] == 1:
                        if (total_activation < 2) or (total_activation > 3): # loneliness & overcrowding 
                            self.grid[i, j] = 0
                        else:
                            self.grid[i, j] = 1 # survival
    
    def update(self):
        if self.iterate:
            self.game()

    def draw(self, screen):
        """ Draws the grid based on the matrix values. """
        screen.fill(grey)
        for i in range(self.N):
            for j in range(self.N):
                if self.grid[i, j] == 0:
                    color = white
                elif self.grid[i][j] == 1:
                    color = black
                pygame.draw.rect(screen, color, ((cell_width + margin) * j + margin, # x-coordinates of the top-left hand corner 
                                                 (cell_height + margin) * i + margin, # y-coordinates of the top-left hand corner
                                                 cell_width, cell_height))    
    
    def text_objects(text, font):
        """ Creates the text objects to be put on the buttons. """
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()
                
if __name__ == "__main__":
    Life()