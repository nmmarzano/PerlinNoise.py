import pygame
import os
import random
import math

SCREEN_WIDTH, SCREEN_HEIGHT = 400, 400
MAX_AMPLITUDE = 255/2

def addToScreen(screen, grid):
    for i, column in enumerate(grid):
        for j, value in enumerate(column):
            square = pygame.Surface((SCREEN_WIDTH/len(grid), SCREEN_HEIGHT/len(grid)))
            if value >= 0:
                square.fill((value, value, value))
                screen.blit(square, (i*(SCREEN_WIDTH/len(grid)), j*(SCREEN_HEIGHT/len(grid))), special_flags=pygame.BLEND_ADD)
            else:
                square.fill((-value, -value, -value))
                screen.blit(square, (i*(SCREEN_WIDTH/len(grid)), j*(SCREEN_HEIGHT/len(grid))), special_flags=pygame.BLEND_SUB)
            #pygame.draw.rect(screen, (value, value, value), [i*(SCREEN_WIDTH/len(grid)), j*(SCREEN_HEIGHT/len(grid)), (i+1)*(SCREEN_WIDTH/len(grid)), (j+1)*(SCREEN_HEIGHT/len(grid))], 0)


def waitForInput():
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True


def randomGrid(frequency, amplitude):
    return [[math.ceil(random.randint(0,math.ceil(amplitude*2))-amplitude) for y in range(frequency)] for x in range(frequency)]


def main():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    screen.fill((127, 127, 127))
    for i in range(8):
        grid = randomGrid(2**(i+1), MAX_AMPLITUDE/(2**i)) # huge grids for big ranges, extremely inefficient, hangs on too many iterations
        addToScreen(screen, grid)

    #displays screen
    pygame.display.flip()
    
    waitForInput()
    pygame.quit()


if __name__ == "__main__":
    main()
