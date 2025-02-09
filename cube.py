import numpy as np
WIDTH = 800
HEIGHT = 600
SCALE = 150
CUBE_CENTER_WIDTH = int(WIDTH/2)
CUBE_CENTER_HEIGHT = int(HEIGHT/2)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
COLORS = [BLUE, GREEN, YELLOW, WHITE, RED, ORANGE]
COLORS_NUMS = [5, 3, 1, 0, 2, 4]
color_dict = {0: WHITE, 1: YELLOW, 2: RED, 3: GREEN, 4: ORANGE, 5: BLUE}

MOVE_TRANSLATIONS = {
    (0, 'T'): (4, 3),
    (0, 'B'): (2, 1),
    (0, 'R'): (5, 1),
    (0, 'L'): (3, 3),

    (1, 'T'): (2, 3),
    (1, 'B'): (4, 1),
    (1, 'R'): (5, 1),
    (1, 'L'): (3, 3),

    (2, 'T'): (0, 3),
    (2, 'B'): (1, 1),
    (2, 'R'): (5, 1),
    (2, 'L'): (3, 3),

    (3, 'T'): (0, 3),
    (3, 'B'): (1, 1),
    (3, 'R'): (2, 1),
    (3, 'L'): (4, 3),

    (4, 'T'): (0, 3),
    (4, 'B'): (1, 1),
    (4, 'R'): (3, 1),
    (4, 'L'): (5, 3),

    (5, 'T'): (0, 3),
    (5, 'B'): (1, 1),
    (5, 'R'): (4, 1),
    (5, 'L'): (2, 3),
}


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

    def to_2d(self):
        res = []
        for point in self.transformed_points:
            projection = np.dot(self.projection_matrix, point)

            x = int(projection[0][0]*SCALE+CUBE_CENTER_WIDTH)
            y = int(projection[1][0]*SCALE+CUBE_CENTER_HEIGHT)
            res.append([x, y])
        return res

    def avg_depth(self):
        return np.mean([point[2] for point in self.transformed_points])

    def transform_list_of_points(self, transformed_edges):
        res = []
        for points in transformed_edges:
            res1 = []
            for point in points:
                projection = np.dot(self.projection_matrix, point)

                x = int(projection[0][0]*SCALE+CUBE_CENTER_WIDTH)
                y = int(projection[1][0]*SCALE+CUBE_CENTER_HEIGHT)
                res1.append([x, y])
            res.append(res1)
        return res

    def get_small_cubes_edge_points(self):

        edge_points = [[self.transformed_points[0], (self.transformed_points[0]*2+self.transformed_points[1])/3, (self.transformed_points[0]+self.transformed_points[1]*2)/3, self.transformed_points[1]],
                       [self.transformed_points[1], (
                           self.transformed_points[1]*2+self.transformed_points[2])/3, (self.transformed_points[1]+self.transformed_points[2]*2)/3, self.transformed_points[2]],
                       [self.transformed_points[2], (
                           self.transformed_points[2]*2+self.transformed_points[3])/3, (self.transformed_points[2]+self.transformed_points[3]*2)/3, self.transformed_points[3]],
                       [self.transformed_points[3], (self.transformed_points[3]*2+self.transformed_points[0])/3, (self.transformed_points[3]+self.transformed_points[0]*2)/3, self.transformed_points[0]],]

        top_to_bottom_points = [edge_points[0], [], [], edge_points[2][::-1]]
        left_to_right_points = [edge_points[1], [], [], edge_points[3][::-1]]

        for pointA, pointB in zip(edge_points[0], edge_points[2][::-1]):
            top_to_bottom_points[1].append((pointA*2+pointB)/3)
            top_to_bottom_points[2].append((pointA+pointB*2)/3)

        for pointA, pointB in zip(edge_points[1], edge_points[3][::-1]):
            left_to_right_points[1].append((pointA*2+pointB)/3)
            left_to_right_points[2].append((pointA+pointB*2)/3)

        top_to_bottom_points_transformed = self.transform_list_of_points(
            top_to_bottom_points)
        left_to_right_points_transformed = self.transform_list_of_points(
            left_to_right_points)
        return (top_to_bottom_points_transformed, left_to_right_points_transformed)

    def get_small_cubes_polygon(self):
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
        sides_cord = [
            [[-1, -1, -1], [-1, -1,  1], [-1,  1,  1],
                [-1,  1, -1]],  # Left (-X) face
            [[1, -1, -1], [1, -1,  1], [1,  1,  1],
                [1,  1, -1]],  # Right (+X) face
            [[-1, -1, -1], [-1, -1,  1], [1, -1,  1],
                [1, -1, -1]],  # Bottom (-Y) face
            [[-1,  1, -1], [-1,  1,  1], [1,  1,  1],
                [1,  1, -1]],  # Top (+Y) face
            [[-1, -1, -1], [-1,  1, -1], [1,  1, -1],
                [1, -1, -1]],  # Back (-Z) face
            [[-1, -1,  1], [-1,  1,  1], [1,  1,  1],
                [1, -1,  1]]   # Front (+Z) face
        ]
        for side, color, color_num in zip(sides_cord, COLORS, COLORS_NUMS):
            self.sides.append(Side(
                np.array(side[0]),
                np.array(side[1]),
                np.array(side[2]),
                np.array(side[3]), color, color_num))
        self.cube = TrueCube()
        self.cube.turn(2, 'R', 'F')

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
        top_sides = self.get_top_sides()
        result = []
        for side in top_sides:
            polygons = side.get_small_cubes_polygon()
            face = []
            for row1, row2 in zip(polygons, self.cube.sides[side.color_num]):
                res_row = []
                for position, color in zip(row1, row2):
                    res_row.append((position, color))
                face.append(res_row)
            result.append(face)
        return result


# 0-white
# 1-yellow
# 2-red
# 3-green
# 4-orange
# 5-blue


class TrueCube:
    def __init__(self):
        self.sides = [[[i]*3, [i]*3, [i]*3] for i in range(0, 6)]

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

        self.paste_arr(row1, color, -1, 2)
        self.paste_arr([row1[2], row2[2], row3[2]], color, 2, -1, True)
        self.paste_arr(row3, color, -1, 0)
        self.paste_arr([row1[0], row2[0], row3[0]], color,  0, -1, True)

    def right_turn(self, color):
        pos_dict = {0: [(2, 0, -1), (3, 0, -1), (4, 0, -1), (5, 0, -1)],
                    1: [(2, 2, -1), (5, 2, -1), (4, 2, -1), (3, 2, -1)],
                    2: [(1, 0, -1), (3, -1, 2), (0, 2, -1), (5, -1, 0)],
                    3: [(0, -1, 0), (2, -1, 0), (1, -1, 0), (4, -1, 2)],
                    4: [(0, 0, -1), (3, -1, 0), (1, 2, -1), (5, -1, 2)],
                    5: [(0, -1, 2), (4, -1, 0), (1, -1, 2), (2, -1, 2)]
                    }
        info = pos_dict[color]
        self.rotate_face(color)
        row = self.extract_first_side(info[0][0], info[0][1], info[0][2])
        for i in range(1, 4):
            row = self.paste_arr(
                row, info[i][0], info[i][1], info[i][2], rev=i == 3 and color != 0 and color != 1)
        row = self.paste_arr(row, info[0][0], info[0][1], info[0][2])

    def turn(self, color, segment, direction):

        if segment != 'F':
            new_color, times = MOVE_TRANSLATIONS[(color, segment)]
        else:
            new_color, times = color, 1
        if direction == 'L':
            times = 1 if times == 3 else 3
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
    cube.turn(0, 'T', 'L')
    cube.print_cube()
