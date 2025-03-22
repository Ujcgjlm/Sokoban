from queue import PriorityQueue

from src.level import Level

class DijkstraSolver:
    def __init__(self):
        self.visited = set()
        self.pq = PriorityQueue()
        self.path = []

    def solve(self, level: Level):
        self.visited.clear()
        self.pq.queue.clear()
        self.path.clear()
        print("Starting djikstra search...")
        self.pq.put((0, level, []))
        steps = 0
        
        while not self.pq.empty():
            cost, current, path = self.pq.get()
            if current in self.visited:
                continue
            self.visited.add(current)
            
            steps += 1
            if steps % 1000 == 0:
                print(f"Processed {steps} states, queue size: {self.pq.qsize()}, visited states: {len(self.visited)}, cost: {cost}")

            if current.check_win():
                print(f"Solution found after processing {steps} states!")
                return path
            
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_level = Level(current.data)
                if new_level.move_player(dx, dy):
                    if new_level not in self.visited:
                        self.pq.put((cost + 1, new_level, path + [(dx, dy)]))
        
        print(f"No solution found after processing {steps} states")
        return None


if __name__ == "__main__":
    level = Level.from_file("levels/level02.txt")
    solver = DijkstraSolver()
    solution = solver.solve(level)
    print(solution)
