import pygame
from connectFour import ConnectFour # connect 4 game class
from connectFourBot import ConnectFourBot
from connect4Minimax import ConnectFourMinimax

def p2p():
    game = ConnectFour()
    game.draw_board()
    game.run_game()

def p2b():
    game = ConnectFourBot()
    game.draw_board()
    game.run_game()

def p2MM():
    game = ConnectFourMinimax()
    game.draw_board()
    game.run_game()

def b2MM():
    game = ConnectFourMinimax()
    game.draw_board()
    game.run_game_bot_vs_minimax

if __name__ == '__main__':
    pygame.init()
    # p2p()
    # p2b()
    # p2MM()
    b2MM()
    pygame.quit()