import pygame
import os
import random
import math

SCREEN_WIDTH, SCREEN_HEIGHT = 512, 512
MAX_AMPLITUDE = 255/2

def getBlendModeFor(value):
    if(value<0):
        return pygame.BLEND_SUB
    else:
        return pygame.BLEND_ADD


def addToScreen(screen, frequency, amplitude):
    for i in range(frequency):
        for j in range(frequency):
            #square = pygame.Surface((SCREEN_WIDTH/frequency, SCREEN_HEIGHT/frequency))
            value = math.ceil(random.randint(0,math.ceil(amplitude*2))-amplitude)
            hOffset = (SCREEN_HEIGHT/frequency)
            wOffset = (SCREEN_WIDTH/frequency)
            posRect = pygame.Rect(i*wOffset, j*hOffset, wOffset, hOffset)
            blendMode = getBlendModeFor(value)
            value = math.fabs(value)
            #square.fill((value, value, value))
            #screen.blit(square, (i*wOffset, j*hOffset), special_flags=pygame.BLEND_ADD)
            screen.fill((value, value, value), rect=posRect, special_flags=blendMode)


def waitForInput():
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
    

def frequencyFor(i):
    return 2**(i+1)


def amplitudeFor(i):
    return MAX_AMPLITUDE/(1.4**i)


def perlinNoise():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    screen.fill((127, 127, 127))
    i = 0
    while frequencyFor(i) < SCREEN_WIDTH: # so we don't go below the actual screen resolution
        print("Iteration {0}...".format(i))
        addToScreen(screen, frequencyFor(i), amplitudeFor(i))
        #displays screen
        pygame.display.flip()
        print("Done.")
        i+=1

    print("All done!")


def main():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    perlinNoise()
    waitForInput()
    pygame.quit()


if __name__ == "__main__":
    main()
