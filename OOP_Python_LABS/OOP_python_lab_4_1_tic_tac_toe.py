from accessify import private, protected
from typing import Literal, Callable
import turtle
from colorama import Fore, Back, Style
import json
import datetime
from random import randint


class Cross():
    """
    Class for cross from tic-tac-toe, and also it plays role of base class in the game.
    """
    def __init__(self, color: Literal["yellow", "green", "blue", "red", "black"], size: Literal["small", "medium", "large"]):
        if self.validate_params(color, size):
            self._size = size
            self._color = color

    @staticmethod
    def validate_params(color: str, size: str) -> bool | ValueError:
        allowed_colors = {"yellow", "green", "blue", "red", "black"}
        allowed_sizes = {"small", "medium", "large"}
        if color in allowed_colors and size in allowed_sizes: return True
        elif color in allowed_colors and size not in allowed_sizes: raise ValueError("incorrect size were inputted")
        elif color not in allowed_colors and size in allowed_sizes: raise ValueError("incorrect color were inputted")
        else: raise ValueError("incorrect color and size were inputted")

    @staticmethod
    def translate_size(size):
        return {"small": (5, 1), "medium": (12, 3), "large": (20, 6)}[size]

    @staticmethod
    def translate_color(color):
        return {"yellow": Fore.YELLOW, "green": Fore.GREEN, "blue": Fore.BLUE, "red": Fore.RED, "black": Fore.BLACK}[color]

    @staticmethod
    def translate_back(color):
        return {"yellow": Back.YELLOW, "green": Back.GREEN, "blue": Back.BLUE, "red": Back.RED, "black": Back.BLACK}[color]

    def cell_lines(self, bg: str) -> list[str]:
        c = self.translate_color(self._color)
        r = Style.RESET_ALL
        match self._size:
            case "small":
                return [bg + " " + c + "x" + r + bg + " " + r]
            case "medium":
                return [bg + "  " + c + "X" + r + bg + "  " + r,
                        bg + "  " + c + "X" + r + bg + "  " + r]
            case "large":
                return [bg + "   " + c + "X   X" + r + bg + "   " + r,
                        bg + "   " + c + "  X  " + r + bg + "   " + r,
                        bg + "   " + c + "X   X" + r + bg + "   " + r]

    def display_yourself(self, x, y):
        t = turtle.Turtle()
        t.hideturtle()
        t.speed(0)
        tpl_size = self.translate_size(self._size)
        val = tpl_size[0]
        t.width(tpl_size[1])
        t.pencolor(self._color)
        t.penup()
        t.goto(x - val, y - val)
        t.pendown()
        t.goto(x + val, y + val)
        t.penup()
        t.goto(x - val, y + val)
        t.pendown()
        t.goto(x + val, y - val)
        t.penup()

    def __str__(self):
        c = self.translate_color(self._color)
        r = Style.RESET_ALL
        match self._size:
            case "small":  return c + "x" + r
            case "medium": return c + "X" + r
            case "large":  return c + "X   X\n  X  \nX   X" + r


class Nought(Cross):
    """
    Class for nought from tic-tac-toe, inherited from class "Cross"
    """

    def cell_lines(self, bg: str) -> list[str]:
        c = self.translate_color(self._color)
        r = Style.RESET_ALL
        match self._size:
            case "small":
                return [bg + " " + c + "o" + r + bg + " " + r]
            case "medium":
                return [bg + "  " + c + "O" + r + bg + "  " + r,
                        bg + "  " + c + "O" + r + bg + "  " + r]
            case "large":
                return [bg + "   " + c + " O O " + r + bg + "   " + r,
                        bg + "   " + c + "O   O" + r + bg + "   " + r,
                        bg + "   " + c + " O O " + r + bg + "   " + r]

    def display_yourself(self, x, y):
        t = turtle.Turtle()
        t.hideturtle()
        t.speed(0)
        tpl_size = super().translate_size(self._size)
        radius = tpl_size[0]
        t.width(tpl_size[1])
        t.pencolor(self._color)
        t.penup()
        t.setheading(0)
        t.goto(x, y - radius)
        t.pendown()
        t.circle(radius, steps=100)
        t.penup()

    def __str__(self):
        c = self.translate_color(self._color)
        r = Style.RESET_ALL
        match self._size:
            case "small":  return c + "o" + r
            case "medium": return c + "O" + r
            case "large":  return c + " O O \nO   O\n O O " + r


class Board(Cross):
    def __init__(self, board_color: Literal["yellow", "green", "blue", "red", "black"], lines_color: Literal["yellow", "green", "blue", "red", "black"], size: Literal["small", "medium", "large"]):
        super().__init__(board_color, size)
        try:
            self.translate_color(lines_color)
        except KeyError:
            raise ValueError('incorrect "lines_color" were inputed')
        else:
            self._lines_color = lines_color
            self._grid = [["" for i in range(3)] for j in range(3)]

    def match_size(self) -> int:
        return {"small": 1, "medium": 2, "large": 4}[self._size]

    def match_cell_size(self) -> int:
        return {"small": 30, "medium": 75, "large": 150}[self._size]

    def _empty_lines(self, piece_size: str, bg: str) -> list[str]:
        r = Style.RESET_ALL
        match piece_size:
            case "small":  return [bg + "   " + r]
            case "medium": return [bg + "     " + r, bg + "     " + r]
            case "large":  return [bg + "           " + r,
                                   bg + "           " + r,
                                   bg + "           " + r]

    def _get_piece_size(self) -> str:
        for row in self._grid:
            for cell in row:
                if cell != "":
                    return cell._size
        return self._size  # дефолт поки дошка порожня

    def __str__(self) -> str:
        bg = self.translate_back(self._color)
        lc = self.translate_color(self._lines_color)
        r = Style.RESET_ALL
        piece_size = self._get_piece_size()

        match self._size:
            case "small":  sep_dash = "---"
            case "medium": sep_dash = "-----"
            case "large":  sep_dash = "-----------"

        pipe = bg + lc + "|" + r
        sep_row = bg + lc + f"{sep_dash}+{sep_dash}+{sep_dash}" + r

        result = ""
        for i, row in enumerate(self._grid):
            all_lines = []
            for cell in row:
                if cell == "":
                    all_lines.append(self._empty_lines(piece_size, bg))
                else:
                    all_lines.append(cell.cell_lines(bg))

            num_lines = max(len(l) for l in all_lines)
            for cl in all_lines:
                while len(cl) < num_lines:
                    cl.append(self._empty_lines(piece_size, bg)[0])

            for line_idx in range(num_lines):
                parts = [all_lines[col][line_idx] for col in range(3)]
                result += pipe.join(parts) + "\n"

            if i < 2:
                result += sep_row + "\n"

        return result

    def display_board(self, regim: Literal["graphic", "text"], center_x: float | int, center_y: float | int):
        match regim:
            case "text":
                print(self)
            case "graphic":
                screen = turtle.Screen()
                screen.tracer(0)
                screen.clearscreen()
                screen.tracer(0)
                screen.bgcolor(self._color)

                pen = turtle.Turtle()
                pen.hideturtle()
                pen.speed(0)
                pen.pencolor(self._lines_color)
                pen.width(2)

                cell_size = self.match_cell_size()

                for i in [-1, 1]:
                    pen.penup()
                    pen.goto(center_x + i * cell_size / 2, center_y - cell_size * 1.5)
                    pen.pendown()
                    pen.goto(center_x + i * cell_size / 2, center_y + cell_size * 1.5)
                    pen.penup()
                    pen.goto(center_x - cell_size * 1.5, center_y + i * cell_size / 2)
                    pen.pendown()
                    pen.goto(center_x + cell_size * 1.5, center_y + i * cell_size / 2)
                    pen.penup()

                for ind_row, row in enumerate(self._grid):
                    for ind_col, elem in enumerate(row):
                        x = center_x + (ind_col - 1) * cell_size
                        y = center_y + (ind_row - 1) * cell_size
                        if type(elem) in (Cross, Nought):
                            elem.display_yourself(x, y)

                screen.update()

    def check_board(self) -> None | Literal["draw", "X", "O"]:
        won_lst = []

        for group in self._grid:
            if all(type(elem) is Cross for elem in group): won_lst.append("X")
            if all(type(elem) is Nought for elem in group): won_lst.append("O")

        for group in zip(*self._grid):
            if all(type(elem) is Cross for elem in group): won_lst.append("X")
            if all(type(elem) is Nought for elem in group): won_lst.append("O")

        diag1 = [self._grid[i][i] for i in range(3)]
        diag2 = [self._grid[i][2 - i] for i in range(3)]
        for diag in (diag1, diag2):
            if all(type(elem) is Cross for elem in diag): won_lst.append("X")
            if all(type(elem) is Nought for elem in diag): won_lst.append("O")

        if won_lst:
            return won_lst[0]

        if all(cell != "" for row in self._grid for cell in row):
            return "draw"

        return None


class Player():
    def __init__(self, login, password):
        self._login = login
        self._password = password


class StatisticsDB():
    def __init__(self, path: str):
        self._file_path = path

    def json_load_dict(self) -> dict:
        with open(self._file_path, "r", encoding="utf-8") as j_file:
            return json.load(j_file)

    def json_upload_dict(self, work_dict: dict) -> None:
        with open(self._file_path, "w", encoding="utf-8") as j_file:
            json.dump(work_dict, j_file, indent=4)

    def wrapper_print(self, number_of_pleyers: int, sort_func: Callable, position_in_game_info: int) -> None:
        if not isinstance(number_of_pleyers, int): raise ValueError('"number_of_pleyers" value must be int type')
        full_res_lst = []
        for user in self.json_load_dict():
            temp_res_lst = [info[position_in_game_info] for info in user["games_information"]]
            value = sort_func(temp_res_lst)
            full_res_lst.append((user["personal_data"]["first_name"], user["personal_data"]["second_name"], value))

        if number_of_pleyers > len(full_res_lst): raise ValueError('"number_of_pleyers" is bigger than lenght of users list')
        sorted_trimmed_lst = sorted(full_res_lst, key=lambda elem: elem[2], reverse=True)[:number_of_pleyers + 1]
        print(*sorted_trimmed_lst, sep="\n")

    def print_most_advanced_players(self, number_of_pleyers: int) -> None:
        self.wrapper_print(number_of_pleyers, lambda lst: abs(lst.count("win") - lst.count("lose")), 2)

    def print_fastest_pleyers(self, number_of_pleyers: int) -> None:
        self.wrapper_print(number_of_pleyers, lambda lst: sum(lst) / len(lst), 0)

    def print_most_enthusiastic_players(self, number_of_pleyers: int) -> None:
        if not isinstance(number_of_pleyers, int): raise ValueError('"number_of_pleyers" value must be int type')
        full_res_lst = []
        for user in self.json_load_dict():
            start_time = datetime.datetime.strptime(user["games_information"][0][1], "%Y/%m/%d/%H:%M:%S")
            value = len(user["games_information"]) / (datetime.datetime.now() - start_time).total_seconds()
            full_res_lst.append((user["personal_data"]["first_name"], user["personal_data"]["second_name"], value))

        if number_of_pleyers > len(full_res_lst): raise ValueError('"number_of_pleyers" is bigger than lenght of users list')
        sorted_trimmed_lst = sorted(full_res_lst, key=lambda elem: elem[2], reverse=True)[:number_of_pleyers + 1]
        print(*sorted_trimmed_lst, sep="\n")

    def print_games_number(self) -> int:
        return sum(len(user["games_information"]) for user in self.json_load_dict())

    def print_players_professionalism(self) -> None:
        work_dict = self.json_load_dict()
        self.wrapper_print(len(work_dict), lambda lst: lst.count("win") / len(work_dict), 2)

    def print_general_statistics(self) -> None:
        work_dict = self.json_load_dict()
        result_dict = sorted([(user["personal_data"]["second_name"], user["games_information"]) for user in work_dict], key=lambda elem: elem[0], reverse=True)
        list(print(elem[0], f"{number}-game: {game_info}") for elem in result_dict for number, game_info in enumerate(elem[1], 1))

    def print_time_statistics(self) -> None:
        work_dict = self.json_load_dict()
        result_dict = [(user["personal_data"], user["games_information"]) for user in work_dict]
        result_dict = [sorted(tmp[1], key=lambda elem: datetime.datetime.strptime(elem[1], "%Y/%m/%d/%H:%M:%S"), reverse=True) for tmp in result_dict]
        list(print(f"{number}-game: {game_info}") for games in result_dict for number, game_info in enumerate(games, 1))


class ConnectionDB():
    def __init__(self, player: Player, statistics: StatisticsDB):
        if self.valid_params(player, statistics):
            self._player = player
            self._statistics = statistics

    @staticmethod
    def valid_params(player, statistics) -> ValueError | bool:
        if not isinstance(player, Player): raise ValueError("param: 'player' is not instance of class Player")
        if not isinstance(statistics, StatisticsDB): raise ValueError("param: 'statistics' is not instance of class StatisticsDB")
        return True

    def make_registration(self, first_name, second_name, age):
        work_dict = self._statistics.json_load_dict()
        work_dict[self._player._login] = {
            "password": self._player._password,
            "personal_data": {"first_name": first_name, "second_name": second_name, "age": age},
            "games_information": {}
        }
        self._statistics.json_upload_dict(work_dict)

    def check_credentials(self) -> None:
        work_dict = self._statistics.json_load_dict()
        try:
            if work_dict[self._player._login]["password"] == self._player._password:
                print(f"Hello {work_dict[self._player._login]['personal_data']['first_name']} {work_dict[self._player._login]['personal_data']['second_name']}")
            else:
                self._player._password = input("You inputted a wrong password, try again: ")
                self.check_credentials()
        except KeyError:
            user_input = input("We haven't found a player with this login, do you wanna make a registration (input [make]) or try again (input [try]) ?: ")
            match user_input:
                case "make":
                    first_name = input("Input your first name: ")
                    second_name = input("Input your second name: ")
                    age = input("Input your age: ")
                    self.make_registration(first_name, second_name, age)
                case "try":
                    self._player._login = input("Input valid login: ")
                    self.check_credentials()

    def save_results(self, game_lasting, game_start_time, result_of_game) -> None:
        work_dict = self._statistics.json_load_dict()
        games = work_dict[self._player._login]["games_information"]
        games[str(len(games) + 1)] = [game_lasting, game_start_time, result_of_game]
        self._statistics.json_upload_dict(work_dict)


class Game(ConnectionDB):
    def __init__(self, regim: Literal["text", "graphic"], player: Player, statistics: StatisticsDB, board: Board, user_obj: Cross | Nought):
        if super().valid_params(player, statistics):
            super().__init__(player, statistics)
            self._regim = regim
            self._board = board
            self._user_obj = user_obj
            if type(user_obj) is Cross:
                self._comp_obj = Nought(user_obj._color, user_obj._size)
            else:
                self._comp_obj = Cross(user_obj._color, user_obj._size)

    def input_move(self):
        match self._regim:
            case "text":
                inp_raw = input("Введіть хід (рядок, стовпець) від 1 до 3, або 'quit': ")
                if inp_raw.strip().lower() == "quit":
                    return None, None
                row, col = map(int, inp_raw.split(","))
                return row - 1, col - 1

            case "graphic":
                self._clicked_row = None
                self._clicked_col = None

                def on_click(x, y):
                    cell_size = self._board.match_cell_size()
                    col = int((x + cell_size * 1.5) // cell_size)
                    row = int((y + cell_size * 1.5) // cell_size)
                    if 0 <= row <= 2 and 0 <= col <= 2:
                        self._clicked_row = row
                        self._clicked_col = col
                        screen.onclick(None)

                screen = turtle.Screen()
                screen.listen()
                screen.onclick(on_click)

                while self._clicked_row is None:
                    screen.update()

                return self._clicked_row, self._clicked_col

    def make_move(self):
        free_cells = [(r, c) for r in range(3) for c in range(3) if self._board._grid[r][c] == ""]
        if not free_cells:
            return None, None
        return free_cells[randint(0, len(free_cells) - 1)]

    def game_process(self) -> Literal["win", "lose", "draw"] | None:
        self._board.display_board(self._regim, 0, 0)

        while True:
            row, col = self.input_move()
            if row is None:
                print("Game over, thanks for playing")
                return None

            if self._board._grid[row][col] != "":
                print("Клітинка зайнята, спробуй ще раз")
                continue

            self._board._grid[row][col] = self._user_obj
            self._board.display_board(self._regim, 0, 0)

            result = self._board.check_board()
            if result:
                msg = "Ти виграв!" if result == ("X" if type(self._user_obj) is Cross else "O") else ("Нічия!" if result == "draw" else "Комп'ютер виграв!")
                print(msg)
                return "win" if result == ("X" if type(self._user_obj) is Cross else "O") else result

            comp_row, comp_col = self.make_move()
            if comp_row is None:
                print("Нічия!")
                return "draw"

            self._board._grid[comp_row][comp_col] = self._comp_obj
            self._board.display_board(self._regim, 0, 0)

            result = self._board.check_board()
            if result:
                msg = "Ти виграв!" if result == ("X" if type(self._user_obj) is Cross else "O") else ("Нічия!" if result == "draw" else "Комп'ютер виграв!")
                print(msg)
                return "lose" if result == ("X" if type(self._comp_obj) is Cross else "O") else result


def main():
    user_player_login = "pavlo226"
    user_player_password = "2814"
    player = Player(user_player_login, user_player_password)
    statistics = StatisticsDB(r"C:\Users\pavlo\OneDrive\LABS_PROGRAMMING\OOP_Python_LABS\database.json")

    while True:
        user_obj_color = input("Please, choose your mark color [yellow, green, blue, red, black]: ")
        if user_obj_color in {"yellow", "green", "blue", "red", "black"}: break
        print("Wrong color, try again.")

    while True:
        user_obj_size = input("Please, choose your mark size [small, medium, large]: ")
        if user_obj_size in {"small", "medium", "large"}: break
        print("Wrong size, try again.")

    while True:
        user_board_color = input("Please, choose board background color [yellow, green, blue, red, black]: ")
        if user_board_color in {"yellow", "green", "blue", "red", "black"}: break
        print("Wrong color, try again.")

    while True:
        user_board_lines_color = input("Please, choose board lines color [yellow, green, blue, red, black]: ")
        if user_board_lines_color in {"yellow", "green", "blue", "red", "black"}: break
        print("Wrong color, try again.")

    while True:
        user_board_size = input("Please, choose board size [small, medium, large]: ")
        if user_board_size in {"small", "medium", "large"}: break
        print("Wrong size, try again.")

    while True:
        user_obj_mark = input("Please, choose who you will play [Cross or Nought]: ")
        match user_obj_mark:
            case "Cross":
                user_obj = Cross(user_obj_color, user_obj_size)
                break
            case "Nought":
                user_obj = Nought(user_obj_color, user_obj_size)
                break
            case _:
                print("Wrong input, try again.")

    while True:
        user_regim = input("Please, input regim of game [text, graphic]: ")
        if user_regim in {"text", "graphic"}: break
        print("Wrong input, try again.")

    board = Board(user_board_color, user_board_lines_color, user_board_size)
    game = Game(user_regim, player, statistics, board, user_obj)
    game.check_credentials()
    start_time = datetime.datetime.now()
    result_of_game = game.game_process()

    if result_of_game:
        total = int((datetime.datetime.now() - start_time).total_seconds())
        h, m, s = total // 3600, (total % 3600) // 60, total % 60
        game.save_results(f"{h:02}:{m:02}:{s:02}", start_time.strftime("%Y/%m/%d/%H:%M:%S"), result_of_game)

    if user_regim == "graphic":
        turtle.Screen().mainloop()
    
    if __name__ == "__main__":
        print("Hello")


if __name__ == "__main__":
    main()
