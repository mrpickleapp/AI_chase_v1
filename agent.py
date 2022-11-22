import pygame
import numpy as np

import constants
import calc
import ai
import eye


class Agent():

    def __init__(self, id, location, angle, health, colour, eyes=[]):
        self.id = id
        self.location = location
        self.angle = angle
        self.speed = 0
        self.health = health
        self.eyes = []
        self.colour = colour
        self.AI = ai.AI()

        self.timeToGoal = None

        self.maxSpeed = 100

    def think(self, obstacles=[]):

        input = []

        for e in self.eyes:
            input.append(e.detectObstacles(obstacles))

        vectorToGoal = calc.getLineVector(
            self.location, [constants.SCREEN_X, constants.SCREEN_Y]
        )
        vectorToGoalAngle = calc.theta(vectorToGoal, [1, 0])
        angleToGoal = self.angle - vectorToGoalAngle

        input.extend([
            angleToGoal
        ])

        output = self.AI.compute(input)

        self.angle += output[0] / 10
        self.speed += output[1] + 0.5
        self.speed = min(self.speed, self.maxSpeed) / 2

        velocity = calc.scaleVector(calc.vectorFromAngle(self.angle), self.speed)

        self.move(velocity)

    def move(self, velocity):
        
        self.location = calc.addVectors(self.location, velocity)

    def isDead(self, obstacles):

        if calc.outOfBounds(self.location):
            return True

        for obstacle in obstacles:
            if calc.pointDistance(self.location, obstacle["centre"]) <= obstacle["radius"]:
                return True

        return False


    def evolve(self, evolution_rate):
        self.AI.evolve(evolution_rate=evolution_rate)


class Herbivore(Agent):

    def __init__(self, id, location, colour, angle=0):
        super().__init__(id=id, location=location, angle=angle, health=100, colour=colour)

        self.eyes.append(
            eye.Eye(
                parent=self, angle=0, length=60
            )
        )
        self.eyes.append(
            eye.Eye(
                parent=self, angle=-0.5, length=40
            )
        )
        self.eyes.append(
            eye.Eye(
                parent=self, angle=0.5, length=40
            )
        )
        self.eyes.append(
            eye.Eye(
                parent=self, angle=-0.9, length=25
            )
        )
        self.eyes.append(
            eye.Eye(
                parent=self, angle=0.9, length=25
            )
        )


    def tick(self):
        self.health -= 1

    def eat(self):
        self.health += 25

    def draw(self):
        screen_x = self.location[0]
        screen_y = calc.flipY(self.location[1])

        pygame.draw.circle(constants.screen, self.colour, [screen_x, screen_y], 10)

        if False:
            for eyeLine in self.eyes:
                eyeLine.draw()


