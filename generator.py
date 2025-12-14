from fillomino import Game
import random
from rich.console import Console

console = Console()

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

def get_generat_field():
    count_row = random.randint(2, 4)
    field = [[] for _ in range(count_row)]
    k = 0
    for count_col in range(1, count_row * 2, 2):
        for i in range(count_col):
            is_num = random.choice([True, False])
            if is_num:
                value = random.randint(1, 5)
                field[k].append(value)
            else:
                field[k].append(None)
        k+=1
    return field




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

gen_dick = {"lvl1_simple" : lvl1_simple,
        "lvl1_simple_2" : lvl1_simple_2,
        "lvl1_medium" : lvl1_medium,
        "lvl1_hard" : lvl1_hard,
        "lvl2_simple" : lvl2_simple,
        "lvl2_simple_2" : lvl2_simple_2,
        "lvl2_medium" : lvl2_medium,
        "lvl2_medium_2" : lvl2_medium_2}


def generate_puzzle(generator):
    random_game = random.choice(generator)
    print_solution(random_game, "Головоломки")


def print_solution(game_field, flag, name = None):
    g = Game(game_field)
    solution = g.solve(max_solutions=1)

    if flag:
        print(f"\n--- Головоломка {name} ---")
    else:
        print(f"\n--- Решение ---")
    if solution:
        if flag:
            Game.print_field_arr(game_field)
        else:
            Game.print_field_arr(solution[0])
    else:
        print("Решение не найдено.")

fil = get_generat_field()
print(fil)
print(print_solution(fil, False))


# if __name__ == "__main__":
#     list_fil = ["lvl1_simple",
#         "lvl1_simple_2",
#         "lvl1_medium",
#         "lvl1_hard",
#         "lvl2_simple",
#         "lvl2_simple_2",
#         "lvl2_medium",
#         "lvl2_medium_2"]
    
#     while True:
#         console.print("help - вывод команд")
#         comand = console.input("Введите команду: ")
#         if comand is None:
#             continue
#         cmd = comand.lower()
#         if cmd == "help":
#             console.print("all_fil - вывести все филомино")
#             console.print("name_field - выводит решение головоломки name_field")
            
#         elif cmd == "all_fil":
#             for puzzle in generator:
#                 for key, value in gen_dick.items():  
#                     if value == puzzle: 
#                         print_solution(puzzle, True, key)
                        
#         elif cmd in list_fil:
#             print_solution(gen_dick[cmd], False)
        
#         else:
#             console.print("хз не шарю чо за команда")
    