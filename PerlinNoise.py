import pygame
import os
import math
import numpy
from PIL import Image

SCREEN_WIDTH, SCREEN_HEIGHT = 256, 256
MAX_AMPLITUDE = 255*2/5

                
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


def randMatrix(frequency):
    return numpy.random.uniform(-1, 1, size=(frequency+4, frequency+4))


def smoothValue(x, y, matrix):
    corners = matrix[x-1][y-1] + matrix[x+1][y-1] + matrix[x-1][y+1] + matrix[x+1][y+1]
    sides = matrix[x-1][y] + matrix[x][y-1] + matrix[x+1][y] + matrix[x][y+1]
    return corners/16 + sides/8 + matrix[x][y]/4


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


def makeNoise(x, y, z, wOffset, hOffset, interpolator, matrix, smooth):
    xFloor = math.floor(x/wOffset)
    yFloor = math.floor(y/hOffset)
    prevX = xFloor+2
    nextX = xFloor+3
    prevY = yFloor+2
    nextY = yFloor+3
    fractionX = (x%wOffset)/wOffset
    fractionY = (y%hOffset)/hOffset

    if smooth:
        v1 = smoothValue(prevX, prevY, matrix)
        v2 = smoothValue(nextX, prevY, matrix)
        v3 = smoothValue(prevX, nextY, matrix)
        v4 = smoothValue(nextX, nextY, matrix)
    else:
        v1 = matrix[prevX][prevY]
        v2 = matrix[nextX][prevY]
        v3 = matrix[prevX][nextY]
        v4 = matrix[nextX][nextY]

    i1 = interpolator(v1, v2, fractionX)
    i2 = interpolator(v3, v4, fractionX)
    return interpolator(i1, i2, fractionY)


def pixelArrayAndInterpolateDraw(screen, frequency, amplitude, interpolator, smooth):
    wOffset = math.floor(SCREEN_WIDTH/frequency)
    hOffset = math.floor(SCREEN_HEIGHT/frequency)
    screenArray = pygame.surfarray.pixels3d(screen)
    matrix = randMatrix(frequency)
    for x in range(SCREEN_WIDTH):
        for y in range(SCREEN_HEIGHT):
            value = makeNoise(x, y, frequency, wOffset, hOffset, interpolator, matrix, smooth)*amplitude
            
            (aux, aux, aux) = screenArray[x][y]
            if aux+value < 0:
                screenArray[x,y] = (0,0,0)
            elif aux+value > 255:
                screenArray[x,y] = (255,255,255)
            else:
                screenArray[x,y] = (aux+value, aux+value, aux+value)


def pixelArrayAndInterpolateImg(screen, frequency, amplitude, interpolator, smooth):
    hOffset = math.floor(SCREEN_HEIGHT/frequency)
    wOffset = math.floor(SCREEN_WIDTH/frequency)
    matrix = randMatrix(frequency)
    for x in range(SCREEN_WIDTH):
        for y in range(SCREEN_HEIGHT):
            value = makeNoise(x, y, frequency, wOffset, hOffset, interpolator, matrix, smooth)*amplitude
            
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


def perlinNoise(interpolator, smooth):
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill((127, 127, 127))
    os.system('call sendkeys.bat "pygame window" ""')
    
    i = 0
    # so we don't go below the actual screen resolution
    while frequencyFor(i) < SCREEN_WIDTH:
        print("Iteration {0}...".format(i))
        pixelArrayAndInterpolateDraw(screen, frequencyFor(i), amplitudeFor(i), interpolator, smooth)
        # displays screen
        pygame.display.flip()
        print("Done.")
        i+=1

    print("All done!")


def imgPerlinNoise(filename, interpolator, smooth):
    # Create a 1024x1024x3 array of 8 bit unsigned integers
    screen = numpy.full( (SCREEN_WIDTH,SCREEN_HEIGHT,3), 127,dtype=numpy.uint8 ) # TODO: change data type!!

    i=0
    while frequencyFor(i) < SCREEN_WIDTH:
        print("Iteration {0}...".format(i))
        screen = pixelArrayAndInterpolateImg(screen, frequencyFor(i), amplitudeFor(i), interpolator, smooth)
        print("Done.")
        i+=1

    img = Image.fromarray(screen, mode='RGB')       # Create a PIL image
    img.save("{0}.png".format(filename))            # save to same directory
    print("All done!")


def main():
    choice1 = 0
    choice2 = 0
    smooth = False
    while not (choice1==1 or choice1==2):
        choice1 = int(input("Enter 1 to visualize generation, 2 to save an image: "))

    while not (choice2==1 or choice2==2):
        choice2 = int(input("Enter 1 for normal values, 2 for smooth values: "))

    if choice2==1:
        smooth = False
    elif choice2==2:
        smooth = 2
            
    
    if choice1==1:
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        perlinNoise(cosineInterpolation, smooth)
        waitForInput()
        pygame.quit()
    elif choice1==2:
        filename = input("Enter the desired filename (no extension): ");
        imgPerlinNoise(filename, cosineInterpolation, smooth)


if __name__ == "__main__":
    main()
