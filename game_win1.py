import copy
from rich.console import Console
from rich.text import Text

console = Console()

class Game:
    def __init__(self):
        self.game_field = self.get_isi_field()
        self.clean_field = copy.deepcopy(self.game_field)
        self.count_lines = len(self.game_field)
        self.color_map  = {
                            1: "#49251E",
                            2: "#FFEDE3",
                            3: "#FA4E00",
                            4: "#CBE7F7",
                            5: "#CC5500",
                            6: "#59362E",
                            7: "#C2E0F2",
                            8: "#FFDDEE",
                            9: "#FFF0DE",
                            }

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

        if self.game_field[line][number]:
            console.print('[red]тут занято![/red]')
            return

        self.game_field[line][number] = value

    def clear_progress(self):
         self.game_field = copy.deepcopy(self.clean_field)

    def solve(self):
        """Рекурсивно ищем решение Филломино и выводим результат"""
        cell = self.find_empty_cell()
        if not cell:
            console.print(self.game_field)
            return True

        line, number = cell

        for value in range(1, 10):
            self.game_field[line][number] = value

            if self.check_valid():
                if self.solve():
                    return True
            self.game_field[line][number] = None

        return False


    def get_groups(self, value):
        visited = set()
        groups = []

        def dfs(line, number):
            stack = [(line, number)]
            size = []
            while stack:
                l, n = stack.pop()
                if (l, n) in visited:
                    continue
                visited.add((l, n))
                size.append((l,n))
                for nl, nn in self.get_neighbors(l, n):
                    if self.game_field[nl][nn] == value and (nl, nn) not in visited:
                        stack.append((nl, nn))
            return size

        for line in range(self.count_lines):
            for number in range(len(self.game_field[line])):
                if self.game_field[line][number] == value and (line, number) not in visited:
                    groups.append(dfs(line, number))

        return groups

    def find_empty_cell(self):
        for line in range(self.count_lines):
            for number in range(len(self.game_field[line])):
                if self.game_field[line][number] is None:
                    return (line, number)
        return None

    def check_valid(self):
        for value in range(1, 10):
            count_neighbors = self.get_count_value(value)
            if count_neighbors and max(count_neighbors) > value:
                return False
        # if not self.no_same_touch():
        #     return False
        return True

    def check_progress(self):
        all_right = True
        for value in range(1, 10):
            count_neighbors = self.get_count_value(value)
            if count_neighbors and max(count_neighbors) > value:
                console.print(f"что-то многовато {value}, не думаешь?")
                all_right = False
        if all_right:
            console.print('все чотко, молодец !')


    def format_cell(self, value):
        if value is None:
            return Text(".", style="dim")
        color = self.color_map.get(value, "white")
        return Text(str(value), style=color)


    def get_correct_line(self, line_field):
        result_line = Text("/")
        for i in range(len(line_field)):
            result_line.append(self.format_cell(line_field[i]))
            if i % 2 == 0:
                result_line.append("\\")
            else:
                result_line.append("/")
        return result_line

    def render_field(self):
        count_item = len(self.game_field)
        count_tab = count_item * 2 - 2
        for i in range(count_item):
            current_line = self.get_correct_line(self.game_field[i])
            prefix = Text(" " * count_tab)
            prefix.append(current_line)
            console.print(prefix)
            count_tab -= 2

    def print_help_commands(self):
        console.print(""
        "- set v a b - вставляет значение v в ячейку с координатами a - номер линии, b - номер столбца\n"
        "- check - проверяет правильность поля\n"
        "- next - переходим на некст уровень\n"
        "- help - выводит все возможные команды\n"
        "- exit - заканчиваем играть\n")

if __name__ == "__main__":
    g = Game()
    g.render_field()