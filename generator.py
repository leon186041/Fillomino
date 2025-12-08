from fillomino import Game

lvl1_simple = [
    [1], 
    [3, None, None]
]

lvl1_simple_2 = [
    [None], 
    [1, None, None]
]

lvl1_medium = [
    [1], 
    [2, None, None], 
    [1, None, None, None, None]
]

lvl1_hard = [
    [1],
    [2, None, None],
    [None, None, None, None, None],
    [None, None, 3, None, None, None, 1],
]

lvl2_simple = [
    [None], 
    [None, None, "<4"]
]

lvl2_simple_2 = [
    ["<3"], 
    [None, None, None]
]

lvl2_medium = [
    ["<4"], 
    [None, "<3", None], 
    [None, None, None, None, None]
]

lvl2_medium_2 = [
    ["<3"],
    [None, None, 4],
    [None, "<5", None, None, "<2"]
]

generator = [
    lvl1_simple,
    lvl1_simple_2,
    lvl1_medium,
    lvl1_hard,
    lvl2_simple,
    lvl2_simple_2,
    lvl2_medium,
    lvl2_medium_2,
]


def generate_puzzle(generator):
    for i, puzzle in enumerate(generator):
        print_solution(puzzle, f"Головоломка #{i+1}")


def print_solution(game_field, name_puzzle):
    g = Game(game_field)
    solution = g.solve(max_solutions=1)

    print(f"\n--- Решение {name_puzzle} ---")
    if solution:
        Game.print_field_arr(solution[0])
    else:
        print("Решение не найдено.")


if __name__ == "__main__":
    generate_puzzle(generator)
