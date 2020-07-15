#!/usr/bin/env python3
import argparse
import sys
from time import time
import multiprocessing

from io import StringIO

DEPTH = 5
DONT_SCORE_ONE = True


def compute(x):
    move_sequence, board = x
    return [x + 1 for x in move_sequence], board.mini_max(DEPTH)


class Board:
    PLAYER_SCORE_HOLDER = 7

    def __str__(self, *args, **kwargs):
        return str(self.board)

    def __repr__(self, *args, **kwargs):
        return "Board%s" % self.__str__()

    @property
    def player_points(self):
        if self.no_more_moves():
            return sum(self.board[1:8])
        else:
            return self.board[7]

    @property
    def opponent_points(self):
        if self.no_more_moves():
            return self.board[0] + sum(self.board[8:])
        else:
            return self.board[0]

    def __init__(self, board=None):
        if board is not None:
            self.board = board.board[:]
            self.reversed = board.reversed
        else:
            self.board = [0, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4]
            self.reversed = False

    def make_player_move(self, n):
        assert n < 6
        n += 1
        tokens = self.board[n]
        assert tokens > 0
        self.board[n] = 0
        while tokens:
            tokens -= 1
            n += 1
            if n >= len(self.board):
                n = 1
            self.board[n] += 1

        if n == self.PLAYER_SCORE_HOLDER:
            return True

        if self.board[n] == 1 and 0 < n < 7:
            oponent_pos = len(self.board) - n
            if DONT_SCORE_ONE is False or (
                DONT_SCORE_ONE is True and self.board[oponent_pos] != 0
            ):
                self.board[n] = 0
                self.board[self.PLAYER_SCORE_HOLDER] += 1 + self.board[oponent_pos]
                self.board[oponent_pos] = 0

        return False

    def possible_player_moves(self):
        for i, a in enumerate(self.board[1:7]):
            if a > 0:
                yield i

    def get_player_moves(self, pos, seq, moves):
        assert self.board[1 + pos] != 0

        new_board = Board(self)
        move_continue = new_board.make_player_move(pos)
        if move_continue and list(new_board.possible_player_moves()):

            for i in new_board.possible_player_moves():
                new_board.get_player_moves(i, seq + [pos], moves)
        else:
            moves.append((seq + [pos], new_board))
            return

    def find_all_moves(self):
        all_moves = []
        for i in self.possible_player_moves():
            self.get_player_moves(i, [], all_moves)

        return all_moves

    def get_opponent_board(self):
        b = Board()
        b.board = self.board[7:] + self.board[:7]
        b.reversed = not self.reversed
        return b

    def no_more_moves(self):
        if any(self.board[8:]) == False or any(self.board[1:7]) == False:
            return True
        return False

    def mini_max(self, depth=2, maximizing_player=False):
        if depth == 0 or self.no_more_moves():
            return self.get_heurestic_score()

        if maximizing_player:
            best_value = -999
            for move, board in self.get_opponent_board().find_all_moves():
                val = board.mini_max(depth - 1, not maximizing_player)
                best_value = max(best_value, val)
            return best_value
        else:
            best_value = 999
            for move, board in self.get_opponent_board().find_all_moves():
                val = board.mini_max(depth - 1, not maximizing_player)
                best_value = min(best_value, val)
            return best_value

    def mini_max_alpha_beta(
        self, depth=2, alpha=-999, beta=+999, maximizing_player=False
    ):
        if depth == 0 or self.no_more_moves():
            return self.get_heurestic_score()

        if maximizing_player:
            best_value = -999
            for move, board in self.get_opponent_board().find_all_moves():
                best_value = max(
                    best_value,
                    board.mini_max(depth - 1, alpha, beta, not maximizing_player),
                )
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value
        else:
            best_value = 999
            for move, board in self.get_opponent_board().find_all_moves():
                best_value = min(
                    best_value, board.mini_max(depth - 1, not maximizing_player)
                )
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value

    def find_best_move(self):
        print("Calculating best move...")
        t = time()

        def moves():
            with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
                yield from pool.map(compute, list(self.find_all_moves()))

        result = sorted(moves(), key=lambda x: x[1], reverse=True)[:1]
        print("Calculated in %.1fs" % (time() - t))
        return result

    def print(self):
        print("         ", end="")
        print(*["%2d" % x for x in reversed(self.board[8:])], sep="|")
        print(
            "AI --> %2d                  %2d <-- You"
            % (self.opponent_points, self.player_points)
        )
        print("         ", end="")
        print(*["%2d" % x for x in self.board[1:7]], sep="|")
        print("")
        print("          ^  ^  ^  ^  ^  ^")
        print("moves:    1  2  3  4  5  6")

    def string(self):
        result = StringIO()
        print("         ", end="", file=result)
        print(*["%2d" % x for x in reversed(self.board[8:])], sep="|", file=result)
        print(
            "AI --> %2d                  %2d <-- You"
            % (self.opponent_points, self.player_points),
            file=result,
        )
        print("         ", end="", file=result)
        print(*["%2d" % x for x in self.board[1:7]], sep="|", file=result)
        return result.getvalue()

    def get_heurestic_score(self):
        if not self.reversed:
            return self.player_points - self.opponent_points
        else:
            return self.opponent_points - self.player_points


def player_move(board):
    has_move = True
    while has_move:
        command = input("Player move: ").split()
        if not command:
            continue
        if command[0] == "q":
            sys.exit(0)

        try:
            c = int(command[0])
            has_move = board.make_player_move(c - 1)
            board.print()
        except:
            print("Wrong move: ", command[0])
            continue

    return board


def opponent_move(board):
    board = board.get_opponent_board()
    has_move = True
    while has_move:
        command = input("Opponent move: ").split()
        if not command:
            continue
        if command[0] == "q":
            sys.exit(0)
        try:
            c = int(command[0])
            has_move = board.make_player_move(c - 1)
            board.get_opponent_board().print()
        except:
            print("Wrong move: ", command[0])
            continue

    return board.get_opponent_board()


def run_game(initial_board=None, player_starts=True):
    board = Board()

    if initial_board is not None:  # Instantiate a board
        board.board = initial_board

    board.print()  # Show the user the starting board
    while 1:
        if player_starts:  # Player means the AI
            for (
                best_move
            ) in (
                board.find_best_move()
            ):  # Calcualte the best move and show it to the user
                print(best_move)
            board = player_move(board)
            board = opponent_move(board)
        else:
            board = opponent_move(board)
            for best_move in board.find_best_move():
                print(best_move)
            board = player_move(board)

        if board.no_more_moves():
            print("Games ended")
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mancala AI")
    parser.add_argument(
        "-b",
        "--board",
        type=int,
        nargs=14,
        default=None,
        help="Board layout, e.g 0 4 4 4 4 4 4 0 4 4 4 4 4 4",
    )
    parser.add_argument("-d", "--depth", type=int, default=5)
    parser.add_argument("-o", "--opponent-starts", default=False, action="store_true")
    parser.add_argument("--dont-score-one", default=False, action="store_true")
    args = parser.parse_args()

    DEPTH = args.depth
    DONT_SCORE_ONE = args.dont_score_one

    run_game(args.board, not args.opponent_starts)
