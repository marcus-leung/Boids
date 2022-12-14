from constants import (pygame, window_size, screen, avoidance_distance, alignment_distance, cohesion_distance,
    max_speed, leader_distance, num_boids)
import math

class Boid:
    def __init__(self, pos, vel, isLeader=False):
        self.pos = pos
        self.vel = vel
        self.leader = isLeader

    def drawBoid(self, x, y, direction):
        if self.leader:
            pygame.draw.circle(screen, (255, 255, 255), (x, y), 10)
            pygame.draw.line(screen, (255, 255, 255), (x, y), (x + direction[0] * 10, y + direction[1] * 10), 2)
        else:
            pygame.draw.circle(screen, (100, 100, 255), (x, y), 10)
            pygame.draw.line(screen, (100, 100, 255), (x, y), (x + direction[0] * 10, y + direction[1] * 10), 2)

    def display(self): 
        self.drawBoid(self.pos[0], self.pos[1], self.vel)

    def update(self, boids):
        if (not self.leader):
            v1 = self.cohesion(boids)
            v2 = self.avoidance(boids)
            v3 = self.align(boids)
            v4 = self.followLeader(boids)

            v = [0, 0]
            v[0] = v1[0] + v2[0] + v3[0] + v4[0]
            v[1] = v1[1] + v2[1] + v3[1] + v4[1]

            self.vel[0] += v[0]*0.1
            self.vel[1] += v[1]*0.1

            self.limitVel()

            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]

            self.edge()
        else: #if leader
            v1 = self.cohesion(boids)
            v2 = self.avoidance(boids)

            v = [0, 0]
            v[0] = v1[0] + v2[0]
            v[1] = v1[1] + v2[1]


            self.vel[0] += v[0]*0.1
            self.vel[1] += v[1]*0.1

            self.limitVel()

            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]

            self.edge()

    # def edge(self): #for avoid edges
    #     if (self.pos[0] < 0): 
    #         self.vel[0] = abs(self.vel[0])
    #     elif (self.pos[0] > window_size):
    #         self.vel[0] = -abs(self.vel[0])

    #     if (self.pos[1] < 0):
    #         self.vel[1] = abs(self.vel[0])
    #     elif (self.pos[1] > window_size):
    #         self.vel[1] = -abs(self.vel[0])

    def edge(self): #for circular edges
        if (self.pos[0] < 0): 
            self.pos[0] = window_size
        elif (self.pos[0] > window_size):
            self.pos[0] = 0

        if (self.pos[1] < 0):
            self.pos[1] = window_size
        elif (self.pos[1] > window_size):
            self.pos[1] = 0

    def limitVel(self):
        if (self.vel[0] > max_speed):
            self.vel[0] = max_speed
        elif (self.vel[0] < -max_speed):
            self.vel[0] = -max_speed

        if (self.vel[1] > max_speed):
            self.vel[1] = max_speed
        elif (self.vel[1] < -max_speed):
            self.vel[1] = -max_speed

    def followLeader(self, boids):
        for b in boids:
            dist = math.sqrt((b.pos[0] - self.pos[0])**2 + (b.pos[1] - self.pos[1])**2)
            if (b.leader and dist < leader_distance):
                return [b.vel[0], b.vel[1]]
        return [0, 0]

    def avoidance(self, boids):
        avoid_vector = [0, 0]
        for b in boids:
            dist = math.sqrt((b.pos[0] - self.pos[0])**2 + (b.pos[1] - self.pos[1])**2)
            if (b != self and dist < avoidance_distance):
                avoid_vector[0] -= (b.pos[0] - self.pos[0])
                avoid_vector[1] -= (b.pos[1] - self.pos[1])

        return avoid_vector

    def align(self, boids):
        align_vector = [0, 0]
        for b in boids:
            dist = math.sqrt((b.pos[0] - self.pos[0])**2 + (b.pos[1] - self.pos[1])**2)
            if (b != self and dist < alignment_distance):
                align_vector[0] += b.vel[0]
                align_vector[1] += b.vel[1]

        align_vector[0] = align_vector[0] / (num_boids - 1)
        align_vector[1] = align_vector[1] / (num_boids - 1)
        result = [ (align_vector[0] - self.vel[0])/10, (align_vector[1] - self.vel[1])/10 ]
        return result

    def cohesion(self, boids):
        center = [0, 0]
        for b in boids:
            dist = math.sqrt((b.pos[0] - self.pos[0])**2 + (b.pos[1] - self.pos[1])**2)
            if (b != self and dist < cohesion_distance):
                center[0] += b.pos[0]
                center[1] += b.pos[1]

        center[0] = center[0] / (num_boids - 1)
        center[1] = center[1] / (num_boids - 1)
        result = [ (center[0] - self.pos[0])/100, (center[1] - self.pos[1])/100 ]
        return result