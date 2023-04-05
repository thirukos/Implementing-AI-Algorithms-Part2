import numpy as np
import pygame
import sys
import math
from connectFour import ConnectFour
import random

class ConnectFourBot(ConnectFour):
    def __init__(self, piece):
        super().__init__()
        self.piece = piece
        self.opponent_piece = self.piece % 2 + 1

    def get_bot_move(self):
        valid_cols = self.get_valid_locations()
        col_move = random.choice(valid_cols)
        
        def find_move(board, piece):
            ROW_COUNT = len(board)
            COLUMN_COUNT = len(board[0])

            for r in range(ROW_COUNT):
                for c in range(COLUMN_COUNT - 3):
                    row = [board[r][c], board[r][c+1], board[r][c+2], board[r][c+3]]
                    if row.count(piece) == 3 and row.count(0) == 1:
                        if r == 0 or board[r-1][c + row.index(0)] != 0:
                            return c + row.index(0)

            for r in range(ROW_COUNT - 3):
                for c in range(COLUMN_COUNT):
                    col = [board[r][c], board[r+1][c], board[r+2][c], board[r+3][c]]
                    if col.count(piece) == 3 and col.count(0) == 1:
                        if board[r+3][c] == 0:
                            return c

            for r in range(ROW_COUNT - 3):
                for c in range(COLUMN_COUNT - 3):
                    diag = [board[r][c], board[r+1][c+1], board[r+2][c+2], board[r+3][c+3]]
                    if diag.count(piece) == 3 and diag.count(0) == 1:
                        if r == 0 or board[r+diag.index(0)-1][c+diag.index(0)] != 0:
                            return c + diag.index(0)

            for r in range(3, ROW_COUNT):
                for c in range(COLUMN_COUNT - 3):
                    anti_diag = [board[r][c], board[r-1][c+1], board[r-2][c+2], board[r-3][c+3]]
                    if anti_diag.count(piece) == 3 and anti_diag.count(0) == 1:
                        if r == 3 or board[r-anti_diag.index(0)-1][c+anti_diag.index(0)] != 0:
                            return c + anti_diag.index(0)

            return None

        # Block opponent's moves
        block_move = find_move(self.board, self.opponent_piece)
        if block_move is not None:
            col_move = block_move

        # Make own winning move
        winning_move = find_move(self.board, self.piece)
        if winning_move is not None:
            col_move = winning_move

        return col_move

    def run_game(self):
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
                            label = self.myfont.render("Player 1 wins!!", 1, self.player1_color)
                            self.screen.blit(label, (40,10))
                            self.game_over = True
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
                            label = self.myfont.render("Bot wins!!", 1, self.player2_color)
                            self.screen.blit(label, (40,10))
                            self.game_over = True
                        self.turn += 1
                        self.turn = self.turn % 2

                # self.print_board()
                self.draw_board()


                if self.game_over:
                    pygame.time.wait(3000)
