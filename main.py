import pygame
import sys
import numpy as np
import copy

import constants
import calc
import agent

import random

def main(**kwargs):

    print()
    for k, v in kwargs.items():
        print('Arg: {} = {}'.format(k, v))
    print()

    pygame.init()
    logo = pygame.image.load("logo_32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("evolution")

    # create a surface on screen
    constants.screen = pygame.display.set_mode((constants.SCREEN_X, constants.SCREEN_Y))
    fontSize = 20
    font = pygame.font.Font('freesansbold.ttf', fontSize)

    # clock
    clock = pygame.time.Clock()
    TICK = 60
    gameTick = 0

    # recording
    rec = kwargs.get('record')

    # Create a screen recorder object
    if rec:
        fname = kwargs.get('fname')
        print(fname)
        constants.outputFileName = fname if fname != None else 'output'
        print(constants.outputFileName)
        
        import record
        recorder = record.ScreenRecorder(constants.SCREEN_X, constants.SCREEN_Y, TICK)
     
    # define a variable to control the main loop
    running = True

    # actors
    s = 50
    actors = []
    evolutionRate = 0.001
    generation = 1


    start = [150, 150]
    startAngle = 0.8


    for i in range(s):
        actor = agent.Herbivore(
            id=0,
            location=start,
            angle=startAngle,
            colour="purple"
        )
        actors.append(actor)

    def setR(n):
        match n:
            case 1:
                return random.randint(100, 200)
            case 2:
                return random.randint(50, 75)
            case 3:
                return random.randint(50, 75)
            case 4:
                return random.randint(50, 125)
            case 5:
                return random.randint(50, 125)
            case 6:
                return random.randint(25, 75)

    obstacle1 = {
        'centre': [750, 575],
        'radius': 1,
        'colour': 'maroon'
    }
    obstacle2 = {
        'centre': [500, 700],
        'radius': 1,
        'colour': 'maroon'
    }
    obstacle3 = {
        'centre': [900, 350],
        'radius': 1,
        'colour': 'maroon'
    }
    obstacle4 = {
        'centre': [450, 485],
        'radius': 1,
        'colour': 'maroon'
    }
    obstacle5 = {
        'centre': [675, 285],
        'radius': 1,
        'colour': 'maroon'
    }
    obstacle6 = {
        'centre': [490, 300],
        'radius': 1,
        'colour': 'maroon'
    }

    obstacles = [obstacle1, obstacle2, obstacle3, obstacle4, obstacle5, obstacle6]

    for i, obstacle in enumerate(obstacles):
        obstacle["radius"] = setR(i+1)


    goal = {
        'centre': [constants.SCREEN_X, constants.SCREEN_Y],
        'radius': 100,
        'colour': 'green'
    }


    cohort = 100
    selectionSize = 10
    spawn = int(cohort / selectionSize)
    genTicks = 2500

    tickSinceLastGen = 0
    finishedActors = 0

    capture = [0, 1, 2, 5, 10, 25, 50, 100]
    
    while running:

        clock.tick(TICK)
        gameTick += 1
        tickSinceLastGen += 1

        for event in pygame.event.get():

            # QUIT
            if event.type == pygame.QUIT:
                running = False


        # RENDERING
        constants.screen.fill("white")

        # OBSTACLE
        for i, obstacle in enumerate(obstacles):
            pygame.draw.circle(constants.screen, obstacle['colour'], [obstacle['centre'][0], calc.flipY(obstacle['centre'][1])], obstacle['radius'])

        # GOAL 
        pygame.draw.circle(constants.screen, goal['colour'], [goal['centre'][0], calc.flipY(goal['centre'][1])], goal['radius'])


        alive = []
        stuck = 0

        # UPDATE ACTORS - keep living
        for actor in actors:

            distToTopRight = np.linalg.norm(
                calc.subVectors(
                [constants.SCREEN_X, constants.SCREEN_Y],
                actor.location
            ))

            if distToTopRight >= goal['radius']:
                
                if not(actor.isDead(obstacles)):
                    actor.think(obstacles)
                    alive.append(actor)
                    actor.draw()

            else:

                if actor.timeToGoal == None:
                    actor.timeToGoal = tickSinceLastGen
                    finishedActors += 1

                alive.append(actor)
                actor.draw()
                stuck += 1

        actors = alive

        # SELECT BEST ACTORS
        if (tickSinceLastGen >= genTicks) | (len(actors) <= selectionSize + 5) | (finishedActors >= selectionSize) | (stuck == len(actors)):

            for actor in actors:
                actor.distToTopRight = np.linalg.norm(
                    calc.subVectors(
                    [constants.SCREEN_X, constants.SCREEN_Y],
                    actor.location
                ))
                if actor.timeToGoal == None:
                    actor.timeToGoal = genTicks + 1

            actors.sort(key=lambda x: (x.timeToGoal, x.distToTopRight), reverse=False)
            actors = actors[:selectionSize]

            print("Generation", generation)
            print("Ticks", tickSinceLastGen)
            print("Alive", len(alive))
            print("Finished", finishedActors)
            print("Capturing", True if generation in capture else False)
            print()

            # reset
            for i, actor in enumerate(actors[:selectionSize]):

                actor.location = start
                actor.angle = startAngle
                actor.timeToGoal = None
                actor.distToTopRight = None

                if i == 0:
                    actor.colour = "chartreuse3"
                else:
                    actor.colour = "purple"

                for i in range(1, spawn):

                    newActor = copy.deepcopy(actor)
                    actors.append(newActor)

            generation += 1
            tickSinceLastGen = 0
            finishedActors = 0

            for i, obstacle in enumerate(obstacles):
                obstacle["radius"] = setR(i+1)

        # EVOLVE
        for actor in actors:
            actor.evolve(evolutionRate)

        if True:

            panelContent = [
                f"generation: {generation}",
            ]

            for i, content in enumerate(panelContent):

                text = font.render(content, True, "white", "black")
                textRect = text.get_rect()
                textRect.center = (constants.SCREEN_X * 0.1, constants.SCREEN_Y * 0.05 + i * fontSize)
                constants.screen.blit(text, textRect)


        pygame.display.flip()

        # Capture the frame
        if rec:
            if generation in capture:
                recorder.capture_frame(constants.screen)

    if rec:
        print()
        print("Saving recording...")
        recorder.end_recording()
        print("Recording Saved")
        print()

    
if __name__ == "__main__":
    main(
        **dict(
            arg.split('=') for arg in sys.argv[1:]
        )
    )