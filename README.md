# Game of Life

Conway's Game of Life in your terminal. One Python file, no libraries to install.

## What is it?

The Game of Life is not a game you play. You draw some cells, then you watch them live.

The world is a grid. Each cell is alive or dead. At each step (a "generation"), every cell looks at its 8 neighbors:

- A living cell with **2 or 3** living neighbors **survives**.
- A dead cell with **exactly 3** living neighbors **is born**.
- All other cells **die** (too lonely, or too crowded).

That's all. With these 3 rules, you get shapes that move, shapes that blink, and even shapes that build other shapes.

The mathematician John Conway invented it in 1970.

## How to run it

You need Python 3. It works out of the box on macOS and Linux. On Windows, first run `pip install windows-curses`.

```
python3 life.py glider_gun.csv
```

The game starts paused. Press `space` to start.

### Run it from an IDE

The game needs a real terminal. Some IDEs run scripts in an output panel that is not a terminal. Then you get this error:

```
_curses.error: setupterm: could not find terminal
```

**PyCharm**: open *Run → Edit Configurations…*, select your `life.py` configuration, then click *Modify options* and check **Emulate terminal in output console**. This also works in Debug mode. If the error is still there, add `TERM=xterm-256color` to *Environment variables*.

**VS Code**: run the script in the integrated terminal, not in the *Debug Console*. In `.vscode/launch.json`, set `"console": "integratedTerminal"` (this is the default value):

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Game of Life",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/life.py",
            "args": ["glider_gun.csv"],
            "console": "integratedTerminal"
        }
    ]
}
```

With these settings, you can also use the debugger and breakpoints.

To only play (no debugger), you can also open the built-in terminal tab of the IDE and run `python3 life.py glider_gun.csv` there.

## Keys

| Key       | Action                                |
|-----------|---------------------------------------|
| `space`   | Pause / resume                        |
| `n`       | Next generation (when paused)         |
| `+` / `-` | Faster / slower                       |
| `w`       | Edges: wrap or wall (see below)       |
| `r`       | Restart from the CSV file             |
| `c`       | Clear the screen                      |
| click     | Add or remove a cell with the mouse   |
| `q`       | Quit                                  |

## Edges: wrap or wall

- **wrap** (default): the world is round like a donut. A shape that exits on the right comes back on the left. A shape that exits at the bottom comes back at the top. In theory, the Game of Life has an infinite grid, and this is the closest we can get on a screen.
- **wall**: outside the screen, all cells are dead. Shapes that reach the edge crash into it.

Each pattern file can choose its best mode (see [Make your own pattern](#make-your-own-pattern)). For example, `glider_gun.csv` starts in wall mode, so the gun keeps shooting forever.

Try this: start `glider_gun.csv` and press `w` to switch to wrap mode. The gliders go around the world and come back to destroy the gun!

## Patterns

### Classics

| File              | What it does                                                    |
|-------------------|-----------------------------------------------------------------|
| `oscillators.csv` | Shapes that blink on the spot: blinker, toad, beacon (every 2 steps) and pulsar (every 3 steps). |
| `glider.csv`      | A glider: 5 cells that walk across the screen.                  |
| `spaceships.csv`  | Three spaceships (small, medium, heavy). They all fly at the same speed: half a cell per step. |

### Long lives

These patterns are called "methuselahs": they start very small and live for a long time.

| File              | What it does                                                    |
|-------------------|-----------------------------------------------------------------|
| `r_pentomino.csv` | Only 5 cells, but it moves for about 500 generations on a normal screen (1103 on an infinite grid). |
| `acorn.csv`       | 7 cells. It moves for 300 to 1250 generations, depending on your screen size (5206 on an infinite grid). |
| `diehard.csv`     | 7 cells that disappear completely at generation 130. Watch the `Gen:` counter! |

### Guns

| File              | What it does                                                    |
|-------------------|-----------------------------------------------------------------|
| `glider_gun.csv`  | The Gosper glider gun: it shoots a new glider every 30 steps.   |
| `gun_battle.csv`  | Two guns shoot at each other. The gliders crash and disappear in the middle. |

### Logic gate: NOT

`not_gate.csv` shows that the Game of Life can compute, like a computer.

A signal is a line of gliders, one glider every 30 steps:

- a glider = **1**
- no glider (a gap in the line) = **0**

The **input** comes from the top left: 4 gliders that mean `1, 0, 1, 1`. The gun at the bottom shoots the **output** to the bottom left. When an input glider meets an output glider, both disappear. So:

- input **1** → the output glider is destroyed → output **0**
- input **0** → the output glider passes → output **1**

Input `1, 0, 1, 1` gives output `0, 1, 0, 0`. After that, there is no more input (only 0), so the output is always 1.

Try this: press `n` many times to watch the collisions one by one. Then edit the CSV, or click with the mouse, to change the input.

This pattern is big: your terminal needs at least 45 lines and 110 columns. Make the window full screen, or make the font smaller with `Cmd -` (Mac) or `Ctrl -`.

Each CSV file starts with its best edge mode: `wall` for the guns and the NOT gate, `wrap` for all the others.

## Make your own pattern

A pattern is a CSV file. You can write it in a text editor, Excel or LibreOffice.

- First line: `edges,wrap` or `edges,wall`, the edge mode (if you forget it, the mode is wrap)
- `1` = living cell
- `0` or empty = dead cell

Use `edges,wall` for patterns that shoot gliders forever, like guns. Use `edges,wrap` for everything else.

Example, a "blinker" (3 cells that turn on the spot):

```
edges,wrap
0,0,0
1,1,1
0,0,0
```

Save it as `blinker.csv`, then run:

```
python3 life.py blinker.csv
```

The pattern is placed in the middle of the screen.

You can also draw with the mouse: press `c` to clear the screen, click to add cells, then press `space`.

## Ideas to change the code

The code is in `life.py`. Each part is a small function. Here are some ideas:

1. **Change the colors.** Look for `COLOR_GREEN` in `main()`. Try `COLOR_RED`, `COLOR_YELLOW` or `COLOR_MAGENTA`.
2. **Change the cell shape.** In `draw()`, replace `"██"` with `"()"` or `"[]"`.
3. **Change the rules.** In `next_generation()`, a cell is born with 3 neighbors. What happens with 3 or 6? (This rule is called "HighLife". Search for it!)
4. **Add a record.** Show the highest number of living cells seen since the start.
5. **Add a key** that fills the screen with random cells. Tip: look at `random.randint(0, 1)`.

## Learn more

- [Conway's Game of Life on Wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)
- [LifeWiki](https://conwaylife.com/wiki/), a huge list of patterns
