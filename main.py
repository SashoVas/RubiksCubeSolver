import numpy as np
import pygame
from math import sin, cos
from cube import Cube

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
angle_x = 10
angle_y = 0
angle_z = 0
is_rotating = True
cube = Cube()
is_pressed_key = False
lastKey = None
while True:
    clock.tick(60)

    for event in pygame.event.get()+[pygame.event.Event(0)]:
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
        angle_x += 0.01
        angle_z += 0.01
    screen.fill(GRAY)
    i = 0
    cube.apply_transform([rotation_z, rotation_y, rotation_x])

    for side in cube.get_top_sides():
        points = side.to_2d()

        pygame.draw.polygon(screen, side.color, points)
        pygame.draw.polygon(screen, BLACK, points, 3)

        edge_points = side.get_edge_points()
        for points in edge_points:
            for point in points:
                pygame.draw.circle(screen, BLACK, point, 4)

        for pointA, pointB in zip(edge_points[0], edge_points[2][::-1]):
            pygame.draw.line(screen, BLACK, pointA, pointB)

        for pointA, pointB in zip(edge_points[1], edge_points[3][::-1]):
            pygame.draw.line(screen, BLACK, pointA, pointB)
    pygame.display.update()
