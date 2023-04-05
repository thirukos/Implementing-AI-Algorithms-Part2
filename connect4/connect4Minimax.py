import numpy as np
from copy import deepcopy
from connectFour import ConnectFour
from connetFourBot import ConnectFourBot
import pygame
import sys
import math

class ConnectFourMinimax(ConnectFour):
    def __init__(self, max_depth=3):
        super().__init__()
        self.max_depth = max_depth

    # def get_bot_move(self):
    #     valid_cols = [col for col in range(self.COLUMN_COUNT) if self.is_valid_location(col).any()]
    #     if not valid_cols:
    #         return np.random.randint(0, self.COLUMN_COUNT)
    #     _, col = self.minimax(self.max_depth, -np.inf, np.inf, True)
    #     return col
    
    def get_bot_move(self):
        valid_cols = [col for col in range(self.COLUMN_COUNT) if self.is_valid_location(col).any()]
        if not valid_cols:
            return np.random.randint(0, self.COLUMN_COUNT)
        _, col = self.minimax(self.max_depth, -np.inf, np.inf, True)
        while not self.is_valid_location(col).any():
            col = np.random.randint(0, self.COLUMN_COUNT)
        row = self.get_next_open_row(col)
        while row == -1:
            col = np.random.randint(0, self.COLUMN_COUNT)
            row = self.get_next_open_row(col)
        return col

    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.game_over:
            if self.winning_move(2):
                return (1000000, None)
            elif self.winning_move(1):
                return (-1000000, None)
            else:
                return (self.score_board(), None)

        if maximizing_player:
            value = -np.inf
            valid_moves = np.where(self.board[0] == 0)[0]
            if valid_moves.size == 0:
                return (value, None)
            col = np.random.choice(valid_moves)
            print(f"max - random column choice {col}")
            self.print_board()
            for c in range(self.COLUMN_COUNT):
                if self.is_valid_location(c).any():
                    r = self.get_next_open_row(c)
                    self.drop_piece(r, c, 2)
                    new_value, _ = self.minimax(depth - 1, alpha, beta, False)
                    self.drop_piece(r, c, 0)
                    if new_value > value:
                        value = new_value
                        col = c
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
            return (value, col)
        else:
            value = np.inf
            valid_moves = np.where(self.board[0] == 0)[0]
            if valid_moves.size == 0:
                return (value, None)
            col = np.random.choice(valid_moves)
            print(f"min - random column choice {col}")
            self.print_board()
            for c in range(self.COLUMN_COUNT):
                if self.is_valid_location(c).any():
                    r = self.get_next_open_row(c)
                    self.drop_piece(r, c, 1)
                    new_value, _ = self.minimax(depth - 1, alpha, beta, True)
                    self.drop_piece(r, c, 0)
                    if new_value < value:
                        value = new_value
                        col = c
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
            return (value, col)

    def score_board(self):
        score = 0
        # Check horizontal score
        for r in range(self.ROW_COUNT):
            row_array = [int(i) for i in list(self.board[r,:])]
            for c in range(self.COLUMN_COUNT-3):
                window = row_array[c:c+4]
                score += self.evaluate_window(window)
        # Check vertical score
        for c in range(self.COLUMN_COUNT):
            col_array = [int(i) for i in list(self.board[:,c])]
            for r in range(self.ROW_COUNT-3):
                window = col_array[r:r+4]
                score += self.evaluate_window(window)
        # Check diagonal score (down-right)
        for r in range(self.ROW_COUNT-3):
            for c in range(self.COLUMN_COUNT-3):
                window = [self.board[r+i][c+i] for i in range(4)]
                score += self.evaluate_window(window)
        # Check diagonal score (up-right)
        for r in range(3, self.ROW_COUNT):
            for c in range(self.COLUMN_COUNT-3):
                window = [self.board[r-i][c+i] for i in range(4)]
                score += self.evaluate_window(window)
        return score

    def evaluate_window(self, window):
        score = 0
        opp_piece = 1
        bot_piece = 2
        empty = 0
        if window.count(bot_piece) == 4:
            score += 100
        elif window.count(bot_piece) == 3 and window.count(empty) == 1:
            score += 5
        elif window.count(bot_piece) == 2 and window.count(empty) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(empty) == 1:
            score -= 4
        return score
    
    def run_game(self, mode = "p2a"):
        if mode == "p2a":
            while not self.game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.MOUSEMOTION:
                        pygame.draw.rect(self.screen, self.background_color, (0,0, self.width, self.SQUARESIZE))
                        posx = event.pos[0]
                        if self.turn == 0:
                            pygame.draw.circle(self.screen, self.player1_color, (posx, int(self.SQUARESIZE/2)), self.RADIUS)
                        else:
                            pygame.draw.circle(self.screen, self.player2_color, (posx, int(self.SQUARESIZE/2)), self.RADIUS)
                        pygame.display.update()
                    if event.type == pygame.MOUSEBUTTONDOWN and self.turn == 0:
                        pygame.draw.rect(self.screen, self.background_color, (0,0, self.width, self.SQUARESIZE))
                        posx = event.pos[0]
                        col = int(math.floor(posx/self.SQUARESIZE))

                        if self.is_valid_location(col).any():
                            row = self.get_next_open_row(col)
                            self.drop_piece(row, col, 1)

                            if self.winning_move(1):
                                label = self.myfont.render("Player wins!!", 1, self.player1_color)
                                self.screen.blit(label, (40,10))
                                self.game_over = True
                                # break
                            else:
                                self.turn += 1
                                self.turn = self.turn % 2
                        else:
                            continue
                    elif self.turn == 1:
                        col = self.get_bot_move()

                        if self.is_valid_location(col).any():
                            row = self.get_next_open_row(col)
                            self.drop_piece(row, col, 2)

                            if self.winning_move(2):
                                label = self.myfont.render("Minimax wins!!", 1, self.player2_color)
                                self.screen.blit(label, (40,10))
                                self.game_over = True
                                # break
                            self.turn += 1
                            self.turn = self.turn % 2

                    # self.print_board()
                    self.draw_board()


                    if self.game_over:
                        pygame.time.wait(3000)

        elif mode == "b2a":
            while not self.game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                # Player 1 move (Bot)
                if self.turn == 0:
                    col = ConnectFourBot.get_bot_move(self)
                    if self.is_valid_location(col).any():
                        row = self.get_next_open_row(col)
                        self.drop_piece(row, col, 1)
                        self.draw_board()
                        pygame.display.update()
                        pygame.time.wait(1000)

                        if self.winning_move(1):
                            label = self.myfont.render("Player wins!!", 1, self.player1_color)
                            self.screen.blit(label, (40, 10))
                            self.game_over = True
                        else:
                            self.turn += 1
                            self.turn = self.turn % 2

                # Player 2 move (Minimax)
                elif self.turn == 1:
                    col = self.get_bot_move()
                    if self.is_valid_location(col).any():
                        row = self.get_next_open_row(col)
                        self.drop_piece(row, col, 2)
                        self.draw_board()
                        pygame.display.update()
                        pygame.time.wait(1000)

                        if self.winning_move(2):
                            label = self.myfont.render("Minimax wins!!", 1, self.player2_color)
                            self.screen.blit(label, (40, 10))
                            self.game_over = True
                        else:
                            self.turn += 1
                            self.turn = self.turn % 2

                if self.game_over:
                    pygame.time.wait(3000)
            # pass
        