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


