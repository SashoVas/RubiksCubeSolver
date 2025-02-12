from cube import Cube
import numpy as np
import pygame
from math import sin, cos
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


class VisualizationEngine:
    def __init__(self):
        self.color_dict = {0: WHITE, 1: YELLOW,
                           2: RED, 3: GREEN, 4: ORANGE, 5: BLUE}

        self.color_dict = {0: WHITE, 1: YELLOW,
                           2: RED, 3: GREEN, 4: ORANGE, 5: BLUE}
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.angle_x = 0.5
        self.angle_y = 0
        self.angle_z = 0
        self.cube = Cube()
        pygame.init()
        self.is_rotating = True
        self.is_pressed_key = False
        self.lastKey = None
        self.last_pressed_key = None
        self.current_pressed_key = None
        self.rotation_command = False
        self.commands_segment_selection = {
            'A': 'L', 'D': 'R', 'S': 'D', 'W': 'U'}
        self.commands_direction_selection = {'A': 'L', 'D': 'F'}

    def control_definition(self, event):

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.is_rotating = not self.is_rotating

        if event.type == pygame.KEYUP:
            self.is_pressed_key = False

        if (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT) or (self.is_pressed_key and self.lastKey == pygame.K_RIGHT):
            self.angle_y -= 0.03
            self.is_pressed_key = True
            self.lastKey = pygame.K_RIGHT

        if (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT) or (self.is_pressed_key and self.lastKey == pygame.K_LEFT):
            self.angle_y += 0.03
            self.is_pressed_key = True
            self.lastKey = pygame.K_LEFT

        if (event.type == pygame.KEYDOWN and event.key == pygame.K_UP) or (self.is_pressed_key and self.lastKey == pygame.K_UP):
            self.angle_x -= 0.03
            self.is_pressed_key = True
            self.lastKey = pygame.K_UP

        if (event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN) or (self.is_pressed_key and self.lastKey == pygame.K_DOWN):
            self.angle_x += 0.03
            self.is_pressed_key = True
            self.lastKey = pygame.K_DOWN

        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            self.last_pressed_key = self.current_pressed_key
            self.current_pressed_key = 'W'
            self.rotation_command = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            self.last_pressed_key = self.current_pressed_key
            self.current_pressed_key = 'A'
            self.rotation_command = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            self.last_pressed_key = self.current_pressed_key
            self.current_pressed_key = 'S'
            self.rotation_command = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            self.last_pressed_key = self.current_pressed_key
            self.current_pressed_key = 'D'
            self.rotation_command = True

    def game_loop(self):
        while True:
            self.clock.tick(60)

            for event in pygame.event.get()+[pygame.event.Event(0)]:
                self.control_definition(event)

            rotation_x = np.matrix([
                [1, 0, 0],
                [0, cos(self.angle_x), -sin(self.angle_x)],
                [0, sin(self.angle_x), cos(self.angle_x)],
            ]
            )
            rotation_y = np.matrix([
                [cos(self.angle_y), 0, sin(self.angle_y)],
                [0, 1, 0],
                [-sin(self.angle_y), 0, cos(self.angle_y)],
            ]
            )
            rotation_z = np.matrix([
                [cos(self.angle_z), -sin(self.angle_z), 0],
                [sin(self.angle_z), cos(self.angle_z), 0],
                [0, 0, 1],
            ]
            )
            if self.is_rotating:
                self.angle_y += 0.01
                # self.angle_x += 0.01
                # self.angle_z += 0.01
                pass
            self.screen.fill(GRAY)
            self.cube.cube.print_cube()
            self.cube.apply_transform([rotation_z, rotation_y, rotation_x])
            sides = self.cube.get_top_small_cubes()
            for side in sides:
                for position, color in side:
                    # position = [(x[1], x[0])for x in position]
                    pygame.draw.polygon(
                        self.screen, self.color_dict[color], position)
                    pygame.draw.polygon(self.screen, BLACK, position, width=1)
                # pygame.draw.polygon(screen, BLACK, side[0][0])
                # pygame.draw.polygon(screen, BLACK, side[1][0])
            selected_side = self.cube.get_top_sides()[0]
            p = selected_side.to_2d()
            temp = p[2]
            p[2] = p[3]
            p[3] = temp
            pygame.draw.polygon(
                self.screen, LIME, p, width=6)

            if self.rotation_command and self.last_pressed_key != None and self.current_pressed_key != None:

                self.cube.cube.turn(selected_side.color_num,
                                    self.commands_segment_selection[self.last_pressed_key],
                                    self.commands_direction_selection[self.current_pressed_key])

                self.last_pressed_key = None
                self.current_pressed_key = None
            self.rotation_command = False
            pygame.display.update()


if __name__ == '__main__':
    visualization_engine = VisualizationEngine()
    visualization_engine.game_loop()
