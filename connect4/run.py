import pygame
from connectFour import ConnectFour # connect 4 game class
from connetFourBot import ConnectFourBot
from connect4Minimax import ConnectFourMinimax
import minimax

def player_vs_player():
    game = ConnectFour()
    game.draw_board()
    game.run_game()

def player_vs_bot():
    game = ConnectFourBot(1)
    game.draw_board()
    game.run_game()

def player_vs_minimaxAlgo():
    game = ConnectFourMinimax()
    game.draw_board()
    game.run_game()

def bot_vs_minimaxAlgo():
    game = ConnectFourMinimax()
    game.draw_board()
    game.run_bot_vs_algorithm(bot_piece=1)

if __name__ == '__main__':
    pygame.init()
    player_vs_player()
    # player_vs_bot()
    # player_vs_minimaxAlgo()
    # bot_vs_minimaxAlgo()
    pygame.quit()