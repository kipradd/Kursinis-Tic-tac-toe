# Tic Tac Toe – Coursework Report

---

## 1. Introduction

### What is this application?

This is a terminal-based **Tic Tac Toe** game. Two players take turns placing `X` or `O` on a 3×3 grid. The first to get three in a row wins. If the grid fills up with no winner, it is a draw.

The game has two modes:
- **Human vs Human** – two people play on the same keyboard
- **Human vs AI** – one person plays against the computer

Every result is saved to a `results.csv` file automatically.

### How to run the program

You need **Python 3** installed. Open a terminal in the project folder and run:

```bash
python main.py
```

### How to use the program

1. Choose mode `1` or `2`
2. Players take turns entering a number from **1 to 9**:

```
 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9
```

3. The game announces a winner or a draw
4. You can choose to play again after each game
5. When you quit, all results from the session are shown

---

## 2. Body / Analysis

### 4 OOP Pillars

#### Encapsulation

The `Board` class keeps its list of cells hidden using double underscores (`__cells`). Nothing outside the class can read or change it directly — you must use the class's own methods.

```python
class Board:
    def __init__(self):
        self.__cells = [" "] * 9  # hidden from outside

    def place(self, pos, symbol):
        self.__cells[pos] = symbol

    def is_empty(self, pos):
        return self.__cells[pos] == " "
```

#### Abstraction

`Player` is an abstract class. It forces every subclass to implement `make_move()`, but does not say how. This hides the details of *how* a move is made from the rest of the program.

```python
from abc import ABC, abstractmethod

class Player(ABC):
    @abstractmethod
    def make_move(self, board):
        pass  # subclasses must fill this in
```

#### Inheritance

`HumanPlayer` and `AIPlayer` both inherit from `Player`. They automatically get the `name` and `symbol` properties and only need to write their own `make_move()`.

```python
class HumanPlayer(Player):   # inherits from Player
    def make_move(self, board):
        pos = int(input("Pick 1-9: ")) - 1
        return pos

class AIPlayer(Player):      # also inherits from Player
    def make_move(self, board):
        for i in range(9):
            if board.is_empty(i):
                return i
```

#### Polymorphism

In `Game`, the current player is stored as a `Player` object. The game loop calls `player.make_move(board)` without knowing or caring whether it is a human or AI — both respond to the same method, but do different things.

```python
player = self.__players[turn % 2]  # could be Human or AI
pos = player.make_move(self.__board)  # same call, different behaviour
```

---

### Design Pattern: Singleton

The `ResultSaver` class uses the **Singleton** pattern. This means only one instance of it can ever exist. The pattern works by overriding `__new__` — on the first call it creates the instance, and on every call after that it returns the same one.

This is the best choice here because the file should only ever be opened from one place. Patterns like Factory Method or Builder are for *creating* different objects — that is the opposite of what is needed.

```python
class ResultSaver:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

---

### Composition and Aggregation

**Composition** — `Game` creates its own `Board` internally. The board cannot exist without the game.

```python
class Game:
    def __init__(self, player1, player2):
        self.__board = Board()  # Board is created here, owned by Game
```

**Aggregation** — The players are created *outside* `Game` and passed in. They could exist without a `Game`.

```python
        self.__players = [player1, player2]  # players exist independently
```

---

### Reading from and Writing to File

`ResultSaver` saves every game result to `results.csv` using Python's `csv` module. It appends one row per game, and reads them all back when the session ends.

**Writing:**
```python
def save(self, game_num, winner):
    with open(self.filename, "a", newline="") as f:
        csv.writer(f).writerow([game_num, winner])
```

**Reading:**
```python
def load(self):
    with open(self.filename, "r") as f:
        return list(csv.DictReader(f))
```

---

## 3. Results and Summary

### Results

- The game runs correctly in the terminal for both Human vs Human and Human vs AI modes
- All 4 OOP pillars are implemented and clearly visible in the code
- The Singleton pattern is used for `ResultSaver` to safely manage file access
- Game results are saved to `results.csv` and displayed at the end of the session
- 17 unit tests written with `unittest` — all pass

### Conclusions

This project produced a working Tic Tac Toe game built with object-oriented programming. Each class has one clear job: `Board` manages the grid, `Player` subclasses handle input, `ResultSaver` handles the file, and `Game` connects everything together.

The program correctly saves and loads game history using a CSV file. Future improvements could include:

- A smarter AI using the Minimax algorithm so the computer never loses
- A graphical interface using `tkinter`
- Tracking win/loss/draw counts per player name across sessions

---

## 4. Resources

- [Python `abc` module](https://docs.python.org/3/library/abc.html)
- [Python `csv` module](https://docs.python.org/3/library/csv.html)
- [Python `unittest` framework](https://docs.python.org/3/library/unittest.html)
- [PEP 8 style guide](https://pep8.org/)
- [Singleton pattern explained](https://refactoring.guru/design-patterns/singleton)
