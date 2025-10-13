import rich
from rich.console import Console

console = Console()

class Game:
    def __init__(self):
        self.game_field = self.get_isi_field()
        self.clean_field = self.game_field
        self.count_lines = len(self.game_field)

    def get_isi_field(self):
        return [[None],
                [1, 2, 1],
                [3, None, None, None, 4],
                [5, None, None, None, 5, None, None]]

    def get_neighbors(self, line, number):
        """найдем координаты всех соседей ячейки"""
        if number % 2 == 0:
            deltas = [(1, 1), (0, -1), (0, 1)]
        else:
            deltas = [(-1, -1), (0, -1), (0, 1)]

        neighbors = []
        for dline, dnum in deltas:
            new_line, new_num = line + dline, number + dnum
            if 0 <= new_line < self.count_lines and 0 <= new_num < len(self.game_field[new_line]):
                neighbors.append((new_line, new_num))
        return neighbors


    def get_count_value(self, value):
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
                for nl, nn in self.get_neighbors(l, n):
                    if self.game_field[nl][nn] == value and (nl, nn) not in visited:
                        stack.append((nl, nn))
            return size

        for line in range(self.count_lines):
            for number in range(len(self.game_field[line])):
                if self.game_field[line][number] == value and (line, number) not in visited:
                    group_sizes.append(dfs(line, number))

        return group_sizes


    def write_value_in_field(self, line, number, value):
        """ ну тут проверочка на корректность значений line, number и value """
        if line >= self.count_lines or line < 0 or number >= len(self.game_field[line]) or number < 0:
            console.print('[red]ты не правильно ввел координаты, снайпер[/red]')
            return

        if value not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            console.print('[red]сюда можно только крутым, то есть цифрам от 1 до 9[/red]')
            return

        if value > 9 or value < 0:
            console.print('[red]ограничься в своих желаниях, значение выходит за допустимые рамки[/red]')
            return

        self.game_field[line][number] = value

    def clear_progress(self):
        self.game_field = self.clean_field

    def check_progress(self):
        all_right = True
        for value in range(1, 10):
            count_neighbors = self.get_count_value(value)
            if count_neighbors and max(count_neighbors) > value:
                console.print(f"что-то многовато {value}, не думаешь?")
                all_right = False
        if all_right:
            console.print('все чотко, молодец !')

# game = Game()
# game.write_value_in_field(0, 0, 2)
# print(game.game_field)
# print(game.check_progress())