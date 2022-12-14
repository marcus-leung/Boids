from constants import pygame, random, num_boids, window_size, max_speed, screen
from BoidClass import Boid
import time

def main():
    pygame.init()

    pygame.display.set_caption('Boids')

    boids = []

    for n in range(num_boids):
        pos = [random.uniform(0, window_size), random.uniform(0, window_size)]
        vel = [random.uniform(-max_speed, max_speed), random.uniform(-max_speed, max_speed)]
        boid = Boid(pos, vel)
        boids.append(boid)

    pos = [random.uniform(0, window_size), random.uniform(0, window_size)]
    vel = [random.uniform(-max_speed, max_speed), random.uniform(-max_speed, max_speed)]
    boid_leader = Boid(pos, vel, True)
    boids.append(boid_leader)

    game_on = True
    while game_on:
        screen.fill((0,0,0))
        for b in boids:
            b.update(boids)
            b.display()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
    
        #time.sleep(0.1)
        pygame.display.update()

if __name__ == "__main__":
    main()