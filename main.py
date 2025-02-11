import numpy as np
import pygame
from math import sin, cos
from cube import Cube

WIDTH = 800
HEIGHT = 600
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
LIME = (50, 205, 50)
color_dict = {0: WHITE, 1: YELLOW, 2: RED, 3: GREEN, 4: ORANGE, 5: BLUE}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
angle_x = 0.5
angle_y = 0
angle_z = 0
cube = Cube()

pygame.init()

is_rotating = True
is_pressed_key = False
lastKey = None
last_pressed_key = None
current_pressed_key = None
rotation_command = False
commands_segment_selection = {'A': 'L', 'D': 'R', 'S': 'D', 'W': 'U'}
commands_direction_selection = {'A': 'L', 'D': 'F'}


def control_definition(event):
    global is_rotating
    global is_pressed_key
    global lastKey
    global last_pressed_key
    global current_pressed_key
    global rotation_command
    global commands_segment_selection
    global commands_direction_selection

    if event.type == pygame.QUIT:
        pygame.quit()
        exit()

    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        pygame.quit()
        exit()

    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        is_rotating = not is_rotating

    if event.type == pygame.KEYUP:
        is_pressed_key = False

    if (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT) or (is_pressed_key and lastKey == pygame.K_RIGHT):
        angle_y -= 0.03
        is_pressed_key = True
        lastKey = pygame.K_RIGHT

    if (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT) or (is_pressed_key and lastKey == pygame.K_LEFT):
        angle_y += 0.03
        is_pressed_key = True
        lastKey = pygame.K_LEFT

    if (event.type == pygame.KEYDOWN and event.key == pygame.K_UP) or (is_pressed_key and lastKey == pygame.K_UP):
        angle_x -= 0.03
        is_pressed_key = True
        lastKey = pygame.K_UP

    if (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN) or (is_pressed_key and lastKey == pygame.K_DOWN):
        angle_x += 0.03
        is_pressed_key = True
        lastKey = pygame.K_DOWN

    if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
        last_pressed_key = current_pressed_key
        current_pressed_key = 'W'
        rotation_command = True

    if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
        last_pressed_key = current_pressed_key
        current_pressed_key = 'A'
        rotation_command = True

    if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
        last_pressed_key = current_pressed_key
        current_pressed_key = 'S'
        rotation_command = True

    if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
        last_pressed_key = current_pressed_key
        current_pressed_key = 'D'
        rotation_command = True


while True:
    clock.tick(60)

    for event in pygame.event.get()+[pygame.event.Event(0)]:
        control_definition(event)

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(angle_x), -sin(angle_x)],
        [0, sin(angle_x), cos(angle_x)],
    ]
    )
    rotation_y = np.matrix([
        [cos(angle_y), 0, sin(angle_y)],
        [0, 1, 0],
        [-sin(angle_y), 0, cos(angle_y)],
    ]
    )
    rotation_z = np.matrix([
        [cos(angle_z), -sin(angle_z), 0],
        [sin(angle_z), cos(angle_z), 0],
        [0, 0, 1],
    ]
    )
    if is_rotating:
        angle_y += 0.01
        # angle_x += 0.01
        # angle_z += 0.01
        pass
    screen.fill(GRAY)
    cube.cube.print_cube()
    cube.apply_transform([rotation_z, rotation_y, rotation_x])
    sides = cube.get_top_small_cubes()
    for side in sides:
        for position, color in side:
            # position = [(x[1], x[0])for x in position]
            pygame.draw.polygon(screen, color_dict[color], position)
            pygame.draw.polygon(screen, BLACK, position, width=1)
        # pygame.draw.polygon(screen, BLACK, side[0][0])
        # pygame.draw.polygon(screen, BLACK, side[1][0])
    selected_side = cube.get_top_sides()[0]
    p = selected_side.to_2d()
    temp = p[2]
    p[2] = p[3]
    p[3] = temp
    pygame.draw.polygon(
        screen, LIME, p, width=6)

    if rotation_command and last_pressed_key != None and current_pressed_key != None:

        cube.cube.turn(selected_side.color_num,
                       commands_segment_selection[last_pressed_key],
                       commands_direction_selection[current_pressed_key])

        last_pressed_key = None
        current_pressed_key = None
    rotation_command = False
    pygame.display.update()
