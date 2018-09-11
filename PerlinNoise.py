import pygame
import os
import random
import math
import numpy

SCREEN_WIDTH, SCREEN_HEIGHT = 512, 512
MAX_AMPLITUDE = 255/2

MASTER_SEED = random.randint(100, 200);


def deterministicRandom(x, y):
    random.seed(x+MASTER_SEED)
    result = random.uniform(-1, 1)
    for i in range(y+4):
        result = random.uniform(-1, 1)
    return result


def smoothDeterministicRandom(x, y):
    corners = deterministicRandom(x-1,y-1) + deterministicRandom(x+1,y-1) + deterministicRandom(x-1,y+1) + deterministicRandom(x+1,y+1)
    sides = deterministicRandom(x-1,y) + deterministicRandom(x,y-1) + deterministicRandom(x+1,y) + deterministicRandom(x,y+1)

    return corners/16 + sides/8 + deterministicRandom(x, y)/4


def getBlendModeFor(value):
    if(value<0):
        return pygame.BLEND_SUB
    else:
        return pygame.BLEND_ADD


def waitForInput():
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True


def lerp(a, b, x):
    return a*(1-x) + b*x


def cosineInterpolation(a, b, x):
    ft = x*math.pi
    f = (1 - math.cos(ft))*0.5
    return a*(1-f) + b*f
   

def randomGridAndInterpolateDraw(screen, frequency, amplitude, randomizer, interpolator):
    hOffset = math.floor(SCREEN_HEIGHT/frequency)
    wOffset = math.floor(SCREEN_WIDTH/frequency)
    for x in range(SCREEN_WIDTH):
        for y in range(SCREEN_HEIGHT):
            prevX = math.floor(x/wOffset)
            nextX = (math.floor(x/wOffset)+1)
            prevY = math.floor(y/hOffset)
            nextY = (math.floor(y/hOffset)+1)
            fractionX = (x%wOffset)/wOffset
            fractionY = (y%hOffset)/hOffset

            v1 = randomizer(prevX,prevY)*amplitude
            v2 = randomizer(nextX,prevY)*amplitude
            v3 = randomizer(prevX,nextY)*amplitude
            v4 = randomizer(nextX,nextY)*amplitude

            i1 = interpolator(v1, v2, fractionX)
            i2 = interpolator(v3, v4, fractionX)

            value = interpolator(i1, i2, fractionY)
            
            blendMode = getBlendModeFor(value)
            if value<0:
                value = -value
            screen.fill((value, value, value), rect=(x,y,1,1), special_flags=blendMode)


def pixelArrayAndInterpolateDraw(screen, frequency, amplitude, randomizer, interpolator):
    hOffset = math.floor(SCREEN_HEIGHT/frequency)
    wOffset = math.floor(SCREEN_WIDTH/frequency)
    screenArray = pygame.surfarray.pixels3d(screen)
    for x in range(SCREEN_WIDTH):
        for y in range(SCREEN_HEIGHT):
            prevX = math.floor(x/wOffset)
            nextX = (math.floor(x/wOffset)+1)
            prevY = math.floor(y/hOffset)
            nextY = (math.floor(y/hOffset)+1)
            fractionX = (x%wOffset)/wOffset
            fractionY = (y%hOffset)/hOffset

            v1 = randomizer(prevX,prevY)*amplitude
            v2 = randomizer(nextX,prevY)*amplitude
            v3 = randomizer(prevX,nextY)*amplitude
            v4 = randomizer(nextX,nextY)*amplitude

            i1 = interpolator(v1, v2, fractionX)
            i2 = interpolator(v3, v4, fractionX)

            value = interpolator(i1, i2, fractionY)
            
            (aux, aux, aux) = screenArray[x][y]
            if aux+value < 0:
                screenArray[x][y] = (0,0,0)
            elif aux+value > 255:
                screenArray[x][y] = (255,255,255)
            else:
                screenArray[x][y] = (aux+value, aux+value, aux+value)


def frequencyFor(i):
    return 2**(i+1)


def amplitudeFor(i):
    return MAX_AMPLITUDE/(1.5**i)


def perlinNoise():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    screen.fill((127, 127, 127))
    i = 0

    # so we don't go below the actual screen resolution
    while frequencyFor(i) < SCREEN_WIDTH:
        print("Iteration {0}...".format(i))
        pixelArrayAndInterpolateDraw(screen, frequencyFor(i), amplitudeFor(i), deterministicRandom, cosineInterpolation)
        # displays screen
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
