import random
from typing import List, Tuple

class LevelGenerator:
    def __init__(self, width: int = 6, height: int = 6):
        self.width = width
        self.height = height
        self.wall_chance = 0.3
        self.box_chance = 0.25
        self.target_chance = 0.2

    def generate(self) -> List[str]:
        level = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        for i in range(self.height):
            level[i][0] = '#'
            level[i][-1] = '#'
        for j in range(self.width):
            level[0][j] = '#'
            level[-1][j] = '#'

        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if random.random() < self.wall_chance:
                    level[y][x] = '#'

        while True:
            player_x = random.randint(1, self.width - 2)
            player_y = random.randint(1, self.height - 2)
            if level[player_y][player_x] == ' ':
                level[player_y][player_x] = '@'
                break

        targets = []
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if (x, y) == (player_x, player_y):
                    continue
                if level[y][x] == ' ' and random.random() < self.target_chance:
                    level[y][x] = '.'
                    targets.append((x, y))

        if not targets:
            return self.generate()

        boxes = []
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if (x, y) == (player_x, player_y):
                    continue
                if (x, y) in targets:
                    continue
                if level[y][x] == ' ' and random.random() < self.box_chance:
                    level[y][x] = '$'
                    boxes.append((x, y))

        while len(boxes) < len(targets):
            x, y = targets.pop(random.randint(0, len(targets) - 1))
            level[y][x] = ' '
        while len(targets) < len(boxes):
            x, y = boxes.pop(random.randint(0, len(boxes) - 1))
            level[y][x] = ' '

        if not self._is_solvable(level, player_x, player_y, boxes, targets):
            return self.generate()

        return [''.join(row) for row in level]

    def _is_solvable(self, level: List[List[str]], player_x: int, player_y: int, 
                    boxes: List[Tuple[int, int]], targets: List[Tuple[int, int]]) -> bool:
        for box_x, box_y in boxes:
            if (box_x, box_y) in targets:
                return False
        
        for box_x, box_y in boxes:
            if not self._is_reachable(level, player_x, player_y, box_x, box_y):
                return False
                
        for target_x, target_y in targets:
            if not self._is_reachable(level, player_x, player_y, target_x, target_y):
                return False
                
        for box_x, box_y in boxes:
            if self._is_corner(level, box_x, box_y):
                return False
                
        return True

    def _is_reachable(self, level: List[List[str]], start_x: int, start_y: int, 
                     end_x: int, end_y: int) -> bool:
        visited = set()
        queue = [(start_x, start_y)]
        
        while queue:
            x, y = queue.pop(0)
            if (x, y) == (end_x, end_y):
                return True
                
            if (x, y) in visited:
                continue
                
            visited.add((x, y))
            
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_x, new_y = x + dx, y + dy
                if (0 <= new_x < self.width and 0 <= new_y < self.height and 
                    level[new_y][new_x] != '#' and (new_x, new_y) not in visited):
                    queue.append((new_x, new_y))
                    
        return False

    def _is_corner(self, level: List[List[str]], x: int, y: int) -> bool:
        walls = 0
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if level[y + dy][x + dx] == '#':
                walls += 1
        return walls >= 2 