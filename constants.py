import pygame
import random

#Size of the window
window_size = 800

max_speed = 2
max_force = 5
avoidance_distance = 35
alignment_distance = 40
cohesion_distance = 400
leader_distance = 50
# Define the number of boids in the flock
num_boids = 20 #not including leader

screen = pygame.display.set_mode((window_size, window_size))