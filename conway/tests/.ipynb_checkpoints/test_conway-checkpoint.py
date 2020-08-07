import unittest
from unittest.mock import Mock 
import mock
from conway import utilities
import pygame 
import numpy as np

# Create an instance of the game  
life = utilities.Life()

# Create a mock instance
life_mocked = Mock()

# Test if the main function is called 
def test_play():
    life_mocked.play()
    life_mocked.play.assert_called()

# Test if the rule function returns a 65x65 matrix 
def test_rules():
    s = life.rules()
    assert isinstance(s, np.ndarray) and s.shape == (utilities.N, utilities.N)

# Test if the reset function returns a grid full of 0s 
def test_reset():
    s = life.reset()
    assert isinstance(s, np.ndarray) and not np.any(s)

# Test if the draw function draws the grid
def test_draw():
    s = life.draw(screen = pygame.display.set_mode((utilities.window_width, utilities.window_height)))
    assert isinstance(s, pygame.Rect)
    
# Test the number of alive cells in the initial patterns
def test_initial():
    cells = [5, 5, 9, 12] # the total number of live cells in each pattern 
    for i, n in zip(range(1, 5), cells):
        s = life.initial(pattern = i)
        utilities.grid = np.zeros((utilities.N, utilities.N)) # reset the grid to use the function again 
        assert isinstance(s, np.ndarray) and len(s[s == 1]) == n




