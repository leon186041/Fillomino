import copy

class Game:
    def __init__(self, field):
        self.game_field = copy.deepcopy(field)
        self.count_lines = len(self.game_field)
        self.limits = {} # Словарь для хранения {(i, j): limit_v}

        # Анализ поля: ИЗВЛЕЧЕНИЕ и УДАЛЕНИЕ строковых ограничений
        for i in range(self.count_lines):
            for j in range(len(self.game_field[i])):
                cell = self.game_field[i][j]
                if isinstance(cell, str) and cell.startswith('<'):
                    try:
                        limit_v = int(cell[1:])
                        self.limits[(i, j)] = limit_v # Сохраняем ограничение
                        self.game_field[i][j] = None # Заменяем на None для заполнения
                    except ValueError:
                        pass 

    # Топология соседей
    def get_neighbors(self, i, j):
        # Возвращает список 6 координат соседей для ячейки (код из вашего запроса)
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
        if visited is None:
            visited = set()
        value = self.game_field[i][j]
        # Для Fillomino группа собирается только по числовому значению.
        if not isinstance(value, int):
             return []
        
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

    # Валидация поля (МОДИФИЦИРОВАНО для Level 2)
    def check_valid(self):
        self.count_lines = len(self.game_field)
        field_complete = self.find_empty() is None
        visited = set()

        for i in range(self.count_lines):
            for j in range(len(self.game_field[i])):
                v = self.game_field[i][j]
                
                if v is None or (i, j) in visited:
                    continue
                
                group = self.collect_group(i, j, visited=visited) # Используем общий visited
                size = len(group)
                
                # 1. Обычные правила Fillomino: Размер <= V
                if size > v:
                    return False
                if field_complete and size != v:
                    return False
                
                # 2. Проверка ограничений Level 2: size < Limit
                for (x, y) in group:
                    # Если любая ячейка в группе имела ограничение <V
                    if (x, y) in self.limits:
                        limit_v = self.limits[(x, y)]
                        # Проверка: Размер должен быть строго меньше Limit
                        if size >= limit_v: 
                            return False 
                    
                    # 3. Проверка на несоприкосновение
                    for nx, ny in self.get_neighbors(x, y):
                        if (nx, ny) not in group:
                            neigh_val = self.game_field[nx][ny]
                            # Нельзя касаться другой группы с тем же значением
                            if neigh_val == v:
                                return False
        return True

    # Поиск пустой клетки
    def find_empty(self):
        for i in range(self.count_lines):
            for j in range(len(self.game_field[i])):
                if self.game_field[i][j] is None:
                    return (i, j)
        return None

    # Локальный анализ (МОДИФИЦИРОВАНО для Level 2)
    def possible_values_for_cell(self, i, j):
        max_size = (
            max(c for row in self.game_field for c in row if isinstance(c, int))
            if any(isinstance(c, int) for row in self.game_field for c in row)
            else 1
        )
        max_size = max(max_size, len(self.game_field[-1]))
        
        vals = set(range(1, max_size + 1))
        to_remove = set()

        all_relevant_limits = []
        
        # 1.1. Ограничение в самой ячейке (i, j)
        if (i, j) in self.limits:
            all_relevant_limits.append(self.limits[(i, j)])
            
        neighbor_group_roots = {}
        for nx, ny in self.get_neighbors(i, j):
             # 1.2. Ограничения в соседних ячейках
             if (nx, ny) in self.limits:
                 all_relevant_limits.append(self.limits[(nx, ny)])

             # 1.3. Сбор корней существующих групп
             if isinstance(self.game_field[nx][ny], int):
                comp = self.collect_group(nx, ny, visited=set())
                comp_key = tuple(sorted(comp))
                if comp_key not in neighbor_group_roots:
                    neighbor_group_roots[comp_key] = set(comp)

        for v in list(vals):
            total_size = 1 # Ячейка (i, j)
            
            # 2. Расчет размера потенциальной группы V
            for group_set in neighbor_group_roots.values():
                root_coords = list(group_set)[0]
                root_val = self.game_field[root_coords[0]][root_coords[1]]
                if root_val == v:
                    total_size += len(group_set)

            # 3. Проверка 1: Нарушение Fillomino (total_size > V)
            if total_size > v:
                to_remove.add(v)
                continue
            
            # 4. Проверка 2: Нарушение ограничения Level 2 (total_size >= Limit)
            for limit_v in all_relevant_limits:
                 if total_size >= limit_v:
                      to_remove.add(v)
                      break

        vals -= to_remove
        return vals

    # Выбрать клетку
    def find_best_cell(self):
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

                # Не используем check_valid здесь, чтобы не замедлять поиск. 
                # check_valid будет вызван только при полном заполнении поля.
                # Если же check_valid тут нужен для раннего отсева:
                # if self.check_valid(): 
                #    backtrack()
                # Но это сильно замедлит. Оставляем только проверку MRV в possible_values.
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
            r_str = [str(c) if c is not None else ' ' for c in r]
            print(" " * (max_len - len(r)) + str(r_str).replace("'", "").replace("[", "").replace("]", "").replace(",", " "))
        print("-" * 20)