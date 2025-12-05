import copy


class Game:
    def __init__(self, field):
        self.game_field = copy.deepcopy(field)
        self.count_lines = len(self.game_field)

    # Топология соседей
    def get_neighbors(self, i, j):
        # Возвращает список 6 координат соседей для ячейки
        neighbors = []
        if i < 0 or i >= self.count_lines or j < 0 or j >= len(self.game_field[i]):
            return neighbors
        L = len(self.game_field[i])

        if j - 1 >= 0:
            neighbors.append((i, j - 1))
        if j + 1 < L:
            neighbors.append((i, j + 1))

        if i - 1 >= 0:
            up_len = len(self.game_field[i - 1])
            jj_ul = j - 2
            if 0 <= jj_ul < up_len:
                neighbors.append((i - 1, jj_ul))
            jj_ur = j - 1
            if 0 <= jj_ur < up_len:
                neighbors.append((i - 1, jj_ur))

        if i + 1 < self.count_lines:
            down_len = len(self.game_field[i + 1])
            jj_dl = j + 1
            if 0 <= jj_dl < down_len:
                neighbors.append((i + 1, jj_dl))
            jj_dr = j + 2
            if 0 <= jj_dr < down_len:
                neighbors.append((i + 1, jj_dr))

        return neighbors

    # Собрать одну компоненту
    def collect_group(self, i, j, visited=None):
        # Собирает все связанные ячейки с одинаковым значением в одну группу (BFS)
        if visited is None:
            visited = set()
        value = self.game_field[i][j]
        queue = [(i, j)]
        visited.add((i, j))
        group = []
        while queue:
            x, y = queue.pop(0)
            group.append((x, y))
            for nx, ny in self.get_neighbors(x, y):
                if self.game_field[nx][ny] == value and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        return group

    # Валидация поля
    def check_valid(self):
        """
        Проверяет поле на соответствие правилам Fillomino:
        1. Размер полиомино не превышает его значение (v).
        2. В полном поле размер точно равен v.
        3. Разные полиомино с одинаковым v не касаются по стороне.
        """
        self.count_lines = len(self.game_field)
        field_complete = all(c is not None for row in self.game_field for c in row)
        # Используем внешний visited для отслеживания обработанных групп
        visited = set()
        for i in range(self.count_lines):
            for j in range(len(self.game_field[i])):
                v = self.game_field[i][j]
                if v is None or (i, j) in visited:
                    continue
                # Собираем группу, используя локальный visited для предотвращения зацикливания
                local_visited = set()
                group = self.collect_group(i, j, visited=local_visited)
                # Добавляем ячейки в общий visited после сбора
                visited.update(group)
                size = len(group)
                # 2. Ограничение размера
                if size > v:
                    return False
                if field_complete and size != v:
                    return False
                # 3. Проверка на несоприкосновение
                for (x, y) in group:
                    for nx, ny in self.get_neighbors(x, y):
                        if (nx, ny) not in group:
                            neigh_val = self.game_field[nx][ny]
                            # Если сосед имеет то же значение V, но не принадлежит группе
                            if neigh_val == v:
                                return False

        return True

    # Поиск пустой клетки
    def find_empty(self):
        # Возвращает координаты первой пустой клетки или None, если поле заполнено
        for i in range(self.count_lines):
            for j in range(len(self.game_field[i])):
                if self.game_field[i][j] is None:
                    return (i, j)
        return None

    # Локальный анализ
    def possible_values_for_cell(self, i, j):
        """
        Вычисляет множество возможных значений для пустой ячейки (i,j)
        на основе локального правила превышения размера полиомино.
        """
        max_size = (
            max(c for row in self.game_field for c in row if c is not None)
            if any(c is not None for row in self.game_field for c in row)
            else 1
        )
        max_size = max(max_size, len(self.game_field[-1]))

        vals = set(range(1, max_size + 1))
        to_remove = set()

        neighbor_group_roots = {}
        for nx, ny in self.get_neighbors(i, j):
            neigh_val = self.game_field[nx][ny]
            if neigh_val is None:
                continue

            comp = self.collect_group(nx, ny, visited=set())
            comp_key = tuple(sorted(comp))

            if comp_key not in neighbor_group_roots:
                neighbor_group_roots[comp_key] = set(comp)

        for v in list(vals):
            total_size = 1

            for group_set in neighbor_group_roots.values():
                root_coords = list(group_set)[0]
                root_val = self.game_field[root_coords[0]][root_coords[1]]

                if root_val == v:
                    total_size += len(group_set)

            if total_size > v:
                to_remove.add(v)

        vals -= to_remove
        return vals

    # Выбрать клетку
    def find_best_cell(self):
        """
        Находит пустую ячейку с наименьшим доменом возможных значений (MRV)
        для повышения эффективности бэктрекинга.
        """
        best = None
        best_domain = set()
        min_domain_size = float("inf")

        for i in range(self.count_lines):
            for j in range(len(self.game_field[i])):
                if self.game_field[i][j] is not None:
                    continue

                dom = self.possible_values_for_cell(i, j)

                if not dom:
                    return (i, j, set())

                if best is None or len(dom) < min_domain_size:
                    min_domain_size = len(dom)
                    best = (i, j)
                    best_domain = dom

        if best is None:
            return (None, None, set())
        return (best[0], best[1], best_domain)

    # Решение
    def solve(self, max_solutions=1000, debug=False):
        # Решает головоломку методом бэктрекинга с использованием эвристики MRV
        self.count_lines = len(self.game_field)
        solutions = []
        steps = 0

        def backtrack():
            nonlocal steps
            if len(solutions) >= max_solutions:
                return

            i, j, domain = self.find_best_cell()

            if i is None:
                if self.check_valid():
                    solutions.append(copy.deepcopy(self.game_field))
                return

            if not domain:
                return

            for v in sorted(domain):
                steps += 1
                self.game_field[i][j] = v

                if self.check_valid():
                    backtrack()

                self.game_field[i][j] = None

                if len(solutions) >= max_solutions:
                    break

        backtrack()
        if debug:
            print(f"Завершено. Шагов: {steps}, решений: {len(solutions)}")
        return solutions

    # Вспомогательная: печать решения
    @staticmethod
    def print_field_arr(field):
        max_len = len(field[-1])
        for r in field:
            print(" " * (max_len - len(r)) + str(r))
        print("-" * 20)
