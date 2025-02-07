import random

def generate_sokoban_level():
    width = 40
    height = 15
    level = [['#' for _ in range(width)] for _ in range(height)]
    rooms = []

    for _ in range(random.randint(5, 8)):
        w = random.randint(4, 8)
        h = random.randint(3, 6)
        x = random.randint(1, width - w - 1)
        y = random.randint(1, height - h - 1)
        
        overlap = False
        for r in rooms:
            if (x < r['x']+r['w'] and x+w > r['x'] and
                y < r['y']+r['h'] and y+h > r['y']):
                overlap = True
                break
        if not overlap:
            room = {'x': x, 'y': y, 'w': w, 'h': h}
            rooms.append(room)
            for yi in range(y, y+h):
                for xi in range(x, x+w):
                    level[yi][xi] = ' '


    for i in range(1, len(rooms)):
        prev = rooms[i-1]
        curr = rooms[i]
        px = prev['x'] + prev['w']//2
        py = prev['y'] + prev['h']//2
        cx = curr['x'] + curr['w']//2
        cy = curr['y'] + curr['h']//2

        for x in range(min(px, cx), max(px, cx)+1):
            level[py][x] = ' '

        for y in range(min(py, cy), max(py, cy)+1):
            level[y][cx] = ' '

    boxes = []
    goals = []
    for room in rooms:
        gx = room['x'] + room['w']//2
        gy = room['y'] + room['h']//2
        if level[gy][gx] == ' ':
            level[gy][gx] = '.'
            goals.append((gx, gy))
        
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top' and room['y'] > 1:
            bx, by = random.randint(room['x']+1, room['x']+room['w']-2), room['y']-1
        elif side == 'bottom' and room['y']+room['h'] < height-1:
            bx, by = random.randint(room['x']+1, room['x']+room['w']-2), room['y']+room['h']
        elif side == 'left' and room['x'] > 1:
            bx, by = room['x']-1, random.randint(room['y']+1, room['y']+room['h']-2)
        elif side == 'right' and room['x']+room['w'] < width-1:
            bx, by = room['x']+room['w'], random.randint(room['y']+1, room['y']+room['h']-2)
        else:
            continue
        
        if 0 <= by < height and 0 <= bx < width and level[by][bx] == ' ':
            level[by][bx] = '$'
            boxes.append((bx, by))

    if rooms:
        room = rooms[0]
        px = random.randint(room['x']+1, room['x']+room['w']-2)
        py = random.randint(room['y']+1, room['y']+room['h']-2)
        if level[py][px] == ' ':
            level[py][px] = '@'

    while len(boxes) > len(goals):
        bx, by = boxes.pop()
        level[by][bx] = ' '
    while len(goals) > len(boxes):
        gx, gy = goals.pop()
        level[gy][gx] = ' '

    return [''.join(row).rstrip() for row in level]

level = generate_sokoban_level()
for row in level:
    print(row)
