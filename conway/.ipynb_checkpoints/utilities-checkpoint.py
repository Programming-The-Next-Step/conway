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
    """ 
    A class for the cellular automaton Game of Life. It has 
    two properties that determine whether the game is running
    and whether Conway's rules are being iterated.
    
    Properties
    ''''''''''
    running: logical
        If True, the game is run. The default is False. Is True 
        when the main function play() is called. 
    iterate: logical 
        If True, the rules are applied to the grid and the Game of Life
        evolves over generations. The default is False. Is on when the user 
        clicks on the START button. Is False when the user clicks on the PAUSE 
        or the RESET button.
    """
    def __init__(self):
        """ 
        Constructor for the Life class. Takes no arguments. 
        """
        self.running = False 
        self.iterate = False
                
    def play(self, pattern = r.randrange(1, 5, 1)):
        """ 
        The main function of the game. Initiates the game by creating 
        a screen with a constant window size. Draws the buttons and runs 
        the event loop while responding to the buttons pressed. 
        
        Parameters 
        
        pattern 
            Determines the initial pattern that appears on the 
            screen when the game is started. It can take values between 
            1 and 4. The correspondence between the arguments and the patterns: 
        
            1 = glider 
            2 = R-pentomino 
            3 = light-weighted space ship 
            4 = pentadecathlon
        
            The default value is a randomly drawn integer. 
        """
        pygame.init() 
        self.running = True # runs the while loop 
        screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Game of Life")
        self.initial(pattern) # sets the initial pattern when the window opens
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
        """ 
        Applies Conway's rules to the matrix of cells
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
        
    def initial(self, pattern): 
        """ 
        Turns cells alive according to the pattern argument.
        Returns the grid with the chosen initial pattern. The 
        location of the pattern is chosen randomly by sampling 
        from grid coordinates. The coordinates of the edges are 
        excluded to make sure the pattern is fully visible. 
        
        1 = glider 
        2 = R-pentomino 
        3 = light-weighted space ship 
        4 = pentadecathlon
        
        Parameters 
        
        pattern 
           Specified in the main function play(). 
           The default is a random draw between 1 and 4. 
        """
        index = r.randrange(10, 50, 1) # randomly pick a location 
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
        """ 
        This function applies Conway's rules to the current pattern if
        the logical attribute iterate is True. iterate is True if the user 
        has pressed the start button.  
        """
        if self.iterate:
            self.rules()
            
    def draw(self, screen):
        """ 
        Draws the grid based on the matrix values. 
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
        """ 
        Uses mouse clicks to turn dead 
        cells live and kill live cells. 
        """
        if grid[i][j] == 0:
            grid[i][j] = 1
        elif grid[i][j] == 1:
            grid[i][j] = 0
        return grid 
            
    def reset(self):
        """ 
        Stops iterating the rules 
        and kills all the cells. 
        Returns an empty grid. 
        """
        for i in range(N):
            for j in range(N):
                grid[i, j] = 0
        return grid 
                
    def text_objects(self, text, font):
        """ 
        Creates a text surface which is later added 
        to the START, PAUSE and RESET buttons. 
        """
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()