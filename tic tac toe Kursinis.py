

from abc import ABC, abstractmethod
import csv
import os


# ABSTRACTION
class Player(ABC):
    def __init__(self, name, symbol):
        self._name = name      # ENCAPSULATION
        self._symbol = symbol

    @property
    def name(self):
        return self._name

    @property
    def symbol(self):
        return self._symbol

    @abstractmethod
    def make_move(self, board):
        pass



# INHERITANCE + POLYMORPHISM:
class HumanPlayer(Player):
    def make_move(self, board):
        while True:
            try:
                pos = int(input(f"{self._name} ({self._symbol}), pick 1-9: ")) - 1
                if 0 <= pos <= 8 and board.is_empty(pos):
                    return pos
                print("Invalid. Try again.")
            except ValueError:
                print("Enter a number.")


class AIPlayer(Player):
    def make_move(self, board):
        for i in range(9):
            if board.is_empty(i):
                print(f"{self._name} picks position {i + 1}")
                return i


# ENCAPSULATION
class Board:
    def __init__(self):
        self.__cells = [" "] * 9

    def show(self):
        c = self.__cells
        print(f"\n {c[0]} | {c[1]} | {c[2]} ")
        print("---+---+---")
        print(f" {c[3]} | {c[4]} | {c[5]} ")
        print("---+---+---")
        print(f" {c[6]} | {c[7]} | {c[8]} \n")

    def place(self, pos, symbol):
        self.__cells[pos] = symbol

    def is_empty(self, pos):
        return self.__cells[pos] == " "

    def is_full(self):
        return " " not in self.__cells

    def get_winner(self):
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],   # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],   # columns
            [0, 4, 8], [2, 4, 6],              # diagonals
        ]
        for a, b, c in lines:
            if self.__cells[a] == self.__cells[b] == self.__cells[c] != " ":
                return self.__cells[a]
        return None

    def reset(self):
        self.__cells = [" "] * 9

    def get_cells(self):
        return self.__cells.copy()



# SINGLETON PATTERN
class ResultSaver:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.filename = "results.csv"
            cls._instance._create_file()
        return cls._instance

    def _create_file(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w", newline="") as f:
                csv.writer(f).writerow(["Game", "Winner"])

    def save(self, game_num, winner):
        with open(self.filename, "a", newline="") as f:
            csv.writer(f).writerow([game_num, winner])

    def load(self):
        with open(self.filename, "r") as f:
            return list(csv.DictReader(f))


# COMPOSITION + AGGREGATION:
class Game:
    def __init__(self, player1, player2):
        self.__board = Board()               # Composition
        self.__players = [player1, player2]  # Aggregation
        self.__saver = ResultSaver()         # Singleton
        self.__game_num = 1

    def play(self):
        print("\nWelcome to Tic Tac Toe!")
        print("Positions:\n 1|2|3\n 4|5|6\n 7|8|9\n")

        while True:
            self.__board.reset()
            self.__board.show()
            turn = 0

            while True:
                player = self.__players[turn % 2]
                pos = player.make_move(self.__board)
                self.__board.place(pos, player.symbol)
                self.__board.show()

                winner_symbol = self.__board.get_winner()
                if winner_symbol:
                    winner = self.__players[turn % 2]
                    print(f"{winner.name} wins!")
                    self.__saver.save(self.__game_num, winner.name)
                    break

                if self.__board.is_full():
                    print("It's a draw!")
                    self.__saver.save(self.__game_num, "Draw")
                    break

                turn += 1

            self.__game_num += 1

            if input("Play again? (yes/no): ").strip().lower() != "yes":
                self.__print_history()
                break

    def __print_history(self):
        print("\n--- Results ---")
        for row in self.__saver.load():
            print(f"Game {row['Game']}: {row['Winner']}")





# START
if __name__ == "__main__":
    print("1. Human vs Human")
    print("2. Human vs AI")
    choice = input("Choose: ").strip()

    p1 = HumanPlayer("Player 1", "X")
    p2 = AIPlayer("Computer", "O") if choice == "2" else HumanPlayer("Player 2", "O")

    Game(p1, p2).play()