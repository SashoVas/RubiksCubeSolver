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
    # Representation of a side in a cube. This class is tasked with managing the perspective changes and transformations of a side in the cube.

    def __init__(self, up_left, down_left, up_right, down_right, color, color_num):
        # Initializes a side

        # Parameters:
        #    up_left ([x,y,z]):The coordinates of the top left point of the side.
        #    down_left ([x,y,z]):The coordinates of the down left point of the side.
        #    up_right ([x,y,z]):The coordinates of the top right point of the side.
        #    down_right ([x,y,z]):The coordinates of the down right point of the side.
        #    color ([r,g,b]):The rgb value of the color, in the middle square.
        #    color_num (int):The color number.

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
        # Applies a transformation that changes the perspective of the side.
        # The function multiplies the matrix and the vertices of the sides,
        # which changes the perspective of the points in 3d

        # Parameters:
        #    transformations (3x3 np.matrix): Matrix that is used to change the perspective of the points on the side.

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
        # Projects 3d point, to 2d plain

        # Parameters:
        #    points (list([x,y,z])]):The points to be projected.

        # Returns:
        #    res(list([x,y])):The points in 2d.
        res = []
        for point in points:
            projection = np.dot(self.projection_matrix, point)

            x = int(projection[0][0]*SCALE+CUBE_CENTER_WIDTH)
            y = int(projection[1][0]*SCALE+CUBE_CENTER_HEIGHT)

            res.append([x, y])
        return res

    def to_2d(self):
        # Transforms the vertices of the sides to 2d
        return self.calculate_projection(self.transformed_points)

    def avg_depth(self):
        # Returns the average depth of the side
        return np.mean([point[2] for point in self.transformed_points])

    def transform_list_of_points(self, transformed_edges):
        return [self.calculate_projection(points) for points in transformed_edges]

    def get_small_cubes_edge_points(self):
        # Calculate every vertex of every cubby on the side

        # Returns:
        #    res(list(list([x,y,z]))):Returns a list of points for every line of the side.
        # The points are evenly spaced, where every point is a vertex of a small cubby

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
        # Getting the list of points that represent every cubby of the side. Later this is used to visualize the side with different colors

        # Returns:
        #    res(list(list([4*point]))):Returns a list with every polygon on the side,
        #    that represents different square of the cube.
        #    Each polygon is represented by 4 points.
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
        # Gets outer points of the side, and returns the in 2d.

        transformed_edges = [[self.transformed_points[0], (self.transformed_points[0]+self.transformed_points[1]*2)/3, (self.transformed_points[0]*2+self.transformed_points[1])/3, self.transformed_points[1]],
                             [self.transformed_points[1], (self.transformed_points[1]+self.transformed_points[2]*2)/3, (
                                 self.transformed_points[1]*2+self.transformed_points[2])/3, self.transformed_points[2]],
                             [self.transformed_points[2], (self.transformed_points[2]+self.transformed_points[3]*2)/3, (
                                 self.transformed_points[2]*2+self.transformed_points[3])/3, self.transformed_points[3]],
                             [self.transformed_points[3], (self.transformed_points[3]+self.transformed_points[0]*2)/3, (self.transformed_points[3]*2+self.transformed_points[0])/3, self.transformed_points[0]],]

        return self.transform_list_of_points(transformed_edges)


class Cube:
    def __init__(self):
        # Represents the cube, and handles its transformations
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
        # Gets the point of every side

        # Returns:
        #    res(list(points)):The points f every side.
        res = []
        for side in self.sides:
            res.append(side.up_left)
            res.append(side.down_left)
            res.append(side.up_right)
            res.append(side.down_right)

        return res

    def apply_transform(self, transformations):
        # Applies a transformation to every side of the cube
        for side in self.sides:
            side.apply_transform(transformations)

    def to_2d(self):
        # Returns every side in 2d
        res = []
        for side in self.sides:
            res += side.to_2d()
        return res

    def get_top_sides(self):
        # Returns the most outer side, that will be visible when visualizing
        self.sides.sort(key=lambda x: x.avg_depth())
        return self.sides[0:3]

    def get_top_small_cubes(self):
        # Gets every cubby, from the sides that will be shown on the screen

        # Returns:
        #    result(list(list(polygon))): Every polygon of the three other sides of the cube.
        top_sides = self.get_top_sides()
        result = []
        for side in top_sides:
            polygons = side.get_small_cubes_polygon()
            colors = self.cube.sides[side.color_num]

            side_polygons = []

            for i in range(0, 3):
                for j in range(0, 3):
                    side_polygons.append((polygons[i][j], colors[j][i]))
            result.append(side_polygons)

        return result

    def turn(self, color, segment, direction, angle):
        # Turns the cube in specific direction

        # Parameters:
        #    color (int)]):The color of the middle square of the side to be turned. Used to determine which side to turn.
        #    segment(U,D,L,R): The segment of the side to turn. Up, Down, Left or Right
        #    direction(F,B): The direction of the turn. Front or back

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
        # Scrambles the cube
        self.cube.scramble()

    def bbs_to_side(self, side):
        bb_color_to_side_color = {
            0: 5, 1: 3, 2: 4, 3: 2, 4: 0, 5: 1}
        flatten = [bb_color_to_side_color[bb.class_id] for bb in side]
        return [flatten[:3], flatten[3:6], flatten[6:]]

    def load_from_bounding_boxes(self, sides):
        self.cube = TrueCube([self.bbs_to_side(sides['white']),
                             self.bbs_to_side(sides['yellow']),
                             self.bbs_to_side(sides['red']),
                             self.bbs_to_side(sides['green']),
                             self.bbs_to_side(sides['orange']),
                             self.bbs_to_side(sides['blue'])])


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
    # The logical representation of the cube

    def __init__(self, sides=None):
        # Initializes a cube

        # Parameters:
        #    sides (3x3 matrix)]): A predefined cube
        if sides is None:
            self.sides = [[[i]*3, [i]*3, [i]*3] for i in range(0, 6)]
        else:
            self.sides = sides

    def get_sides(self):
        # Returns the sides of the cube
        return self.sides

    def set_sides(self, sides):
        # Sets the sides of a cube. The function creates a deep copy of the sides,
        # which is important, when searching for optimal solution.
        self.sides = []
        for side in sides:
            rows = []
            for row in side:
                rows.append(row.copy())
            self.sides.append(rows)

    def scramble(self):
        # Scrambles the cube
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
        # Prints the cube
        for side in self.sides:
            for row in side:
                print(row)
            print('==========')

    def paste_arr(self, arr, side, row, col, rev=False):
        # Places one array in the place of another

        # Result:
        # before(list):The arr before the new one was placed.
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
        # Extracting the fist side, when executing the algorithm for turning a side

        # Returns:
        # res(list): a list with the colors of the side
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
        # It handles the rotation of the colors on the face of the side that is turned.
        row1 = self.sides[color][0].copy()
        row2 = self.sides[color][1].copy()
        row3 = self.sides[color][2].copy()

        self.paste_arr([row1[0], row1[1], row1[2]], color, -1, 2)
        self.paste_arr([row1[2], row2[2], row3[2]], color, 2, -1, True)
        self.paste_arr([row3[0], row3[1], row3[2]], color, -1, 0)
        self.paste_arr([row1[0], row2[0], row3[0]], color,  0, -1, True)

    def right_turn(self, color):
        # Turns the cube in the right direction from the front of the side
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
        # Translates a move, so that it only uses front right turns

        # Result:
        # res(new_color,times):The new color to be turned front right, and how many times to turn it
        if segment != 'F':
            new_color, times = MOVE_TRANSLATIONS[(color, segment)]
        else:
            new_color, times = color, 1
        if direction == 'B':
            times = 1 if times == 3 else 3
        return (new_color, times)

    def turn(self, color, segment, direction):
        # Turns a side segment of the cube in specific direction
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
