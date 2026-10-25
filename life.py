#!/usr/bin/env python3
"""Conway's Game of Life in the terminal.

Usage:
    python3 life.py glider_gun.csv

The CSV file is a grid: 1 = living cell, 0 (or empty) = dead cell.
An optional line "edges,wall" or "edges,wrap" chooses the edge mode
(default: wrap).

Keys:
    space   pause / resume
    n       next generation (when paused)
    + / -   faster / slower
    w       edges: wrap around (torus) or wall
    r       restart from the CSV file
    c       clear the screen
    click   add or remove a cell with the mouse
    q       quit
"""

import csv
import curses
import sys


def load_pattern(filename):
    """Read the CSV file and return a list of rows of 0 and 1."""
    pattern = []
    with open(filename, newline="") as f:
        for row in csv.reader(f):
            if len(row) > 0 and row[0].strip() == "edges":
                continue  # this is a setting, not a row of cells
            line = []
            for value in row:
                if value.strip() == "1":
                    line.append(1)
                else:
                    line.append(0)
            pattern.append(line)
    return pattern


def load_wrap(filename):
    """Read the edge mode from the CSV file.

    Return True for "edges,wrap" (or no edges line), False for "edges,wall".
    """
    with open(filename, newline="") as f:
        for row in csv.reader(f):
            if len(row) >= 2 and row[0].strip() == "edges":
                return row[1].strip() != "wall"
    return True


def empty_grid(height, width):
    """Return a grid full of dead cells."""
    grid = []
    for y in range(height):
        grid.append([0] * width)
    return grid


def place_pattern(grid, pattern):
    """Copy the pattern into the middle of the grid."""
    height = len(grid)
    width = len(grid[0])

    pattern_height = len(pattern)
    pattern_width = 0
    for row in pattern:
        if len(row) > pattern_width:
            pattern_width = len(row)

    top = (height - pattern_height) // 2
    left = (width - pattern_width) // 2

    for y in range(pattern_height):
        for x in range(len(pattern[y])):
            gy = top + y
            gx = left + x
            # Ignore cells that do not fit on the screen
            if 0 <= gy < height and 0 <= gx < width:
                grid[gy][gx] = pattern[y][x]


def count_neighbors(grid, y, x, wrap):
    """Count the living cells around (y, x).

    If wrap is True, the world wraps around: the left edge touches
    the right edge, and the top edge touches the bottom edge.
    If wrap is False, everything outside the grid is dead.
    """
    height = len(grid)
    width = len(grid[0])
    count = 0
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dy == 0 and dx == 0:
                continue  # this is the cell itself, not a neighbor
            ny = y + dy
            nx = x + dx
            if wrap:
                ny = ny % height
                nx = nx % width
            elif ny < 0 or ny >= height or nx < 0 or nx >= width:
                continue  # outside the grid: no neighbor here
            count = count + grid[ny][nx]
    return count


def next_generation(grid, wrap):
    """Apply the rules of life and return the new grid."""
    height = len(grid)
    width = len(grid[0])
    new_grid = empty_grid(height, width)

    for y in range(height):
        for x in range(width):
            neighbors = count_neighbors(grid, y, x, wrap)
            alive = grid[y][x] == 1

            if alive and (neighbors == 2 or neighbors == 3):
                new_grid[y][x] = 1  # survives
            elif not alive and neighbors == 3:
                new_grid[y][x] = 1  # is born
            else:
                new_grid[y][x] = 0  # dies or stays dead

    return new_grid


def count_alive(grid):
    total = 0
    for row in grid:
        total = total + sum(row)
    return total


def draw(screen, grid, generation, paused, delay, wrap):
    """Draw the grid and the status bar."""
    screen.erase()

    height = len(grid)
    width = len(grid[0])
    for y in range(height):
        for x in range(width):
            if grid[y][x] == 1:
                # Two characters per cell, so cells look square
                try:
                    screen.addstr(y, x * 2, "██", curses.color_pair(1))
                except curses.error:
                    pass  # the terminal got smaller: skip this cell

    if paused:
        state = "PAUSE"
    else:
        state = "RUN"

    status = " Gen: " + str(generation)
    status = status + " | Cells: " + str(count_alive(grid))
    status = status + " | Delay: " + str(delay) + " ms"
    status = status + " | " + state
    if wrap:
        status = status + " | Edges: wrap"
    else:
        status = status + " | Edges: wall"
    status = status + " | space n + - w r c q "

    screen_height, screen_width = screen.getmaxyx()
    try:
        screen.addstr(screen_height - 1, 0, status[:screen_width - 1], curses.color_pair(2))
    except curses.error:
        pass

    screen.refresh()


def main(screen):
    filename = sys.argv[1]
    pattern = load_pattern(filename)
    start_wrap = load_wrap(filename)

    # Screen setup
    curses.curs_set(0)  # hide the cursor
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.mousemask(curses.BUTTON1_CLICKED | curses.BUTTON1_PRESSED)

    # The grid fills the screen, minus one line for the status bar
    screen_height, screen_width = screen.getmaxyx()
    height = screen_height - 1
    width = screen_width // 2

    grid = empty_grid(height, width)
    place_pattern(grid, pattern)

    generation = 0
    paused = True
    delay = 100  # milliseconds between two generations
    wrap = start_wrap  # True: the world wraps around, False: the edges are walls

    while True:
        draw(screen, grid, generation, paused, delay, wrap)

        # Wait for a key, but not longer than "delay"
        if paused:
            screen.timeout(-1)  # wait forever
        else:
            screen.timeout(delay)
        key = screen.getch()

        if key == ord("q"):
            break
        elif key == ord(" "):
            paused = not paused
        elif key == ord("n"):
            grid = next_generation(grid, wrap)
            generation = generation + 1
        elif key == ord("+"):
            delay = max(10, delay - 20)
        elif key == ord("-"):
            delay = min(1000, delay + 20)
        elif key == ord("w"):
            wrap = not wrap
        elif key == ord("r"):
            grid = empty_grid(height, width)
            place_pattern(grid, pattern)
            generation = 0
            wrap = start_wrap
        elif key == ord("c"):
            grid = empty_grid(height, width)
            generation = 0
        elif key == curses.KEY_MOUSE:
            try:
                mouse = curses.getmouse()
            except curses.error:
                continue
            mx = mouse[1] // 2
            my = mouse[2]
            if 0 <= my < height and 0 <= mx < width:
                grid[my][mx] = 1 - grid[my][mx]  # 0 becomes 1, 1 becomes 0
        elif key == -1 and not paused:
            # No key pressed during the delay: time for the next generation
            grid = next_generation(grid, wrap)
            generation = generation + 1


if len(sys.argv) != 2:
    print("Usage: python3 life.py <file.csv>")
    sys.exit(1)

curses.wrapper(main)
