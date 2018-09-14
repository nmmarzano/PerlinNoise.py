import pygame
import os
import random
import math
import numpy
from PIL import Image

SCREEN_WIDTH, SCREEN_HEIGHT = 512, 512
MAX_AMPLITUDE = 255*2/5
MASTER_SEED = random.uniform(0, 1);


# --- PRNG ---

# no post-processing, takes an optional 'extra' value to get a different set of random values for the same (X,Y), used for successive iterations
def deterministicRandom(x, y, extra=0):
    random.seed(x+extra+MASTER_SEED)
    random.seed(y*random.uniform(1,2)+extra+MASTER_SEED)
    result = random.uniform(-1, 1)
    return result


# smooths deterministicRandom(...) values, takes way too long and results are extremely bland so not recommended unless smooth noise is required
def smoothDeterministicRandom(x, y, extra):
    corners = deterministicRandom(x-1,y-1,extra) + deterministicRandom(x+1,y-1,extra) + deterministicRandom(x-1,y+1,extra) + deterministicRandom(x+1,y+1,extra)
    sides = deterministicRandom(x-1,y,extra) + deterministicRandom(x,y-1,extra) + deterministicRandom(x+1,y,extra) + deterministicRandom(x,y+1,extra)

    return corners/16 + sides/8 + deterministicRandom(x, y,extra)/4

# ------------

                
# --- INTERPOLATORS ---

# quickest but kinda harsh, not extremely bad though
def lerp(a, b, x):
    return a*(1-x) + b*x


# good smoothness and not too slow
def cosineInterpolation(a, b, x):
    ft = x*math.pi
    f = (1 - math.cos(ft))*0.5
    return a*(1-f) + b*f

# ---------------------


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


def makeNoise(x, y, wOffset, hOffset, randomizer, interpolator):
    prevX = math.floor(x/wOffset)
    nextX = (math.floor(x/wOffset)+1)
    prevY = math.floor(y/hOffset)
    nextY = (math.floor(y/hOffset)+1)
    fractionX = (x%wOffset)/wOffset
    fractionY = (y%hOffset)/hOffset

    v1 = randomizer(prevX,prevY,frequency)*amplitude
    v2 = randomizer(nextX,prevY,frequency)*amplitude
    v3 = randomizer(prevX,nextY,frequency)*amplitude
    v4 = randomizer(nextX,nextY,frequency)*amplitude

    i1 = interpolator(v1, v2, fractionX)
    i2 = interpolator(v3, v4, fractionX)
    
    return interpolator(i1, i2, fractionY)


def pixelArrayAndInterpolateDraw(screen, frequency, amplitude, randomizer, interpolator):
    wOffset = math.floor(SCREEN_WIDTH/frequency)
    hOffset = math.floor(SCREEN_HEIGHT/frequency)
    screenArray = pygame.surfarray.pixels3d(screen)
    for x in range(SCREEN_WIDTH):
        for y in range(SCREEN_HEIGHT):
            value = makeNoise(x, y, wOffset, hOffset, randomizer, interpolator)
            
            (aux, aux, aux) = screenArray[x][y]
            if aux+value < 0:
                screenArray[x,y] = (0,0,0)
            elif aux+value > 255:
                screenArray[x,y] = (255,255,255)
            else:
                screenArray[x,y] = (aux+value, aux+value, aux+value)


def pixelArrayAndInterpolateImg(screen, frequency, amplitude, randomizer, interpolator):
    hOffset = math.floor(SCREEN_HEIGHT/frequency)
    wOffset = math.floor(SCREEN_WIDTH/frequency)
    for x in range(SCREEN_WIDTH):
        for y in range(SCREEN_HEIGHT):
            value = makeNoise(x, y, wOffset, hOffset, randomizer, interpolator)
            
            [aux, aux, aux] = screen[x,y]
            if aux+value < 0:
                screen[x,y] = [0,0,0]
            elif aux+value > 255:
                screen[x,y] = [255,255,255]
            else:
                screen[x,y] = [aux+value, aux+value, aux+value]

    return screen


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


def imgPerlinNoise(filename):
    # Create a 1024x1024x3 array of 8 bit unsigned integers
    screen = numpy.full( (SCREEN_WIDTH,SCREEN_HEIGHT,3), 127,dtype=numpy.uint8 ) # TODO: change data type!!

    i=0
    while frequencyFor(i) < SCREEN_WIDTH:
        print("Iteration {0}...".format(i))
        screen = pixelArrayAndInterpolateImg(screen, frequencyFor(i), amplitudeFor(i), deterministicRandom, cosineInterpolation)
        print("Done.")
        i+=1

    img = Image.fromarray(screen, mode='RGB')       # Create a PIL image
    img.save("{0}.png".format(filename))                      # save to same directory
    print("All done!")


def main():
    input = 0
    while not (input==1 or input==2):
        input = int(input("Enter 1 to visualize generation, 2 to save an image: "))
    
    if input==1:
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        perlinNoise()
        waitForInput()
        pygame.quit()
    elsif input==2:
        filename = input("Enter the desired filename (no extension): ");
        imgPerlinNoise(filename)


if __name__ == "__main__":
    main()
