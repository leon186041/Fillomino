from game_win1 import Game

game_field = [[None], [1, 2, 1], [3, 5, 5, 5, 4], [5, 5, 5, 5, 5, 5, 5]]


def is_solution_correct(game_field):
    g = Game(game_field)
    g.count_lines = len(game_field)
    # 1. Проверяем валидность правил Fillomino
    is_valid = g.check_valid()
    # 2. Проверяем, что нет пустых клеток (т.е., поле полностью заполнено)
    is_complete = g.find_empty() is None

    return is_valid and is_complete


def test_field(game_field, n):
    if n == 0:
        return None
    g = Game(game_field)
    print("Начальное поле корректно?", g.check_valid())
    # Ищем n решений, чтобы проверить, что они все верны
    solutions = g.solve(max_solutions=n, debug=True)
    print(f"\nНайдено решений: {len(solutions)}")
    for i, sol in enumerate(solutions):
        print(f"--- Решение {i+1} ---")
        Game.print_field_arr(sol)
        # Выводим финальный вердикт
        correct_status = "Корректно" if is_solution_correct(sol) else "НЕКОРРЕКТНО"
        print(f"Финальная проверка: {correct_status}\n")


game_field = [[1], [None, None, None], [None, None, None, None, None]]
test_field(game_field, 10)
