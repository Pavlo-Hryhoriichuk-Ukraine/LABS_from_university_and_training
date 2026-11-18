from __future__ import annotations


class MazeTreeNode:
    """
    Represents a node in the decision tree (state space tree) of the maze.
    Each node preserves the current coordinate, the path history from the root,
    and references to its child branches.
    """

    def __init__(self, position: tuple[int, int], path: list[tuple[int, int]]) -> None:
        self.position: tuple[int, int] = position
        self.path: list[tuple[int, int]] = path + [position]
        self.children: list[MazeTreeNode] = []

    def explore(
        self,
        grid: list[str],
        exit_pos: tuple[int, int],
        portals: dict[tuple[int, int], tuple[int, int]],
        visited: set[tuple[int, int]],
        solutions: list[list[tuple[int, int]]],
    ) -> None:

        if self.position == exit_pos:
            solutions.append(list(self.path))
            return

        curr_pos = self.position
        path_prefix = list(self.path)
        portal_exit = None

        if curr_pos in portals:
            portal_exit = portals[curr_pos]
            visited.add(portal_exit)
            curr_pos = portal_exit
            path_prefix.append(curr_pos)

        # Standard grid directions: Down, Up, Right, Left
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            nx, ny = curr_pos[0] + dx, curr_pos[1] + dy

            # Boundary checks
            if not (0 <= nx < len(grid) and 0 <= ny < len(grid[0])):
                continue

            # Cell validity: corridors, portals, and exit are walkable; ignore walls '#' and spaces ' '
            cell = grid[nx][ny]
            if cell in ("#", " "):
                continue

            neighbor = (nx, ny)
            if neighbor not in visited:
                visited.add(neighbor)

                # Branch out a new decision tree node
                child_node = MazeTreeNode(position=neighbor, path=path_prefix)
                self.children.append(child_node)

                # Recurse down this decision branch
                child_node.explore(grid, exit_pos, portals, visited, solutions)

                # Backtrack: unmark to allow alternative exploration branches
                visited.remove(neighbor)

        # Backtrack the teleport exit if traversed
        if portal_exit is not None:
            visited.remove(portal_exit)


class MazeSolver:
    def __init__(self, file_content_or_path: str, is_raw_text: bool = False) -> None:
        self.grid: list[str] = []
        self.start: tuple[int, int] | None = None
        self.exit_pos: tuple[int, int] | None = None
        self.portals: dict[tuple[int, int], tuple[int, int]] = {}

        self._parse(file_content_or_path, is_raw_text)

    def _parse(self, source: str, is_raw_text: bool) -> None:
        if is_raw_text:
            lines = [
                line.rstrip("\r\n")
                for line in source.strip().split("\n")
                if line.strip()
            ]
        else:
            with open(source, "r", encoding="utf-8") as f:
                lines = [line.rstrip("\r\n") for line in f if line.strip()]

        self.grid = lines
        portal_pairs: dict[str, list[tuple[int, int]]] = {}

        for r_idx, row in enumerate(self.grid):
            for c_idx, char in enumerate(row):
                if char == "?":
                    self.start = (r_idx, c_idx)
                elif char == "!":
                    self.exit_pos = (r_idx, c_idx)
                elif char.isalpha() and char.islower():
                    portal_pairs.setdefault(char, []).append((r_idx, c_idx))

        # Build bidirectional links between matching portal coordinates
        for _, coords in portal_pairs.items():
            if len(coords) == 2:
                p1, p2 = coords
                self.portals[p1] = p2
                self.portals[p2] = p1

    def solve(self) -> tuple[list[int], list[list[tuple[int, int]]]]:

        if self.start is None or self.exit_pos is None:
            return [], []

        root = MazeTreeNode(position=self.start, path=[])
        visited: set[tuple[int, int]] = {self.start}
        solutions: list[list[tuple[int, int]]] = []

        # Recursively construct and traverse the tree
        root.explore(self.grid, self.exit_pos, self.portals, visited, solutions)

        # Calculate lengths (number of transition steps is len(path) - 1)
        # Sort both paths and lengths in ascending order by step count
        solutions.sort(key=lambda p: len(p) - 1)
        lengths = [len(p) - 1 for p in solutions]

        return lengths, solutions


def find_maze_paths(file_path: str) -> tuple[list[int], list[list[tuple[int, int]]]]:
    solver = MazeSolver(file_path, is_raw_text=False)
    return solver.solve()


def test_maze_solver() -> None:
    sample_maze = (
        "#######?#########\n"
        "#######.........#\n"
        "#######.#######.#\n"
        "#######.#######.#\n"
        "#######a#######.#\n"
        "##.##       ###.#\n"
        "a..##       ###.#\n"
        "##.##       ###.#\n"
        "##..b       ###.#\n"
        "##.##       ###.#\n"
        "#########c#####.#\n"
        "b.#######...###.#\n"
        "#.#########.###.#\n"
        "c.#########.....#\n"
        "###########!#####"
    )

    solver = MazeSolver(sample_maze, is_raw_text=True)
    lengths, paths = solver.solve()

    print(f"Lengths found: {lengths}")
    assert lengths == [23, 26], f"Expected [23, 26], got {lengths}"
    assert len(paths) == 2, f"Expected 2 paths, got {len(paths)}"

    assert len(paths[0]) - 1 == 23
    assert len(paths[1]) - 1 == 26

    print(
        "All assertions passed successfully! The tree-based exploration works flawlessly."
    )


if __name__ == "__main__":
    test_maze_solver()
