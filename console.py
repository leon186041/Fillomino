
from game_win1 import Game
from rich.console import Console
from rich.text import Text

console = Console()

def main():
    g = Game()
    g.render_field()
    console.print('"help" выводит все возможные команды\n')

    while True:
        comand_line = console.input("Введите команду: ")
        comand = comand_line.strip().split()
        if comand is None:
            continue

        cmd = comand[0].lower()
        if cmd == "help":
            g.print_help_commands()
        elif cmd == "exit":
            break
        elif cmd == "set":
            if len(comand) != 4:
                console.print("[red]чет много")
                continue
            value = int(comand[1])
            num_line = int(comand[2]) - 1
            num_col = int(comand[3]) - 1
            g.write_value_in_field(num_line, num_col, value)
            g.render_field()
        elif cmd == "check":
            g.check_progress()
        elif cmd == "next":
            continue
        else:
            console.print("[red]неизвестная команда, попробуй еще раз[/red]")
        


if __name__ == "__main__":
    main()