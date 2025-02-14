from queue import PriorityQueue

from main import Level

class AStarSolver:
    def __init__(self):
        self.visited = set()
        self.pq = PriorityQueue()

    def solve(self, level: Level):
        self.visited.clear()
        self.pq.queue.clear()
        
        print("Starting A* search...")
        self.pq.put((0, level))
        steps = 0
        
        while not self.pq.empty():
            cost, current = self.pq.get()
            if current in self.visited:
                continue
            self.visited.add(current)
            
            steps += 1
            if steps % 1000 == 0:
                print(f"Processed {steps} states, queue size: {self.pq.qsize()}, visited states: {len(self.visited)}")
            
            if current.check_win():
                print(f"Solution found after processing {steps} states!")
                return current
            
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_level = Level(current.data)
                if new_level.move_player(dx, dy):
                    if new_level not in self.visited:
                        self.pq.put((cost + 1, new_level))
        
        print(f"No solution found after processing {steps} states")
        return None
