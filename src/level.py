class Level:
    def __init__(self, level_data):
        # Убеждаемся, что все строки одинаковой длины
        max_width = max(len(row) for row in level_data)
        self.data = [row.ljust(max_width) for row in level_data]
        self.width = max_width
        self.height = len(self.data)
        self.find_player()
        self.moves_count = 0
        # print("\nНачальное состояние уровня:")
        # self.print_board()

    def print_board(self):
        """Выводит текущее состояние доски в консоль"""
        print("\n" + "=" * (self.width + 4))
        for row in self.data:
            print("║ " + row + " ║")
        print("=" * (self.width + 4))
        print(f"Позиция игрока: {self.player_pos}")
        print(f"Сделано ходов: {self.moves_count}\n")

    def find_player(self):
        self.player_pos = None
        for y, row in enumerate(self.data):
            for x, char in enumerate(row):
                if char in '@+':
                    self.player_pos = (x, y)
                    return

    def check_win(self):
        return not any('$' in row for row in self.data)

    def get_tile(self, x, y):
        if 0 <= y < self.height and 0 <= x < self.width:
            return self.data[y][x]
        return '#'  # За пределами уровня считаем стену

    def move_player(self, dx, dy):
        if not self.player_pos:
            return False

        p_from = {"+": ".", "@": " "}
        p_to = {"$": "@", " ": "@", "*": "+", ".": "+"}
        box_to = {".": "*", " ": "$"}

        px, py = self.player_pos
        nx, ny = px + dx, py + dy
        nnx, nny = nx + dx, ny + dy

        current = self.get_tile(px, py)
        next_tile = self.get_tile(nx, ny)
        next_next_tile = self.get_tile(nnx, nny)

        new_data = [list(row) for row in self.data]

        # Случай 1: Впереди ящик
        if next_tile in "$*":
            # Проверяем, можно ли его толкнуть
            if next_next_tile in box_to:
                new_data[py][px] = p_from[current]
                new_data[ny][nx] = p_to[next_tile]
                new_data[nny][nnx] = box_to[next_next_tile]
                self.data = [''.join(row) for row in new_data]
                self.player_pos = (nx, ny)
                self.moves_count += 1
                # print(f"\nХод {self.moves_count}: Толкаем ящик {(nx, ny)} -> {(nnx, nny)}")
                # self.print_board()
                return True
            return False

        # Случай 2: Впереди пустое место или цель
        if next_tile in " .":
            new_data[py][px] = p_from[current]
            new_data[ny][nx] = p_to[next_tile]
            self.data = [''.join(row) for row in new_data]
            self.player_pos = (nx, ny)
            self.moves_count += 1
            # print(f"\nХод {self.moves_count}: Перемещение {(px, py)} -> {(nx, ny)}")
            # self.print_board()
            return True

        return False

    @staticmethod
    def from_file(filename):
        with open(filename, 'r') as file:
            return Level([line.rstrip() for line in file.readlines()])
    
    def __eq__(self, other):
        if not isinstance(other, Level):
            return False
        return self.data == other.data

    def __hash__(self):
        return hash(tuple(self.data))
    
    def __lt__(self, other):
        return self.moves_count < other.moves_count
