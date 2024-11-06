from Board import BoardUtility
import random
import copy
import time

ROWS = 6
COLS = 6


class Player:
    def __init__(self, player_piece):
        self.piece = player_piece

    def play(self, board):
        return 0


class RandomPlayer(Player):
    def play(self, board):
        return [random.choice(BoardUtility.get_valid_locations(board)), random.choice([1, 2, 3, 4]), random.choice(["skip", "clockwise", "anticlockwise"])]

class BoardHelp():
    @staticmethod
    def count_in_row(board, player_piece):
        count_four = 0
        count_three = 0
        # checking horizontally
        for c in range(3):
            for r in range(ROWS):
                if (board[r][c] == player_piece):
                    length = 1
                    for next_r in range(r, ROWS):
                        if (board[next_r][c]) == player_piece:
                            length +=1
                        else:
                            break
                    if (length == 3):
                        count_three += 1
                    if (length == 4):
                        count_four += 1
                        break
                    

        # checking vertically
        for r in range(2):
            for c in range(COLS):
                if (board[r][c] == player_piece):
                    length = 1
                    for next_c in range(c, COLS):
                        if (board[r][next_c]) == player_piece:
                            length += 1
                        else:
                            break
                    if (length == 3):
                        count_three += 1
                    if (length == 4):
                        count_four += 1
                        break
        
        return count_three, count_four
    
    @staticmethod
    def get_moves(board):
        moves = []
        for location in BoardUtility().get_valid_locations(board):
            for region in [1, 2, 3, 4]:
                for rotation in ["skip", "clockwise", "anticlockwise"]:
                    moves.append([location, region, rotation])
        random.shuffle(moves)
        return moves

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
        row = -1
        col = -1
        region = -1
        rotation = -1
        # Todo: implement minimax algorithm
        final_move = [[row, col], region, rotation]
        maxUtility = float('-inf')
        alpha_beta = [float('-inf'), float('inf')]
        for move in BoardHelp().get_moves(board):
            location = move[0]
            region = move[1]
            rotation = move[2]
            board_copy = copy.deepcopy(board)
            BoardUtility().make_move(
                board_copy, location[0], location[1], region, rotation, 1)
            if (BoardUtility().is_terminal_state(board_copy)):
                value = self.Utility(board_copy)
                if (value == 100):
                    return move
            else:
                value = self.min_value(board_copy, alpha_beta, self.depth - 1)
            if (value > maxUtility):
                maxUtility = value
                final_move = move
        return final_move

    def Utility(self, board):
        if (BoardUtility().has_player_won(board, 1)):
            return 100
        if (BoardUtility().has_player_won(board, 2)):
            return -100
        if (BoardUtility().is_draw(board)):
            return 0

    def heuristic(self, board):
        h = 0
        for row, column in [(1, 1), (4, 1), (1, 4), (4, 4)]:
            if (board[row][column] != 0):
                if (board[row][column] == 1):
                    h += 20
                else:
                    h -= 10
        count_player = BoardHelp().count_in_row(board, 1)
        count_opponent = BoardHelp().count_in_row(board, 2)
        h += 3 * count_player[0]
        h += 4 * count_player[1]
        h -= 3 * count_opponent[0]
        h -= 4 * count_opponent[1]
        return h

    def min_value(self, board, alpha_beta, depth):
        if (BoardUtility().is_terminal_state(board)):
            return self.Utility(board)
        if (depth == 0):
            return self.heuristic(board)
        v = float('inf')
        moves = BoardHelp().get_moves(board)
        for move in moves:
            location = move[0]
            region = move[1]
            rotation = move[2]
            board_copy = copy.deepcopy(board)
            BoardUtility().make_move(
                board_copy, location[0], location[1], region, rotation, 2)
            v = min(v, self.max_value(board_copy, alpha_beta, depth - 1))
            if (v >= alpha_beta[1]):
                return v
            alpha_beta[1] = min(alpha_beta[1], v)
        return v

    def max_value(self, board, alpha_beta, depth):
        if (BoardUtility().is_terminal_state(board)):
            return self.Utility(board)
        if (depth == 0):
            return self.heuristic(board)
        v = float('-inf')
        moves = BoardHelp().get_moves(board)
        for move in moves:
            location = move[0]
            region = move[1]
            rotation = move[2]
            board_copy = copy.deepcopy(board)
            BoardUtility().make_move(
                board_copy, location[0], location[1], region, rotation, 1)
            v = max(v, self.min_value(board_copy, alpha_beta, depth - 1))
            if (v <= alpha_beta[0]):
                return v
            alpha_beta[0] = max(alpha_beta[0], v)
        return v


class MiniMaxProbPlayer(Player):
    def __init__(self, player_piece, depth=5, prob_stochastic=0.1):
        super().__init__(player_piece)
        self.depth = depth
        self.prob_stochastic = prob_stochastic

    def play(self, board):
        row = -1
        col = -1
        region = -1
        rotation = -1
        # Todo: implement minimaxProb algorithm
        moves = BoardHelp().get_moves(board)
        if (random.random() < self.prob_stochastic):
            return random.choice(moves)
        final_move = [[row, col], region, rotation]
        maxUtility = float('-inf')
        alpha_beta = [float('-inf'), float('inf')]
        for move in BoardHelp().get_moves(board):
            location = move[0]
            region = move[1]
            rotation = move[2]
            board_copy = copy.deepcopy(board)
            BoardUtility().make_move(
                board_copy, location[0], location[1], region, rotation, 1)
            if (BoardUtility().is_terminal_state(board_copy)):
                value = self.Utility(board_copy)
                if (value == 100):
                    return move
            else:
                value = self.min_value(board_copy, alpha_beta, self.depth - 1)
            if (value > maxUtility):
                maxUtility = value
                final_move = move
        return final_move

    def Utility(self, board):
        if (BoardUtility().has_player_won(board, 1)):
            return 100
        if (BoardUtility().has_player_won(board, 2)):
            return -100
        if (BoardUtility().is_draw(board)):
            return 0

    def heuristic(self, board):
        h = 0
        for row, column in [(1, 1), (4, 1), (1, 4), (4, 4)]:
            if (board[row][column] != 0):
                if (board[row][column] == 1):
                    h += 20
                else:
                    h -= 10
        count_player = BoardHelp().count_in_row(board, 1)
        count_opponent = BoardHelp().count_in_row(board, 2)
        h += 3 * count_player[0]
        h += 4 * count_player[1]
        h -= 3 * count_opponent[0]
        h -= 4 * count_opponent[1]
        return h

    def min_value(self, board, alpha_beta, depth):
        if (BoardUtility().is_terminal_state(board)):
            return self.Utility(board)
        if (depth == 0):
            return self.heuristic(board)
        v = float('inf')
        moves = BoardHelp().get_moves(board)
        for move in moves:
            location = move[0]
            region = move[1]
            rotation = move[2]
            board_copy = copy.deepcopy(board)
            BoardUtility().make_move(
                board_copy, location[0], location[1], region, rotation, 2)
            v = min(v, self.max_value(board_copy, alpha_beta, depth - 1))
            if (v >= alpha_beta[1]):
                return v
            alpha_beta[1] = min(alpha_beta[1], v)
        return v

    def max_value(self, board, alpha_beta, depth):
        if (BoardUtility().is_terminal_state(board)):
            return self.Utility(board)
        if (depth == 0):
            return self.heuristic(board)
        v = float('-inf')
        moves = BoardHelp().get_moves(board)
        if (random.random() < self.prob_stochastic):
            move = random.choice(moves)
            location = move[0]
            region = move[1]
            rotation = move[2]
            board_copy = copy.deepcopy(board)
            BoardUtility().make_move(
                board_copy, location[0], location[1], region, rotation, 1)
            return self.min_value(board_copy, alpha_beta, depth - 1)
        for move in moves:
            location = move[0]
            region = move[1]
            rotation = move[2]
            board_copy = copy.deepcopy(board)
            BoardUtility().make_move(
                board_copy, location[0], location[1], region, rotation, 1)
            v = max(v, self.min_value(board_copy, alpha_beta, depth - 1))
            if (v <= alpha_beta[0]):
                return v
            alpha_beta[0] = max(alpha_beta[0], v)
        return v
