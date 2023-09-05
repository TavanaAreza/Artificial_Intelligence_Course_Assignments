import numpy as np
import copy
import time
from Board import BoardUtility
import random


class Player:
    def __init__(self, player_piece):
        self.piece = player_piece

    def play(self, board):
        return 0


class RandomPlayer(Player):
    def play(self, board):
        return [random.choice(BoardUtility.get_valid_locations(board)), random.choice([1, 2, 3, 4]), random.choice(["skip", "clockwise", "anticlockwise"])]


class HumanPlayer(Player):
    def play(self, board):
        move = input("row, col, region, rotation\n")
        move = move.split()
        print(move)
        return [[int(move[0]), int(move[1])], int(move[2]), move[3]]


class MiniMaxPlayer(Player):
    def __init__(self, player_piece, depth=5):
        super().__init__(player_piece)
        self.depth = depth

    def play(self, board):
        start_time = time.time() * 1000
        best_move = None
        best_score = float("-inf")
        alpha, beta = float("-inf"), float("inf")
        for move in BoardUtility.get_valid_locations(board):
            row, col = move
            for region in range(1, 5):
                for rotation in ["skip", "clockwise", "anticlockwise"]:
                    board_copy = copy.deepcopy(board)
                    BoardUtility.make_move(board_copy, row, col, region, rotation, self.piece)
                    score = self.minimax(board_copy, self.depth - 1, False, alpha, beta)
                    if score > best_score:
                        best_score = score
                        best_move = [move, region, rotation]
                    alpha = max(alpha, score)
                    if alpha >= beta:
                        break
                if alpha >= beta:
                    break
            if alpha >= beta:
                break
        print("Time taken: ", time.time() * 1000 - start_time)
        return [[row, col], region, rotation]

    def minimax(self, board, depth, alpha, beta, player_piece):
        if depth == 0 or BoardUtility.is_game_over(board):
            return BoardUtility.evaluate_board(board, player_piece)
        if player_piece == self.piece:
            best_score = float("-inf")
            for move in BoardUtility.get_valid_locations(board):
                row, col = move
                for region in range(1, 5):
                    for rotation in ["skip", "clockwise", "anticlockwise"]:
                        board_copy = copy.deepcopy(board)
                        BoardUtility.make_move(board_copy, row, col, region, rotation, player_piece)
                        score = self.minimax(board_copy, depth - 1, alpha, beta, BoardUtility.get_opponent_piece(player_piece))
                        best_score = max(score, best_score)
                        alpha = max(alpha, score)
                        if alpha >= beta:
                            break
                    if alpha >= beta:
                        break
                if alpha >= beta:
                    break
            return best_score
        else:
            best_score = float("inf")
            for move in BoardUtility.get_valid_locations(board):
                row, col = move
                for region in range(1, 5):
                    for rotation in ["skip", "clockwise", "anticlockwise"]:
                        board_copy = copy.deepcopy(board)
                        BoardUtility.make_move(board_copy, row, col, region, rotation, player_piece)
                        score = self.minimax(board_copy, depth - 1, alpha, beta, BoardUtility.get_opponent_piece(player_piece))
                        best_score = min(score, best_score)
                        beta = min(beta, score)
                        if alpha >= beta:
                            break
                    if alpha >= beta:
                        break
                if alpha >= beta:
                    break
            return best_score
    def evaluate(self, board, player_piece):
        if BoardUtility.is_game_over(board):
            if BoardUtility.get_winner(board) == player_piece:
                return 100000000
            elif BoardUtility.get_winner(board) == BoardUtility.get_opponent_piece(player_piece):
                return -100000000
            else:
                return 0
        score = 0
        score += self.get_score(board, player_piece)
        score -= self.get_score(board, BoardUtility.get_opponent_piece(player_piece))
        return score



class MiniMaxProbPlayer(Player):
    def __init__(self, player_piece, depth=5, prob_stochastic=0.1):
        super().__init__(player_piece)
        self.depth = depth
        self.prob_stochastic = prob_stochastic

    def play(self, board):
        if random.random() < self.prob_stochastic:
            return self.random_player.play(board)
        else:
            return self.mini_max_player.play(board)

    def future_move(board, move, piece):

        board_after_move = copy.deepcopy(board)
        row, col = move[0][0], move[0][1]
        board_after_move[row][col] = piece
        BoardUtility.rotate_region(board_after_move, move[1], move[2])
        return board_after_move

    def future_move_without_copy(board, move, piece):
        row, col = move[0][0], move[0][1]
        board[row][col] = piece
        BoardUtility.rotate_region(board, move[1], move[2])
        return board

    def backward_move(board, pre_move, piece):
        row, col = pre_move[0][0], pre_move[0][1]
        board[row][col] = 0
        BoardUtility.rotate_region(board, pre_move[1], BoardUtility.get_opposite_rotation(pre_move[2]))
        return board

    def get_opposite_rotation(rotation):
        if rotation == "clockwise":
            return "anticlockwise"
        elif rotation == "anticlockwise":
            return "clockwise"
        else:
            return "skip"

    def opponent_piece(piece):
        return abs(piece - 3)
