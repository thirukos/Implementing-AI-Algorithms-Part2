import numpy as np
import pygame
import sys
import math
from connectFour import ConnectFour
import numpy as np
import random

class ConnectFourBot(ConnectFour):
    def __init__(self):
        super().__init__()

    def get_bot_move(self, piece):
        you = piece + 1
        op = you % 2 + 1
        valid_cols = self.get_valid_locations()
        col_move = random.choice(valid_cols)

        ROW_COUNT = self.ROW_COUNT
        COLUMN_COUNT = self.COLUMN_COUNT
        board = self.board

        # Block horizontal
        for r in range(0, ROW_COUNT):
            row = []
            for c in range(0, COLUMN_COUNT - 4):
                row = [board[r][c], board[r][c + 1], board[r][c + 2], board[r][c + 3]]
                if row.count(op) == 3 and row.count(0) == 1:
                    if r == 0 or board[r - 1][c + row.index(0)] != 0:
                        col_move = c + row.index(0)

        # Block vertical
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT):
                if board[r][c] == op and board[r + 1][c] == op and board[r + 2][c] == op:
                    if r + 3 < ROW_COUNT and board[r + 3][c] == 0:
                        col_move = c

        # Block diagonal
        for r in range(ROW_COUNT - 3):
            for c in range(COLUMN_COUNT - 3):
                diag = [board[r][c], board[r + 1][c + 1], board[r + 2][c + 2], board[r + 3][c + 3]]
                if diag.count(op) == 3 and diag.count(0) == 1:
                    temp = c + diag.index(0)
                    if diag.index(0) == 0 and r == 0 or board[r + diag.index(0) - 1][temp] != 0:
                        col_move = temp

        # Block anti-diagonal
        for r in range(3, ROW_COUNT):
            for c in range(0, COLUMN_COUNT - 3):
                diag = [board[r][c], board[r - 1][c + 1], board[r - 2][c + 2], board[r - 3][c + 3]]
                if diag.count(op) == 3 and diag.count(0) == 1:
                    temp = c + diag.index(0)
                    if diag.index(0) == 3 and r == 0 or board[r - diag.index(0) - 1][temp] != 0:
                        col_move = temp

        return col_move

    def run_game(self):
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, self.background_color, (0, 0, self.width, self.SQUARESIZE))
                    posx = event.pos[0]
                    if self.turn == 0:
                        pygame.draw.circle(self.screen, self.player1_color, (posx, int(self.SQUARESIZE / 2)), self.RADIUS)
                    pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN and self.turn == 0:
                    pygame.draw.rect(self.screen, self.background_color, (0, 0, self.width, self.SQUARESIZE))
                    posx = event.pos[0]
                    col = int(math.floor(posx / self.SQUARESIZE))

                    if self.is_valid_location(col):
                        row = self.get_next_open_row(col)
                        self.drop_piece(row, col, 1)

                        if self.winning_move(1):
                            label = self.myfont.render("Player 1 wins!!", 1, self.player1_color)
                            self.screen.blit(label, (40, 10))
                            self.game_over = True

                        self.turn = 1

                if self.turn == 1 and not self.game_over:
                    col = self.get_bot_move(1)  # Pass the piece number for the bot
                    if col is not None:
                        row = self.get_next_open_row(col)
                        self.drop_piece(row, col, 2)

                        if self.winning_move(2):
                            label = self.myfont.render("Bot wins!!", 1, self.player2_color)
                            self.screen.blit(label, (40, 10))
                            self.game_over = True

                        self.turn = 0

                # self.print_board()
                self.draw_board()

                if self.game_over:
                    pygame.time.wait(3000)
