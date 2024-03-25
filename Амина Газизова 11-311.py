import matplotlib.pyplot as plt
from dataclasses import dataclass, field
import random

@dataclass
class Labirint:
    x: int
    y: int
    component: int
    is_open: bool = field(default=False)
    walls: list = field(default_factory=lambda: [True, True, True, True])
N = 30
def find(cell, parent):
    if parent[cell] != cell:
        parent[cell] = find(parent[cell], parent)
    return parent[cell]

def union(cell1, cell2, parent, rank):
    root1 = find(cell1, parent)
    root2 = find(cell2, parent)
    if root1 != root2:
        if rank[root1] > rank[root2]:
            parent[root2] = root1
        elif rank[root1] < rank[root2]:
            parent[root1] = root2
        else:
            parent[root2] = root1
            rank[root1] += 1

def generate_maze(size):
    maze = [[Labirint(x, y, x * size + y) for y in range(size)] for x in range(size)]
    parent = {(x, y): (x, y) for x in range(size) for y in range(size)}
    rank = {(x, y): 0 for x in range(size) for y in range(size)}

    while len(set(find((x, y), parent) for x in range(size) for y in range(size))) > 1:
        x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        direction = random.choice(['top', 'right', 'bottom', 'left'])

        if direction == 'top' and y > 0:
            if find((x, y), parent) != find((x, y - 1), parent):
                union((x, y), (x, y - 1), parent, rank)
                maze[x][y].walls[0] = False
                maze[x][y - 1].walls[2] = False
        elif direction == 'right' and x < size - 1:
            if find((x, y), parent) != find((x + 1, y), parent):
                union((x, y), (x + 1, y), parent, rank)
                maze[x][y].walls[1] = False
                maze[x + 1][y].walls[3] = False
        elif direction == 'bottom' and y < size - 1:
            if find((x, y), parent) != find((x, y + 1), parent):
                union((x, y), (x, y + 1), parent, rank)
                maze[x][y].walls[2] = False
                maze[x][y + 1].walls[0] = False
        elif direction == 'left' and x > 0:
            if find((x, y), parent) != find((x - 1, y), parent):
                union((x, y), (x - 1, y), parent, rank)
                maze[x][y].walls[3] = False
                maze[x - 1][y].walls[1] = False

    maze[0][0].walls[3] = False
    maze[size - 1][size - 1].walls[1] = False
    return maze
maze = generate_maze(N)

def draw_maze(maze):
    fig, xy = plt.subplots(figsize=(7, 7))
    xy.set_xlim(-1, N + 1)
    xy.set_ylim(-1, N + 1)

    for x in range(N):
        for y in range(N):
            cell = maze[x][y]
            if cell.walls[0]:
                xy.plot([x, x + 1], [y, y], 'k-', lw=2)
            if cell.walls[1]:
                xy.plot([x + 1, x + 1], [y, y + 1], 'k-', lw=2)
            if cell.walls[2]:
                xy.plot([x, x + 1], [y + 1, y + 1], 'k-', lw=2)
            if cell.walls[3]:
                xy.plot([x, x], [y, y + 1], 'k-', lw=2)


draw_maze(maze)
plt.show()
