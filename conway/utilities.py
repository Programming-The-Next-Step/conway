import pygame
import numpy as np
import random as r 

# Colors used to draw the buttons 
grey = (210, 210, 210) # the grid lines 
black = (0, 0, 0) # alive cells 
white = (255, 255, 255) # dead cells 
green = (0, 200, 0) # start button 
red = (200, 0, 0) # pause button
blue = (30, 144, 255) # reset button
bright_green = (0, 255, 0) # to make the buttons light up 
bright_red = (255, 0, 0)
bright_blue = (0, 191, 255)

# The game window
window_width = 716
window_height = 785 

# A matrix to store on/off values 
N = 65
grid = np.zeros((N, N)) 

# The cell dimensions  
cell_width = 10
cell_height = 10
margin = 1 # the margin between the cells

class Life: 
    def __init__(self):
        """ Creating two attributes both of which are logical. 
        These determine whether the main game loop is running
        and whether the rules are being iterated. They are both 
        initiated as False and are changed when a specific method
        is called or when the user clicks on a specific button. 
        For example, if the main game function 'play' is called, 
        running will be True and the event loop will begin. Iterate 
        is True if the user clicks on the START button to start applying
        Conway's rules. False if the game is paused or the grid is reset. 
        """
        self.running = False 
        self.iterate = False
                
    def play(self):
        """ The main function. Initiates the game by creating the 
        screen based on the predetermined, constant window size. 
        Draws the button and runs the event loop while responding to
        which button is pressed. 
        """
        pygame.init() 
        self.running = True # runs the while loop 
        screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Game of Life")
        self.initial() # sets the initial pattern when the window opens
        while self.running == True:
            self.update()
            self.draw(screen)
            # always track the mouse position
            mouse = pygame.mouse.get_pos() 
            click = pygame.mouse.get_pressed()
            # change the screen coordinates to grid coordinates
            global i # if these are not declared globally 
            global j # the state function does not work 
            i = mouse[1] // (cell_height + margin) # row number
            j = mouse[0] // (cell_width + margin) # column number            
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: # stop the loop if the user closes the window 
                    running = False
                    pygame.quit()
                    quit()
                elif click[0] == 1: # if the mouse is clicked 
                    # change the cell state if the mouse is on the grid   
                    if 0 <= i <= (N - 1): 
                        self.state()
                    # start iterating if the start button is pressed 
                    elif 140 < mouse[0] < 140 + 100 and 725 < mouse[1] < 725 + 50:
                        self.iterate = True 
                    # stop iterating if the pause button is pressed 
                    elif 305 < mouse[0] < 305 + 100 and 725 < mouse[1] < 725 + 50:
                        self.iterate = False
                    # stop and reset if the reset button is pressed 
                    elif 466 < mouse[0] < 466 + 100 and 725 < mouse[1] < 725 + 50:
                        self.iterate = False
                        self.reset()
                    
           # Draw the buttons, bright if the mouse is on the button 
            if 140 < mouse[0] < 140 + 100 and 600 < mouse[1] < 725 + 50:
                pygame.draw.rect(screen, bright_green, (140, 725, 100, 50))
            else: 
                pygame.draw.rect(screen, green, (140, 725, 100, 50))

            if 305 < mouse[0] < 305 + 100 and 538 < mouse [1] < 725 + 50:
                pygame.draw.rect(screen, bright_red, (305, 725, 100, 50))
            else:
                pygame.draw.rect(screen, red, (305, 725, 100, 50))

            if 466 < mouse[0] < 466 + 100 and 725 < mouse [1] < 725 + 50:
                pygame.draw.rect(screen, bright_blue, (466, 725, 100, 50))
            else:
                pygame.draw.rect(screen, blue, (466, 725, 100, 50))
            
            text = pygame.font.Font("freesansbold.ttf", 20)
            textSurf_1, textRect_1 = self.text_objects("START", text)
            textSurf_2, textRect_2 = self.text_objects("PAUSE", text)
            textSurf_3, textRect_3 = self.text_objects("RESET", text)
            textRect_1.center = ((140 + (100 / 2)), (725 + (50 / 2)))
            textRect_2.center = ((305 + (100 / 2)), (725 + (50 / 2)))
            textRect_3.center = ((466 + (100 / 2)), (725 + (50 / 2)))
            screen.blit(textSurf_1, textRect_1)
            screen.blit(textSurf_2, textRect_2)
            screen.blit(textSurf_3, textRect_3)
            # update the screen
            pygame.display.update()
            
    def rules(self):
        """ Applies Conway's rules to the matrix of cells
        and updates the matrix over generations. 
        """
        X = grid.copy()
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
                    # implementing Conway's 4 rules
                    if X[i, j] == 0:
                        if total_activation == 3: # birth 
                            grid[i, j] = 1
                        else: 
                            grid[i, j] = 0 # loneliness 
                    elif X[i, j] == 1:
                        if (total_activation < 2) or (total_activation > 3): # loneliness & overcrowding 
                            grid[i, j] = 0
                        else:
                            grid[i, j] = 1 # survival
        return grid
        
    def initial(self, pattern = r.randrange(1, 5, 1), index = r.randrange(10, 50, 1)): # randomly pick a pattern and a location 
        """ Randomly draws from four initial patterns
        and turns the corresponding cells alive. Returns 
        the grid with this starting pattern. The location
        of the starting pattern is also determined randomly. 
        
        1 is the glider 
        2 is the R-pentomino 
        3 is the light-weighted space ship 
        4 is the pentadecathlon
        """
        if pattern == 1: # glider 
            grid[index, index] = 1
            grid[index, index + 1] = 1
            grid[index, index + 2] = 1
            grid[index - 1, index + 2] = 1
            grid[index - 2, index + 1] = 1
        elif pattern == 2: # R-pentomino 
            grid[index, index] = 1
            grid[index + 1, index] = 1
            grid[index + 2, index] = 1
            grid[index + 1, index - 1] = 1
            grid[index, index + 1] = 1
        elif pattern == 3: # light-weight space ship
            grid[index, index] = 1
            grid[index, index + 1] = 1
            grid[index, index + 2] = 1
            grid[index, index + 3] = 1
            grid[index - 1, index] = 1
            grid[index - 2, index] = 1
            grid[index - 3, index + 1] = 1
            grid[index - 3, index + 4] = 1
            grid[index - 1, index + 4] = 1
        elif pattern == 4: # pentadecathlon
            l = list(range(index, index + 10))
            grid[index, [x for i, x in enumerate(l) if (i != 2 and i != 7)]] = 1
            grid[index + 1, [index + 2, index + 7]] = 1
            grid[index - 1, [index + 2, index + 7]] = 1
        return grid
        
    def update(self):
        """ If the user has pressed the start button,
        self.iterate becomes true. If iterating, this 
        function applies Conway's rules to the existing pattern.
        """
        if self.iterate:
            self.rules()
            
    def draw(self, screen):
        """ Draws the grid based on the matrix values. 
        If the matrix value is 1, the cell is drawn black. 
        If the matrix value is 0, the cell is drawn white. 
        """
        screen.fill(grey)
        for i in range(N):
            for j in range(N):
                if grid[i, j] == 0:
                    color = white
                elif grid[i][j] == 1:
                    color = black
                rect = pygame.draw.rect(screen, color, ((cell_width + margin) * j + margin, # x-coordinates of top-left corner 
                                                 (cell_height + margin) * i + margin, # y-coordinates of top-left corner
                                                 cell_width, cell_height)) 
        return rect  
    
    def state(self):
        """ Uses mouse clicks to turn dead 
        cells live and kill live cells. 
        """
        if grid[i][j] == 0:
            grid[i][j] = 1
        elif grid[i][j] == 1:
            grid[i][j] = 0
        return grid 
            
    def reset(self):
        """ Stops applying Conway's rules 
        and kills all the cells. 
        """
        for i in range(N):
            for j in range(N):
                grid[i, j] = 0
        return grid 
                
    def text_objects(self, text, font):
        """ Creates a text surface which is later added 
        to the start, pause and reset buttons. 
        """
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()