import pygame
import os
import math
import numpy
from PIL import Image
from multiprocessing import Pool

SCREEN_WIDTH, SCREEN_HEIGHT = 256, 256
MAX_AMPLITUDE = 255 * 2/5

                
# --- INTERPOLATORS ---

# quickest but kinda harsh, not extremely bad though
def lerp(a, b, x):
    return a * (1-x) + b * x


# good smoothness and not too slow
def cosine_interpolation(a, b, x):
    ft = x * math.pi
    f = (1 - math.cos(ft)) * 0.5
    return a * (1-f) + b * f

# ---------------------


def rand_matrix(frequency):
    return numpy.random.uniform(-1, 1, size=(frequency + 4, frequency + 4))


def smooth_value(x, y, matrix):
    corners = (
            matrix[x - 1][y - 1]
            + matrix[x - 1][y + 1]
            + matrix[x + 1][y - 1]
            + matrix[x + 1][y + 1]
       )
    sides = (
            matrix[x - 1][y]
            + matrix[x + 1][y]
            + matrix[x][y - 1]
            + matrix[x][y + 1]
        )
    return (
            corners / 16
            + sides / 8
            + matrix[x][y] / 4
        )


def make_noise(x, y, z, wOffset, hOffset, interpolator, matrix, smooth):
    xFloor = math.floor(x/wOffset)
    yFloor = math.floor(y/hOffset)
    prevX = xFloor + 2
    nextX = xFloor + 3
    prevY = yFloor + 2
    nextY = yFloor + 3
    fractionX = (x % wOffset) / wOffset
    fractionY = (y % hOffset) / hOffset

    if smooth:
        v1 = smooth_value(prevX, prevY, matrix)
        v2 = smooth_value(nextX, prevY, matrix)
        v3 = smooth_value(prevX, nextY, matrix)
        v4 = smooth_value(nextX, nextY, matrix)
    else:
        v1 = matrix[prevX][prevY]
        v2 = matrix[nextX][prevY]
        v3 = matrix[prevX][nextY]
        v4 = matrix[nextX][nextY]

    i1 = interpolator(v1, v2, fractionX)
    i2 = interpolator(v3, v4, fractionX)
    return interpolator(i1, i2, fractionY)


def get_line(args):
    [screen, frequency, amplitude, x, wOffset, hOffset, interpolator, matrix, smooth] = args
    result = screen[x]
    for y in range(SCREEN_HEIGHT):
        value = make_noise(x, y, frequency, wOffset, hOffset, interpolator, matrix, smooth) * amplitude
            
        [aux, _, _] = screen[x, y]
        value += aux
        if value < 0:
            value = 0
        elif value > 255:
            value = 255
        result[y] = [value, value, value]
        
    return result


def generate_noise_array(screen, frequency, amplitude, interpolator, smooth):
    hOffset = math.floor(SCREEN_HEIGHT / frequency)
    wOffset = math.floor(SCREEN_WIDTH / frequency)
    matrix = rand_matrix(frequency)

    with Pool(4) as p:
        screen = p.map(get_line, [[screen, frequency, amplitude, x, wOffset, hOffset, interpolator, matrix, smooth] for x in range(SCREEN_WIDTH)])
    
    return numpy.array(screen)


def frequency_for(i):
    return 2 ** (i + 1)


def amplitude_for(i):
    return MAX_AMPLITUDE / (1.5 ** i)


def draw_perlin_noise(interpolator, smooth, value_array):
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill((127, 127, 127))
    os.system('call sendkeys.bat "pygame window" ""')
    pygame.display.flip()
    
    i = 0
    # so we don't go below the actual screen resolution
    while frequency_for(i) < SCREEN_WIDTH:
        print("Iteration {0}...".format(i))
        value_array = generate_noise_array(value_array, frequency_for(i), amplitude_for(i), interpolator, smooth)
        # displays screen
        pygame.surfarray.blit_array(screen, value_array)
        pygame.display.flip()
        print("Done.")
        i+=1
        if frequency_for(i) < SCREEN_WIDTH:
            input("Press Return for the next iteration!")

    print("All done!")


def img_perlin_noise(filename, interpolator, smooth, value_array):
    i=0
    while frequency_for(i) < SCREEN_WIDTH:
        print("Iteration {0}...".format(i))
        value_array = generate_noise_array(value_array, frequency_for(i), amplitude_for(i), interpolator, smooth)
        print("Done.")
        i+=1

    img = Image.fromarray(value_array, mode = 'RGB')       # Create a PIL image
    img.save("{0}.png".format(filename))            # save to same directory
    print("All done!")


def wait_for_input():
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True


def main():
    choice1 = 0
    choice2 = 0
    choice3 = 0
    smooth = False
    
    while not (choice1 in [1, 2]):
        choice1 = int(input("Enter 1 to visualize generation, 2 to save an image: "))
    while not (choice2 in [1, 2]):
        choice2 = int(input("Enter 1 for normal values, 2 for smooth values: "))
    while not (choice3 in [1, 2]):
        choice3 = int(input("Enter 1 for lerp interpolation, 2 for cosine interpolation: "))

    if choice2 == 1:
        smooth = False
    else:
        smooth = True
        MAX_AMPLITUDE = 255 # testing

    if choice3 == 1:
        interpolator = lerp
    else:
        interpolator = cosine_interpolation

    # Create a 1024x1024x3 array of 8 bit unsigned integers
    value_array = numpy.full((SCREEN_WIDTH, SCREEN_HEIGHT, 3), 127, dtype = numpy.uint8) # TODO: change data type??
    
    if choice1 == 1:
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        draw_perlin_noise(interpolator, smooth, value_array)
        wait_for_input()
        pygame.quit()
    else:
        filename = input("Enter the desired filename (no extension): ");
        img_perlin_noise(filename, interpolator, smooth, value_array)


if __name__ == "__main__":
    main()
