import pygame

import constants
import calc

class Eye:

    def __init__(self, parent, angle=0, length=20):

        self.parent=parent
        self.angle=angle
        self.length=length
        self.obstacleDetected=False

    def detectObstacles(self, obstacles):

        self.rayStart = self.parent.location
        angle = self.parent.angle + self.angle
        self.rayEnd = calc.addVectors(self.rayStart, calc.scaleVector(calc.vectorFromAngle(angle), self.length))

        for obstacle in obstacles:
            if calc.lineIntersectsCircle(self.rayStart, self.rayEnd, obstacle['centre'], obstacle['radius']) > 0:
                self.obstacleDetected = True
                return 1

        # wall detection
        if calc.outOfBounds(self.rayEnd):
            self.obstacleDetected = True
            return 1

        self.obstacleDetected = False
        return 0

    def draw(self):
        colour = "grey" if self.obstacleDetected == False else "red"
        pygame.draw.line(
            constants.screen, 
            colour, 
            [self.rayStart[0], calc.flipY(self.rayStart[1])], 
            [self.rayEnd[0], calc.flipY(self.rayEnd[1])],
            1
        )
