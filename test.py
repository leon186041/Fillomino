from fillomino import Game
import unittest


def is_solution_correct(game_field):
    g = Game(game_field)
    g.count_lines = len(game_field)
    is_valid = g.check_valid()
    is_complete = g.find_empty() is None

    return is_valid and is_complete


class TestFillomino(unittest.TestCase):
    def _test_solver(self, initial_field, expected_min_solutions=1):
        g = Game(initial_field)
        if any(c is not None for row in initial_field for c in row):
            self.assertTrue(g.check_valid(), "Начальное поле должно быть валидным.")
        solutions = g.solve(max_solutions=expected_min_solutions, debug=True)
        self.assertGreaterEqual(
            len(solutions),
            expected_min_solutions,
            f"Ожидалось минимум {expected_min_solutions} решений, найдено {len(solutions)}.",
        )
        for sol in solutions:
            self.assertTrue(
                is_solution_correct(sol),
                f"Найдено некорректное решение:\n{Game.print_field_arr(sol)}",
            )

        return solutions

    def test_check_valid_size(self):
        # Проверка: Размер группы > значения
        field_invalid_size = [[1], [1, 5, 5], [5, 1, 5, 5, 5]]
        g = Game(field_invalid_size)
        self.assertFalse(g.check_valid())

    def test_check_valid_contact(self):
        # Проверка: Две группы одного значения касаются
        field_invalid_contact = [[2], [5, 5, 2], [5, 5, 5, 5, 5]]
        g = Game(field_invalid_contact)
        self.assertFalse(g.check_valid())

    def test_simple_fill(self):
        field = [[1], [None, None, None], [None, None, None, None, None]]
        self._test_solver(field, expected_min_solutions=1)

    def test_no_contact_rule_solution(self):
        # Два 2 на расстоянии, но могут быть легко соединены неправильным заполнением.
        field = [[2], [None, None, None], [2, None, None, None, None]]
        self._test_solver(field, expected_min_solutions=1)

    def test_complex_unique_solution(self):
        # Проверка: Сложный случай
        field = [[None], [3, None, None], [1, None, None, 2, None]]
        self._test_solver(field, expected_min_solutions=1)

    def test_multiple_solutions(self):
        # Проверка: Поиск нескольких решений для пустого поля
        field = [[None], [None, None, None], [None, None, None, None, None]]
        self._test_solver(field, expected_min_solutions=5)


if __name__ == "__main__":
    unittest.main()
