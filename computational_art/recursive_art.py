""" TODO: Put your header comment here """

import random
import math
from PIL import Image

def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    # TODO: implement this

    depth = random.choice(range(min_depth, max_depth))
    return make_function(depth)

    #Nice. Your make_function is nice and simple, and nicely gets around the random depths between min and max depth.

def make_function(depth):
    if depth == 1:
        return random.choice(['x', 'y'])
    modifiers = ['prod', 'avg', 'cos_pi', 'sin_pi', 'tan_pi', 'abs']
    modifier = random.choice(modifiers)
    if modifier == "prod":
        return ["prod", make_function(depth-1), make_function(depth-1)]
    elif modifier == "avg":
        return ["avg", make_function(depth-1), make_function(depth-1)]
    elif modifier == 'sqr':
        return ["sqr", make_function(depth-1)]
    elif modifier == 'half':
        return ["half", make_function(depth-1)]
    elif modifier == "cos_pi":
        return ["cos_pi", make_function(depth-1)]
    elif modifier == "sin_pi":
        return ["sin_pi", make_function(depth-1)]
    elif modifier == "tan_pi":
        return ["tan_pi", make_function(depth-1)]
    elif modifier == "abs":
        return ["abs", make_function(depth-1)]

    #You should add some doctests though. Even if it's random, you can check if it outputs the right depth and all

def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
        >>> evaluate_random_function(['prod', ['x'], ['y']], 1, 2)
        2.0
        >>> evaluate_random_function(['avg', ['x'], ['y']], 1, 2)
        1.5
        >>> evaluate_random_function(['cos_pi', ['x']], 0, 2)
        1.0
        >>> evaluate_random_function(['sin_pi', ['y']], 1, 0)
        0.0
        >>> evaluate_random_function(['prod', ['avg', ['x'], ['y']], ['prod', ['x'], ['y']]], 2, 2)
        8.0
        >>> evaluate_random_function(['sqr', ['y']], 1, .5)
        0.25
        >>> evaluate_random_function(['half', ['y']], 1, 1)
        0.5
    """
    # TODO: implement this
    if len(f) == 1:
        if f[0] == 'x':
            return float(x)
        elif f[0] == 'y':
            return float(y)
    else:
        if f[0] == 'prod':
            return float(evaluate_random_function(f[1], x, y))*evaluate_random_function(f[2], x, y)
        elif f[0] == 'avg':
            return (evaluate_random_function(f[1], x, y)+evaluate_random_function(f[2], x, y))/2.0
        elif f[0] == 'sqr':
            return float(evaluate_random_function(f[1], x, y))**2.0
        elif f[0] == 'half':
            return evaluate_random_function(f[1], x, y)*.5
        elif f[0] == 'cos_pi':
            return math.cos(math.pi*evaluate_random_function(f[1], x, y))
        elif f[0] == 'sin_pi':
            return math.sin(math.pi*evaluate_random_function(f[1], x, y))
        elif f[0] == 'tan_pi':
            return math.tan(math.pi*evaluate_random_function(f[1], x, y))
        elif f[0] == 'abs':
            return abs(evaluate_random_function(f[1], x, y))

        #YAY TESTS <3 Overall nice. The floats is kind of confusing/sketchy looking though. It might be cleaner to convert x and y
        # to floats at the top of this function rather than in each seperate if statement. 

def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    # TODO: implement this
    diff1 = input_interval_end - input_interval_start
    diff2 = output_interval_end - output_interval_start
    valDiff1 = val - input_interval_start
    fraction1 = float(valDiff1) / diff1
    fraction2 = fraction1 * diff2

    return fraction2 + output_interval_start

    #This is a little confusing to someone who doens't know what you're doing. It can be a good idea to split things up
    # between multiple lines, but I think you did that a little too much here - it might make more sense in two lines instead
    # of five. Yay tests though!

def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)

def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)

def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)
    print 'red function: ' + str(red_function)
    print 'green function: ' + str(green_function)
    print 'blue function: ' + str(blue_function)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                color_map(evaluate_random_function(red_function, x, y)),
                color_map(evaluate_random_function(green_function, x, y)),
                color_map(evaluate_random_function(blue_function, x, y))
                )

    im.save(filename)

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    z = 49
    nameNum = range(z, z+5)
    str1 = 'art' + str(nameNum[0]) + '.png'
    str2 = 'art' + str(nameNum[1]) + '.png'
    str3 = 'art' + str(nameNum[2]) + '.png'
    str4 = 'art' + str(nameNum[3]) + '.png'
    str5 = 'art' + str(nameNum[4]) + '.png'

    generate_art(str1, 1920, 1080)

    #Huh. Cool modifications to make the screen bigger. Cool art too. I get what you're doing here above with the file
    # names, but perhaps explain it better, or wrap it in a main function. Overall, nice code, and good job implementing
    # tests and taking it further. 

    # generate_art(str2, 1920, 1080)
    # generate_art(str3, 1920, 1080)
    # generate_art(str4, 1920, 1080)
    # generate_art(str5, 1920, 1080)