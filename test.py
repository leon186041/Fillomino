# def get_neighbors(line, number, game_field, count_lines):
#     """найдем координаты всех соседей ячейки"""
#     if number % 2 == 0:
#         deltas = [(1, 1), (0, -1), (0, 1)]
#     else:
#         deltas = [(-1, -1), (0, -1), (0, 1)]

#     neighbors = []
#     for dline, dnum in deltas:
#         new_line, new_num = line + dline, number + dnum
#         if 0 <= new_line < count_lines and 0 <= new_num < len(game_field[new_line]):
#             neighbors.append((new_line, new_num))
#     return neighbors


# def get_count_value(value, game_field, count_lines):
#     visited = set()
#     groups = []

#     def dfs(line, number):
#         stack = [(line, number)]
#         size = []
#         while stack:
#             l, n = stack.pop()
#             if (l, n) in visited:
#                 continue
#             visited.add((l, n))
#             size.append((l,n))
#             for nl, nn in get_neighbors(l, n, game_field, count_lines):
#                 if game_field[nl][nn] == value and (nl, nn) not in visited:
#                     stack.append((nl, nn))
#         return size

#     for line in range(count_lines):
#         for number in range(len(game_field[line])):
#             if game_field[line][number] == value and (line, number) not in visited:
#                 groups.append(dfs(line, number))

#     return groups
# def no_same_touch(game_field, count_lines):
#         """Проверяем, что разные регионы с одинаковыми числами не касаются по сторонам"""
#         for line in range(count_lines):
#             for number in range(len(game_field[line])):
#                 value = game_field[line][number]
#                 if value is None:
#                     continue

#                 for nl, nn in get_neighbors(line, number, game_field, count_lines):
#                     neighbor_value = game_field[nl][nn]
#                     if neighbor_value is None:
#                         continue

#                     if neighbor_value == value:
#                         groups = get_count_value(value, game_field, count_lines)
#                         if len(groups) > 1:
#                             found_same_group = any(
#                                 (line, number) in group and (nl, nn) in group
#                                 for group in groups
#                             )
#                             if not found_same_group:
#                                 return False
#         return True

game_field = [[None],
                [1, 2, 1],
                [3, 5, 5, 5, 4],
                [5, 5, 5, 5, 5, 5, 5]]
# count_lines = len(game_field)
# print(no_same_touch(game_field, count_lines))
# print(get_count_value(5, game_field, count_lines))
def get_correct_line(line_field):
    result_line = "/"
    for i in range(len(line_field)):
        if line_field[i] is None:
            current_item = "."
        else:
            current_item = str(line_field[i])
        
        if i % 2 == 0:
            result_line += f"{current_item}\\"
        else:
            result_line += f"{current_item}/"

    return result_line

print(get_correct_line(game_field[2]))
