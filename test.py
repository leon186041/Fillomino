def get_neighbors(line, number, game_field, count_lines):
    """найдем координаты всех соседей ячейки"""
    if number % 2 == 0:
        deltas = [(1, 1), (0, -1), (0, 1)]
    else:
        deltas = [(-1, -1), (0, -1), (0, 1)]

    neighbors = []
    for dline, dnum in deltas:
        new_line, new_num = line + dline, number + dnum
        if 0 <= new_line < count_lines and 0 <= new_num < len(game_field[new_line]):
            neighbors.append((new_line, new_num))
    return neighbors


def get_count_value(value, game_field, count_lines):
    """найдем колличество соседей у заданного значения"""
    visited = set()
    group_sizes = []

    def dfs(line, number):
        stack = [(line, number)]
        size = 0
        while stack:
            l, n = stack.pop()
            if (l, n) in visited:
                continue
            visited.add((l, n))
            size += 1
            for nl, nn in get_neighbors(l, n, game_field, count_lines):
                if game_field[nl][nn] == value and (nl, nn) not in visited:
                    stack.append((nl, nn))
        return size

    for line in range(count_lines):
        for number in range(len(game_field[line])):
            if game_field[line][number] == value and (line, number) not in visited:
                group_sizes.append(dfs(line, number))

    return group_sizes

game_field = [[None],
                [1, 2, 1],
                [3, None, None, None, 4],
                [5, 5, None, None, 5, None, None]]
count_lines = len(game_field)

print(get_count_value(2, game_field, count_lines))
