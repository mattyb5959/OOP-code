import pygame, sys
import os
from pygame.math import Vector2 as vector

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TILE_SIZE = 64
ANIMATION_SPEED = 6

Z_LAYERS = {}



#-----------------------------Make sure the directory is correct----------------------



# Get the directory containing the current file
current_file_directory = os.path.dirname(os.path.abspath(__file__))
#print(current_file_directory)

# Get the directory containing settings.py (assuming it's in the 'code' directory)
#project_directory = os.path.abspath(os.path.join(current_file_directory, os.pardir))
#print(project_directory)

#sys.path.append(project_directory)
#print(project_directory)

os.chdir(current_file_directory)

#print(sys.path)


#-------------------------------------------------------------------------------------