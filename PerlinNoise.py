import pygame
import os
import random
import math

SCREEN_WIDTH, SCREEN_HEIGHT = 400, 400
MAX_AMPLITUDE = 255/2

def addToScreen(screen, frequency, amplitude):
    for i in range(frequency):
        for j in range(frequency):
            #square = pygame.Surface((SCREEN_WIDTH/frequency, SCREEN_HEIGHT/frequency))
            value = math.ceil(random.randint(0,math.ceil(amplitude*2))-amplitude)
            posRect = pygame.Rect(i*(SCREEN_WIDTH/frequency), j*(SCREEN_HEIGHT/frequency), SCREEN_WIDTH/frequency, SCREEN_HEIGHT/frequency)
            if value >= 0:
                #square.fill((value, value, value))
                #screen.blit(square, (i*(SCREEN_WIDTH/frequency), j*(SCREEN_HEIGHT/frequency)), special_flags=pygame.BLEND_ADD)
                screen.fill((value, value, value), rect=posRect, special_flags=pygame.BLEND_ADD)
            else:
                #square.fill((-value, -value, -value))
                #screen.blit(square, (i*(SCREEN_WIDTH/frequency), j*(SCREEN_HEIGHT/frequency)), special_flags=pygame.BLEND_SUB)
                screen.fill((-value, -value, -value), rect=posRect, special_flags=pygame.BLEND_SUB)


def waitForInput():
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True


def main():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    screen.fill((127, 127, 127))
    i = 0
    while 2**(i+1)<SCREEN_WIDTH: # so we don't go below the actual screen resolution
        print("Iteration {0}...".format(i))
        addToScreen(screen, 2**(i+1), MAX_AMPLITUDE/(1.3**i))
        #displays screen
        pygame.display.flip()
        print("Done.")
        i+=1
    
    waitForInput()
    pygame.quit()


if __name__ == "__main__":
    main()
