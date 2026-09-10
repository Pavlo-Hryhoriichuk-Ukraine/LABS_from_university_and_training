from dataclasses import dataclass, field
from collections import defaultdict
from typing import Any
from collections.abc import Callable
import turtle
import time

TypeTuringComandTable = dict[tuple[str,str], tuple[str,str, str]]
@dataclass
class TuringMachine:
    machine_code_table: dict[tuple[str, str], tuple[str, str, str]]
    state: str
    end_states: dict[str, str | bool | None]
    blank_symbol: str = "_"
    _move_states: dict[str, int] = field(init=False, default_factory=lambda: {'R': 1, 'L': -1, 'N': 0})
    head_position: int = field(init=False, default=0)
    _steps: int = field(init=False, default=0)
    _MAX_STEPS_NUMBER: int = field(init=False, default=15000)
    tape: defaultdict[int, str] = field(init=False)

    def init_tape(self, user_string: str) -> None:
        self.tape = defaultdict(lambda: self.blank_symbol)
        for i, char in enumerate(user_string):
            self.tape[i] = char

    def step(self) -> bool:
        if self.state in self.end_states:
            return False # means: end

        current_symbol = self.tape[self.head_position]

        if (self.state, current_symbol) not in self.machine_code_table:
            raise ValueError(f"There is no rule for state: '{self.state}' and symbol: '{current_symbol}'")

        next_state, write_symbol, move_dir = self.machine_code_table[(self.state, current_symbol)]
        self.tape[self.head_position] = write_symbol
        self.state = next_state
        self.head_position += self._move_states[move_dir]

        self._steps += 1
        if self._steps >= self._MAX_STEPS_NUMBER:
            raise RecursionError("Step limit was reached!")

        return True


    def get_result(self) -> str | bool:
        """Extracts and formats the final computation output."""
        result = self.end_states.get(self.state)
        if result is not None:
            return result

        if not self.tape:
            return ""

        min_idx, max_idx = min(self.tape.keys()), max(self.tape.keys())
        return "".join(self.tape[i] for i in range(min_idx, max_idx + 1))


    def run(self, user_string: str, on_step: Callable[['TuringMachine'], Any] | None = None) -> str | bool:

        self.init_tape(user_string)

        if on_step:
            on_step(self)

        while self.step():
            if on_step:
                on_step(self)

        return self.get_result()


class TuringVisualizer:
    def __init__(self, tm: TuringMachine, cell_size: int = 40, visible_cells: int = 11) -> None:
        self.tm = tm
        self.cell_size = cell_size
        self.visible_cells = visible_cells

        turtle.setup(width=750, height=450)
        self.screen = turtle.Screen()
        self.screen.tracer(0)

        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.penup()
        self.pen.speed(0)

    def _draw_square(self, x: float, y: float, size: float) -> None:
        self.pen.goto(x, y)
        self.pen.pendown()
        for _ in range(4):
            self.pen.forward(size)
            self.pen.right(90)
        self.pen.penup()

    def render(self, delay: float = 0.25) -> None:
        self.pen.clear()

        self.pen.goto(0, 130)
        info_text = f"Step: {self.tm._steps}   |   State: {self.tm.state}   |   Head Index: {self.tm.head_position}"
        self.pen.write(info_text, align="center", font=("Arial", 14, "bold"))

        half_cells = self.visible_cells // 2
        start_x = - (self.visible_cells * self.cell_size) / 2
        y_tape = 40

        for i in range(self.visible_cells):
            tape_index = self.tm.head_position - half_cells + i
            cell_x = start_x + i * self.cell_size

            self._draw_square(cell_x, y_tape, self.cell_size)

            symbol = self.tm.tape[tape_index]
            self.pen.goto(cell_x + self.cell_size / 2, y_tape - self.cell_size + 8)
            self.pen.write(symbol, align="center", font=("Courier", 16, "bold"))

            self.pen.goto(cell_x + self.cell_size / 2, y_tape + 5)
            self.pen.write(str(tape_index), align="center", font=("Arial", 9, "normal"))

        arrow_x = 0
        arrow_y = y_tape - self.cell_size - 10
        self.pen.goto(arrow_x, arrow_y)
        self.pen.write("▲\n[Head]", align="center", font=("Arial", 10, "bold"))

        self.screen.update()
        time.sleep(delay)


def print_text_step(tm: TuringMachine) -> None:
    min_idx = min(min(tm.tape.keys(), default=0), tm.head_position - 3)
    max_idx = max(max(tm.tape.keys(), default=0), tm.head_position + 3)

    tape_slice = "".join(tm.tape[i] for i in range(min_idx, max_idx + 1))

    pointer_offset = tm.head_position - min_idx
    pointer_line = " " * pointer_offset + "^"

    print(f"Step {tm._steps:03d} | State: {tm.state:<6} | Head: {tm.head_position:2d}")
    print(f"Tape:   {tape_slice}")
    print(f"        {pointer_line}")
    print("-" * 40)


if __name__ == "__main__":
    test_add_table: TypeTuringComandTable = {
        ('q0', '1') : ('q1', '_', 'R'),
        ('q1', '1') : ('q2', '_', 'R'),
        ('q2', '1') : ('q2', '1', 'R'),
        ('q2', '_') : ('q3', '1', 'R'),
        ('q3', '1') : ('q3', '1', 'R'),
        ('q3', '_') : ('q_done', '_', 'R')
    }

    test_table_2: TypeTuringComandTable = {
        ('q0', '0'): ('q0', '1', 'R'),
        ('q0', '1'): ('q0', '0', 'R'),
        ('q0', '_'): ('q_done', '_', 'N')
    }

    tm = TuringMachine(
        machine_code_table=test_add_table,
        state='q0',
        end_states={'q_done': None},
        blank_symbol='_'
    )

    visualizer = TuringVisualizer(tm, cell_size=45, visible_cells=11)

    # Calolback
    def sync_observer(machine: TuringMachine) -> None:
        print_text_step(machine)
        visualizer.render(delay=2)

    input_string = "11_111"
    print(f"--- Starting execution for input: {input_string} ---")

    result = tm.run(input_string, on_step=sync_observer)

    print(f"\nCompleted! Result on tape: {result}")
    turtle.done()