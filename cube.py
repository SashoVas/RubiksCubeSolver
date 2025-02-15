import numpy as np
from random import randint
WIDTH = 800
HEIGHT = 600
SCALE = 150
CUBE_CENTER_WIDTH = int(WIDTH/2)
CUBE_CENTER_HEIGHT = int(HEIGHT/2)
SEGMENTS_ORDER = ['R', 'U',  'L', 'D']

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
COLORS = [BLUE, GREEN, YELLOW, WHITE, ORANGE, RED]
COLORS_NUMS = [5, 3, 1, 0, 4, 2]
color_dict = {0: WHITE, 1: YELLOW, 2: RED, 3: GREEN, 4: ORANGE, 5: BLUE}
YELLOW_NUM = 1
WHITE_NUM = 0
# (Side_color,segment_to_turn)-(new_color,times_to_turn)// translating every move so that only right turns are used
MOVE_TRANSLATIONS = {
    (0, 'U'): (4, 3),
    (0, 'D'): (2, 1),
    (0, 'R'): (5, 1),
    (0, 'L'): (3, 3),

    (1, 'U'): (2, 3),
    (1, 'D'): (4, 1),
    (1, 'R'): (5, 1),
    (1, 'L'): (3, 3),

    (2, 'U'): (0, 3),
    (2, 'D'): (1, 1),
    (2, 'R'): (5, 1),
    (2, 'L'): (3, 3),

    (3, 'U'): (0, 3),
    (3, 'D'): (1, 1),
    (3, 'R'): (2, 1),
    (3, 'L'): (4, 3),

    (4, 'U'): (0, 3),
    (4, 'D'): (1, 1),
    (4, 'R'): (3, 1),
    (4, 'L'): (5, 3),

    (5, 'U'): (0, 3),
    (5, 'D'): (1, 1),
    (5, 'R'): (4, 1),
    (5, 'L'): (2, 3),
}
YELLOW_NEIGHBORS = {'L': 6, 'R': 3, 'U': 2, 'D': 4}
WHITE = {'L': 3, 'R': 6, 'U': 4, 'D': 2}
NORMAL_COLORS = [2, 5, 4, 3]


class Side:

    def __init__(self, up_left, down_left, up_right, down_right, color, color_num):
        self.up_left = up_left.reshape((3, 1))
        self.down_left = down_left.reshape((3, 1))
        self.up_right = up_right.reshape((3, 1))
        self.down_right = down_right.reshape((3, 1))
        self.points = [self.up_left, self.down_left,
                       self.up_right, self.down_right]

        self.projection_matrix = np.matrix([
            [1, 0, 0],
            [0, 1, 0]
        ])
        self.color = color
        self.color_num = color_num

    def apply_transform(self, transformations):
        self.up_left_transformed = self.up_left
        self.down_left_transformed = self.down_left
        self.up_right_transformed = self.up_right
        self.down_right_transformed = self.down_right

        for transform in transformations:
            self.up_left_transformed = np.dot(
                transform, self.up_left_transformed)
            self.down_left_transformed = np.dot(
                transform, self.down_left_transformed)
            self.up_right_transformed = np.dot(
                transform, self.up_right_transformed)
            self.down_right_transformed = np.dot(
                transform, self.down_right_transformed)

        self.transformed_points = [self.up_left_transformed, self.down_left_transformed,
                                   self.up_right_transformed, self.down_right_transformed]

    def calculate_projection(self, points):
        res = []
        for point in points:
            projection = np.dot(self.projection_matrix, point)

            x = int(projection[0][0]*SCALE+CUBE_CENTER_WIDTH)
            y = int(projection[1][0]*SCALE+CUBE_CENTER_HEIGHT)

            res.append([x, y])
        return res

    def to_2d(self):
        return self.calculate_projection(self.transformed_points)

    def avg_depth(self):
        return np.mean([point[2] for point in self.transformed_points])

    def transform_list_of_points(self, transformed_edges):
        return [self.calculate_projection(points) for points in transformed_edges]

    def get_small_cubes_edge_points(self):
        # calculate every vertex of every cubbie on the side
        edge_points = [[self.transformed_points[0], (self.transformed_points[0]*2+self.transformed_points[1])/3, (self.transformed_points[0]+self.transformed_points[1]*2)/3, self.transformed_points[1]],
                       [self.transformed_points[1], (
                           self.transformed_points[1]*2+self.transformed_points[2])/3, (self.transformed_points[1]+self.transformed_points[2]*2)/3, self.transformed_points[2]],
                       [self.transformed_points[2], (
                           self.transformed_points[2]*2+self.transformed_points[3])/3, (self.transformed_points[2]+self.transformed_points[3]*2)/3, self.transformed_points[3]],
                       [self.transformed_points[3], (self.transformed_points[3]*2+self.transformed_points[0])/3, (self.transformed_points[3]+self.transformed_points[0]*2)/3, self.transformed_points[0]],]

        top_to_bottom_points = [edge_points[0], [], [], edge_points[2]]
        left_to_right_points = [edge_points[1], [], [], edge_points[3]]

        for pointA, pointB in zip(edge_points[0], edge_points[2]):
            top_to_bottom_points[1].append((pointA*2+pointB)/3)
            top_to_bottom_points[2].append((pointA+pointB*2)/3)

        for pointA, pointB in zip(edge_points[1], edge_points[3]):
            left_to_right_points[1].append((pointA*2+pointB)/3)
            left_to_right_points[2].append((pointA+pointB*2)/3)

        top_to_bottom_points_transformed = self.transform_list_of_points(
            top_to_bottom_points)
        left_to_right_points_transformed = self.transform_list_of_points(
            left_to_right_points)
        return (top_to_bottom_points_transformed, left_to_right_points_transformed)

    def get_small_cubes_polygon(self):
        # getting the list of points that represent every cubbie of the side. Later this is used to visualize the side with different colors
        top_to_bottom_points, left_to_right_points = self.get_small_cubes_edge_points()
        result = [[], [], []]
        for i in range(0, 3):
            for j in range(1, 4):
                up_left = top_to_bottom_points[i][j-1]
                up_right = top_to_bottom_points[i][j]
                down_left = top_to_bottom_points[i+1][j-1]
                down_right = top_to_bottom_points[i+1][j]
                result[i].append((up_left, up_right, down_right, down_left))

        return result

    def get_edge_points(self):
        # List with every point of the vertex of the cube
        transformed_edges = [[self.transformed_points[0], (self.transformed_points[0]+self.transformed_points[1]*2)/3, (self.transformed_points[0]*2+self.transformed_points[1])/3, self.transformed_points[1]],
                             [self.transformed_points[1], (self.transformed_points[1]+self.transformed_points[2]*2)/3, (
                                 self.transformed_points[1]*2+self.transformed_points[2])/3, self.transformed_points[2]],
                             [self.transformed_points[2], (self.transformed_points[2]+self.transformed_points[3]*2)/3, (
                                 self.transformed_points[2]*2+self.transformed_points[3])/3, self.transformed_points[3]],
                             [self.transformed_points[3], (self.transformed_points[3]+self.transformed_points[0]*2)/3, (self.transformed_points[3]*2+self.transformed_points[0])/3, self.transformed_points[0]],]

        return self.transform_list_of_points(transformed_edges)


class Cube:
    def __init__(self):
        self.sides = []
        # The coordinates of every vertex of the cube in the 3d plane
        sides_cord = [
            [[-1,  -1,  1], [-1, 1,  1], [-1,  -1, -1], [-1, 1, -1],
             ],  # Left (-X) face
            [[1, -1, -1],
             [1,  1, -1], [1, -1,  1], [1,  1,  1], ],  # Right (+X) face
            [[1,  1,  1], [1,  1, -1], [-1,  1,  1], [-1,  1, -1],
             ],  # Bottom (+Y) face
            [[1, -1, -1],   [1, -1,  1], [-1, -1, -1], [-1, -1,  1],
             ],  # Top (-Y) face
            [[-1,  -1, -1], [-1, 1, -1], [1, -1, -1], [1,  1, -1],
             ],  # Back (-Z) face
            [[1,  -1,  1],
             [1, 1,  1], [-1, -1,  1], [-1,  1,  1],]   # Front (+Z) face
        ]
        for side, color, color_num in zip(sides_cord, COLORS, COLORS_NUMS):
            self.sides.append(Side(
                np.array(side[0]),
                np.array(side[1]),
                np.array(side[2]),
                np.array(side[3]), color, color_num))
        self.cube = TrueCube()

    def get_all_points(self):
        res = []
        for side in self.sides:
            res.append(side.up_left)
            res.append(side.down_left)
            res.append(side.up_right)
            res.append(side.down_right)

        return res

    def apply_transform(self, transformations):
        for side in self.sides:
            side.apply_transform(transformations)

    def to_2d(self):
        res = []
        for side in self.sides:
            res += side.to_2d()
        return res

    def get_top_sides(self):
        self.sides.sort(key=lambda x: x.avg_depth())
        return self.sides[0:3]

    def get_top_small_cubes(self):
        # Gets every cubbie, from the sides that are shown to the screen
        top_sides = self.get_top_sides()
        result = []
        for side in top_sides:
            polygons = side.get_small_cubes_polygon()
            colors = self.cube.sides[side.color_num]

            side_polygons = []

            for i in range(0, 3):
                for j in range(0, 3):
                    side_polygons.append((polygons[i][j], colors[j][i]))
                    # side_polygons.append((polygons[i][j], colors[i][j]))
            result.append(side_polygons)

        return result

    def turn(self, color, segment, direction, angle):

        if color == YELLOW_NUM or color == WHITE_NUM:
            # so that the visualization perspective is aligned with the logic perspective the angle is incremented
            angle += 1.6
            new_segment_position = SEGMENTS_ORDER.index(
                segment)+int(angle/0.8) % len(SEGMENTS_ORDER)
            if color == YELLOW_NUM:
                new_segment_position = (
                    new_segment_position+2) % len(SEGMENTS_ORDER)
                # keeping the perspective correct
                if direction == 'F':
                    direction = 'B'
                elif direction == 'B':
                    direction = 'F'
            segment = SEGMENTS_ORDER[new_segment_position]
        self.cube.turn(color, segment, direction)

    def scramble(self):
        self.cube.scramble()


# 0-white
# 1-yellow
# 2-red
# 3-green
# 4-orange
# 5-blue
# the adjacent colors to white and yellow,(position)-color
YELLOW_NEIGHBORS = {(1, 0): 6, (1, 2): 3, (0, 1): 2, (2, 1): 4}
WHITE_NEIGHBORS = {(1, 0): 3, (1, 2): 6, (0, 1): 4, (2, 1): 2}
NORMAL_COLORS_NEIGHBORS = [2, 5, 4, 3]


class TrueCube:

    def __init__(self, sides=None):
        if sides is None:
            self.sides = [[[i]*3, [i]*3, [i]*3] for i in range(0, 6)]
        else:
            self.sides = sides

    def get_sides(self):
        return self.sides

    def set_sides(self, sides):
        self.sides = []
        for side in sides:
            rows = []
            for row in side:
                rows.append(row.copy())
            self.sides.append(rows)

    def scramble(self):
        moves = []
        for _ in range(20):
            side_to_move = randint(0, 5)
            segment = SEGMENTS_ORDER[randint(0, 3)]
            direction = ['F', 'B'][randint(0, 1)]
            moves.append((side_to_move, segment, direction))

        self.last_scramble = moves
        for side_to_move, segment, direction in moves:
            self.turn(side_to_move, segment, direction)

    def print_cube(self):
        for side in self.sides:
            for row in side:
                print(row)
            print('==========')

    def paste_arr(self, arr, side, row, col, rev=False):
        before = []
        if row != -1 and col == -1:
            before = self.sides[side][row].copy()
            if rev is False:
                self.sides[side][row] = arr
            else:
                self.sides[side][row] = arr[::-1]
        if row == -1 and col != -1:
            before = [
                self.sides[side][0][col],
                self.sides[side][1][col],
                self.sides[side][2][col],
            ]
            if not rev:
                self.sides[side][0][col] = arr[0]
                self.sides[side][1][col] = arr[1]
                self.sides[side][2][col] = arr[2]
            else:
                self.sides[side][0][col] = arr[2]
                self.sides[side][1][col] = arr[1]
                self.sides[side][2][col] = arr[0]

        return before

    def extract_first_side(self, side, row, col):
        if row != -1 and col == -1:
            return self.sides[side][row].copy()

        if row == -1 and col != -1:
            return [
                self.sides[side][0][col],
                self.sides[side][1][col],
                self.sides[side][2][col],
            ]

        return None

    def rotate_face(self, color):
        row1 = self.sides[color][0].copy()
        row2 = self.sides[color][1].copy()
        row3 = self.sides[color][2].copy()

        self.paste_arr([row1[0], row1[1], row1[2]], color, -1, 2)
        self.paste_arr([row1[2], row2[2], row3[2]], color, 2, -1, True)
        self.paste_arr([row3[0], row3[1], row3[2]], color, -1, 0)
        self.paste_arr([row1[0], row2[0], row3[0]], color,  0, -1, True)

    def right_turn(self, color):
        pos_dict = {0: [(2, 0, -1, False), (3, 0, -1, False), (4, 0, -1, False), (5, 0, -1, False)],
                    1: [(2, 2, -1, False), (5, 2, -1, False), (4, 2, -1, False), (3, 2, -1, False)],
                    2: [(1, 0, -1, False), (3, -1, 2, True), (0, 2, -1, False), (5, -1, 0, True)],
                    3: [(0, -1, 0, False), (2, -1, 0, False), (1, -1, 0, True), (4, -1, 2, True)],
                    4: [(0, 0, -1, True), (3, -1, 0, False), (1, 2, -1, True), (5, -1, 2, False)],
                    5: [(0, -1, 2, True), (4, -1, 0, True), (1, -1, 2, False), (2, -1, 2, False)]
                    }
        info = pos_dict[color]
        self.rotate_face(color)
        row = self.extract_first_side(info[0][0], info[0][1], info[0][2])
        for i in range(1, 4):
            row = self.paste_arr(
                row, info[i][0], info[i][1], info[i][2], rev=info[i-1][3])
        row = self.paste_arr(
            row, info[0][0], info[0][1], info[0][2], rev=info[3][3])

    def translate_to_rights(self, color, segment, direction):
        if segment != 'F':
            new_color, times = MOVE_TRANSLATIONS[(color, segment)]
        else:
            new_color, times = color, 1
        if direction == 'B':
            times = 1 if times == 3 else 3
        return (new_color, times)

    def turn(self, color, segment, direction):

        new_color, times = self.translate_to_rights(color, segment, direction)
        for _ in range(0, times):
            self.right_turn(new_color)

 # 0-white
# 1-yellow
# 2-red
# 3-green
# 4-orange
# 5-blue


if __name__ == '__main__':
    cube = TrueCube()
    cube.scramble()
