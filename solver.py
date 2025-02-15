from cube import TrueCube


def is_solved(sides, *to_check):
    for color, i, j in to_check:
        if sides[color][i][j] != color:
            return False
    return True


def check_white_orange(sides):
    return is_solved(sides, (0, 0, 1), (4, 0, 1))


def check_white_red(sides):
    return is_solved(sides, (0, 2, 1), (2, 0, 1)) and check_white_orange(sides)


def check_white_green(sides):
    return is_solved(sides, (0, 1, 0), (3, 0, 1)) and check_white_red(sides)


def check_white_blue(sides):
    return is_solved(sides, (0, 1, 2), (5, 0, 1)) and check_white_green(sides)


def check_white_orange_blue_edge(sides):
    return is_solved(sides, (0, 0, 2), (5, 0, 2), (4, 0, 0)) and check_white_blue(sides)


def check_white_orange_green_edge(sides):
    return is_solved(sides, (0, 0, 0), (3, 0, 0), (4, 0, 2)) and check_white_orange_blue_edge(sides)


def check_white_red_blue_edge(sides):
    return is_solved(sides, (0, 2, 2), (2, 0, 2), (5, 0, 0)) and check_white_orange_green_edge(sides)


def check_white_red_green_edge(sides):
    return is_solved(sides, (0, 2, 0), (2, 0, 0), (3, 0, 2)) and check_white_red_blue_edge(sides)


def check_orange_green_edge(sides):
    return is_solved(sides, (4, 1, 2), (3, 1, 0)) and check_white_red_green_edge(sides)


def check_orange_blue_edge(sides):
    return is_solved(sides, (4, 1, 0), (5, 1, 2)) and check_orange_green_edge(sides)


def check_red_green_edge(sides):
    return is_solved(sides, (2, 1, 0), (3, 1, 2)) and check_orange_blue_edge(sides)


def check_red_blue_edge(sides):
    return is_solved(sides, (2, 1, 2), (5, 1, 0)) and check_red_green_edge(sides)


def check_yellow_cross(sides):
    return is_solved(sides, (1, 2, 1), (1, 1, 2), (1, 1, 0), (1, 0, 1)) and check_red_blue_edge(sides)


def check_partial_bottom_row(sides):
    return check_yellow_cross(sides) and \
        ((sides[3][2][1] == 3 and sides[4][2][1] == 4) or
         (sides[5][2][1] == 5 and sides[2][2][1] == 2) or
         (sides[2][2][1] == 2 and sides[3][2][1] == 3) or
         (sides[4][2][1] == 4 and sides[5][2][1] == 5))


def check_bottom_row(sides):
    return is_solved(sides, (3, 2, 1), (4, 2, 1), (5, 2, 1), (2, 2, 1)) and check_partial_bottom_row(sides)


def check_orient_of_two_consecutive_edges(sides):
    orange_green_colors = [sides[4][2][2], sides[3][2][0], sides[1][2][0]]
    orange_blue_colors = [sides[4][2][0], sides[5][2][2], sides[1][2][2]]
    red_blue_colors = [sides[2][2][2], sides[5][2][0], sides[1][0][2]]
    red_green_colors = [sides[2][2][0], sides[3][2][2], sides[1][0][0]]

    orange_green = 4 in orange_green_colors and 3 in orange_green_colors
    orange_blue = 4 in orange_blue_colors and 5 in orange_blue_colors
    red_blue = 2 in red_blue_colors and 5 in red_blue_colors
    red_green = 2 in red_green_colors and 3 in red_green_colors
    return check_bottom_row(sides) and ((orange_green and orange_blue) or (orange_blue and red_blue) or (orange_green and red_green) or (red_blue and red_green))


def check_orient_of_all_yellow_edges(sides):
    orange_green_colors = [sides[4][2][2], sides[3][2][0], sides[1][2][0]]
    orange_blue_colors = [sides[4][2][0], sides[5][2][2], sides[1][2][2]]
    red_blue_colors = [sides[2][2][2], sides[5][2][0], sides[1][0][2]]
    red_green_colors = [sides[2][2][0], sides[3][2][2], sides[1][0][0]]

    orange_green = 4 in orange_green_colors and 3 in orange_green_colors
    orange_blue = 4 in orange_blue_colors and 5 in orange_blue_colors
    red_blue = 2 in red_blue_colors and 5 in red_blue_colors
    red_green = 2 in red_green_colors and 3 in red_green_colors
    return check_bottom_row(sides) and orange_green and orange_blue and red_blue and red_green


def check_two_solved_bottom_edges(sides):
    return check_orient_of_all_yellow_edges(sides) and \
        ((sides[2][2][2] == 2 and sides[2][2][0] == 2) or
         (sides[3][2][2] == 3 and sides[3][2][0] == 3) or
         (sides[4][2][2] == 4 and sides[4][2][0] == 4) or
         (sides[5][2][2] == 5 and sides[5][2][0] == 5))


def check_solved(sides):
    return is_solved(sides, (2, 2, 2), (2, 2, 0), (3, 2, 2), (3, 2, 0), (4, 2, 2), (4, 2, 0), (5, 2, 2), (5, 2, 0)) and check_two_solved_bottom_edges(sides)


def find_path(sides, validation_func, moves):
    if validation_func(sides):
        return TrueCube(sides), []

    processed_moves = [(color, comp_moves.split(' '))
                       for color, comp_moves in moves]
    dummy_cube = TrueCube()
    queue = [(sides, [])]
    while True:
        curr_sides, solving_steps = queue.pop(0)
        for color, comp_moves in processed_moves:

            dummy_cube.set_sides(curr_sides)
            for move in comp_moves:
                dummy_cube.turn(color, move, 'F')
            if validation_func(dummy_cube.get_sides()):
                return dummy_cube, solving_steps+[(color, comp_moves)]
            queue.append((dummy_cube.get_sides(), solving_steps +
                         [(color, comp_moves)]))


def get_unique_moves():
    dummy_cube = TrueCube()
    segments = ['U', 'D', 'L', 'R']
    all_moves = []
    for color in range(2, 6):
        for segment in segments:
            all_moves.append((color, segment))
    unique_moves_translation = set()
    unique_moves = []
    for color, segment in all_moves:
        new_color, times = dummy_cube.translate_to_rights(
            color, segment, 'F')
        if (new_color, times) not in unique_moves_translation:
            unique_moves_translation.add((new_color, times))
            unique_moves.append((color, segment))
    return unique_moves


def get_needed_moves(moves, faces):
    res = []
    for move in moves:
        for face in faces:
            res.append((face, move))
    return res


def solve_white(cube):
    solution = []
    all_moves = get_unique_moves()
    solving_order = [check_white_red,
                     check_white_green,
                     check_white_blue]
    moves = ['F F', 'D R F F F R R R',
             'L D L L L',
             'R D D D R R R', 'R D R R R', 'L D D D L L L']
    needed_moves = get_needed_moves(moves, range(2, 6)) + all_moves

    new_cube, solution_new = find_path(
        cube.get_sides(), check_white_orange, needed_moves)
    solution = solution + solution_new
    for func in solving_order:
        new_cube, solution_new = find_path(
            new_cube.get_sides(), func, needed_moves)
        solution = solution + solution_new
    moves = ['R R R D D D R D', 'F D F F F D D D',
             'R R R D D R D R R R D D D R']

    needed_moves = get_needed_moves(moves, range(
        2, 6)) + [(2, 'D'), (2, 'D D'), (2, 'D D D')]  # + all_moves
    solving_order = [check_white_orange_blue_edge, check_white_orange_green_edge,
                     check_white_red_blue_edge, check_white_red_green_edge]

    for func in solving_order:
        new_cube, solution_new = find_path(
            new_cube.get_sides(), func, needed_moves)
        solution = solution + solution_new
    return new_cube, solution


def solve_second_row(new_cube, solution):

    moves = ['R R R D R D F D D D F F F',
             'L L L D D D L D D D F F F D F']
    needed_moves = get_needed_moves(moves, range(
        2, 6)) + [(2, 'D'), (2, 'D D'), (2, 'D D D')]
    solving_order = [check_orange_green_edge, check_orange_blue_edge,
                     check_red_green_edge, check_red_blue_edge]

    for func in solving_order:
        new_cube, solution_new = find_path(
            new_cube.get_sides(), func, needed_moves)
        solution = solution + solution_new
    return new_cube, solution


def solve_yellow(new_cube, solution):

    moves = [
        'R L F R R R L L L D R L F R R R L L L D R L F R R R L L L D']  # , 'R L F R R R L L L D R L F R R R L L L D R L F R R R L L L D R L F R R R L L L D R L F R R R L L L D R L F R R R L L L D']
    needed_moves = get_needed_moves(moves, range(2, 6))
    new_cube, solution_new = find_path(
        new_cube.get_sides(), check_yellow_cross, needed_moves)
    solution = solution + solution_new

    moves = ['R R R D D R D R R R D R D']
    needed_moves = get_needed_moves(moves, range(
        2, 6)) + [(2, 'D'), (2, 'D D'), (2, 'D D D')]
    solving_order = [check_partial_bottom_row, check_bottom_row]
    for func in solving_order:
        new_cube, solution_new = find_path(
            new_cube.get_sides(), func, needed_moves)

        solution = solution + solution_new

    moves = ['R R R D L L L D D D R D L',
             'R R R D L L L D D D R D L R R R D L L L D D D R D L',
             'R R R D L L L D D D R D L R R R D L L L D D D R D L R R R D L L L D D D R D L']
    needed_moves = get_needed_moves(moves, range(2, 6))
    solving_order = [check_orient_of_two_consecutive_edges,
                     check_orient_of_all_yellow_edges]

    for func in solving_order:
        new_cube, solution_new = find_path(
            new_cube.get_sides(), func, needed_moves)

        solution = solution + solution_new
    return new_cube, solution


def solve_last_row(new_cube, solution):
    moves = ['R R R D D R D R R R D R L L L D D L D D D L L L D D D',
             'R R R D D R D R R R D R L L L D D L D D D L L L D D D R R R D D R D R R R D R L L L D D L D D D L L L D D D',
             'R R R D D R D R R R D R L L L D D L D D D L L L D D D R R R D D R D R R R D R L L L D D L D D D L L L D D D R R R D D R D R R R D R L L L D D L D D D L L L D D D',
             'R R R D D R D R R R D R L L L D D L D D D L L L D D D R R R D D R D R R R D R L L L D D L D D D L L L D D D R R R D D R D R R R D R L L L D D L D D D L L L D D D R R R D D R D R R R D R L L L D D L D D D L L L D D D']
    needed_moves = get_needed_moves(moves, range(2, 6))
    solving_order = [check_two_solved_bottom_edges, check_solved]

    for func in solving_order:
        new_cube, solution_new = find_path(
            new_cube.get_sides(), func, needed_moves)
        solution = solution + solution_new
    return new_cube, solution


def solve(cube):
    new_cube, solution = solve_white(cube)
    new_cube, solution = solve_second_row(new_cube, solution)
    new_cube, solution = solve_yellow(new_cube, solution)
    new_cube, solution = solve_last_row(new_cube, solution)
    solution = [(color, move) for color, moves in solution for move in moves]
    processed_solution = []
    while len(solution) >= 1:
        current_move = solution.pop(0)
        if len(solution) > 1 and solution[0] == current_move and solution[1] == current_move:
            solution.pop(0)
            solution.pop(0)
            processed_solution.append(
                (current_move[0], current_move[1], 'B', 1))
            continue
        if len(solution) > 1 and solution[0] == current_move:
            solution.pop(0)
            processed_solution.append(
                (current_move[0], current_move[1], 'F', 2))
            continue

        processed_solution.append((current_move[0], current_move[1], 'F', 1))
    print('Moves:', len(processed_solution))

    return new_cube, processed_solution


if __name__ == '__main__':
    cube = TrueCube()
    for i in range(10):
        cube.scramble()
        new_cube, solution = solve(cube)
    # new_cube.print_cube()
