from game import Game
import rich
from rich.console import Console


console = Console()

def get_correct_line(line_field):
    """из [3, 5, 5, 5, 4] в /3\\5/5\\5/4\\"""
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


def render_field(field):
    count_item = len(field)
    count_tab = count_item*2 - 2
    for i in range(count_item):
        current_line = get_correct_line(field[i])
        console.print(" "*(count_tab) + current_line)
        count_tab -= 2



test_field = [[None],
                [1, 2, 1],
                [3, None, None, None, 4],
                [5, None, None, None, 5, None, None]]
game = Game()
render_field(test_field)


