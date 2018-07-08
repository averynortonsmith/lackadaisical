import time
import random

def simulate(initialCells, iterations, showSteps=False, delay=0):
    cells = initialCells
    for x in range(iterations):
        if showSteps:
            print("iteration ", x + 1, "of", str(iterations) + ":")
            print(showCells(cells) + "\n")
        cells = tick(cells)
        if showSteps: 
            time.sleep(delay)
    if not showSteps: return cells

def zeroCells(rows, columns):
    return [[0] * columns for _ in range(rows)]

def randomCells(rows, columns):
    return [[round(random.random()) for _ in range(columns)] for _ in range(rows)]

def showCells(cells):
    return "\n".join(showRow(row) for row in cells)

def showRow(row):
    return "[" + " ".join(" " if cell == 0 else "*" for cell in row) + "]"

def tick(cells):
    rows = len(cells)
    columns = len(cells[0])
    newCells = zeroCells(rows, columns)
    for y in range(rows):
        for x in range(columns):
            value = cells[y][x]
            count = getCount(cells, x, y, rows, columns)
            birth = not value and count == 3
            survive = value and count in {2, 3}
            newCells[y][x] = int(birth or survive)
    return newCells

def getCount(cells, x, y, rows, columns):
    deltas = [-1, 0, 1]
    count = 0
    for dy in deltas:
        for dx in deltas:
            if dy != 0 or dx != 0:
                count += cells[(y + dy) % rows][(x + dx) % columns]
    return count