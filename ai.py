import random
import copy
import math
from constants import *

class ConnectFourAI:
    def __init__(self, difficulty=HARD):
        self.difficulty = difficulty

    def choose_move(self, board):
        """Routes calculations depending on the configured difficulty tier."""
        valid_moves = board.get_valid_locations()
        if not valid_moves:
            return None

        if self.difficulty == EASY:
            return random.choice(valid_moves)
        
        elif self.difficulty == MEDIUM:
            return self._get_medium_move(board, valid_moves)
            
        elif self.difficulty == HARD:
            # Look ahead depth of 5 moves for optimal performance without web server timeout
            col, score = self._minimax(board, 5, -math.inf, math.inf, True)
            return col if col is not None else random.choice(valid_moves)

    def _get_medium_move(self, board, valid_moves):
        """Rule-based heuristic: Immediate wins/blocks, defaulting to the center."""
        # 1. Win if an immediate move exists
        for col in valid_moves:
            row = board.get_next_open_row(col)
            temp_board = copy.deepcopy(board)
            temp_board.drop_piece(row, col, AI)
            if temp_board.check_win(AI):
                return col

        # 2. Block immediate human win threats
        for col in valid_moves:
            row = board.get_next_open_row(col)
            temp_board = copy.deepcopy(board)
            temp_board.drop_piece(row, col, PLAYER)
            if temp_board.check_win(PLAYER):
                return col

        # 3. Prioritize center position
        center_col = COLS // 2
        if center_col in valid_moves:
            return center_col

        return random.choice(valid_moves)

    # --- MINIMAX CORE ENGINE ---
    def _evaluate_window(self, window, piece):
        score = 0
        opp_piece = PLAYER if piece == AI else AI

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
            score -= 4

        return score

    def _score_position(self, board, piece):
        score = 0
        # Center column bias
        center_array = [int(i) for i in list(board.grid[:, COLS//2])]
        score += center_array.count(piece) * 3

        # Horizontal Check
        for r in range(ROWS):
            row_array = [int(i) for i in list(board.grid[r, :])]
            for c in range(COLS - 3):
                window = row_array[c:c+4]
                score += self._evaluate_window(window, piece)

        # Vertical Check
        for c in range(COLS):
            col_array = [int(i) for i in list(board.grid[:, c])]
            for r in range(ROWS - 3):
                window = col_array[r:r+4]
                score += self._evaluate_window(window, piece)

        # Diagonals Check
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                window = [board.grid[r+i][c+i] for i in range(4)]
                score += self._evaluate_window(window, piece)

        for r in range(3, ROWS):
            for c in range(COLS - 3):
                window = [board.grid[r-i][c+i] for i in range(4)]
                score += self._evaluate_window(window, piece)

        return score

    def _is_terminal_node(self, board):
        return board.check_win(PLAYER) or board.check_win(AI) or len(board.get_valid_locations()) == 0

    def _minimax(self, board, depth, alpha, beta, maximizingPlayer):
        valid_locations = board.get_valid_locations()
        is_terminal = self._is_terminal_node(board)

        if depth == 0 or is_terminal:
            if is_terminal:
                if board.check_win(AI): return (None, 100000000)
                elif board.check_win(PLAYER): return (None, -10000000)
                else: return (None, 0)
            else:
                return (None, self._score_position(board, AI))

        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = board.get_next_open_row(col)
                b_copy = copy.deepcopy(board)
                b_copy.drop_piece(row, col, AI)
                new_score = self._minimax(b_copy, depth-1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta: break
            return column, value
        else:
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = board.get_next_open_row(col)
                b_copy = copy.deepcopy(board)
                b_copy.drop_piece(row, col, PLAYER)
                new_score = self._minimax(b_copy, depth-1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta: break
            return column, value
