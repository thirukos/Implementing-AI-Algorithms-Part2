import numpy as np
import random
import pygame
import sys
import math
import os
import pickle
import matplotlib.pyplot as plt

BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4
SQUARESIZE = 100
RADIUS = int(SQUARESIZE/2 - 5)
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

screen = pygame.display.set_mode(size)

epsilon_start = 1.0
min_epsilon = 0.01
epsilon_decay = 0.999

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
    # return -1

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == piece
            ):
                return True

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c : c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r : r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score negative sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def is_terminal_node(board):
    return (
        winning_move(board, PLAYER_PIECE)
        or winning_move(board, AI_PIECE)
        or len(get_valid_locations(board)) == 0
    )

def get_bot_move(board, piece):
    opponent_piece = piece % 2 + 1

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
    block_move = find_move(board, opponent_piece)
    if block_move is not None:
        col_move = block_move
    else:
        valid_cols = get_valid_locations(board)
        col_move = random.choice(valid_cols)

    # Make own winning move
    winning_move = find_move(board, piece)
    if winning_move is not None:
        col_move = winning_move

    return col_move

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value
    
def state_to_tuple(board):
    return tuple(map(tuple, board))

def qlearning(board, episodes, alpha=0.3, gamma=0.7, epsilon=0.9, validation_interval=10, save_file='qtable.pkl'):
    qtable = dict()
    training_rewards = []
    validation_rewards = []
    path = "Implementing-AI-Algorithms-Part2\connect4\\"
#Implementing-AI-Algorithms-Part2\connect4\connectFour_AI.py
    for episode in range(episodes):
        board = create_board()
        game_over = False
        turn = random.randint(PLAYER, AI)
        episode_reward = 0
        epsilon = max(epsilon * epsilon_decay, min_epsilon)
        while not game_over:
            if turn == AI:
                col = choose_best_action(qtable, board, AI_PIECE, epsilon)
                row = get_next_open_row(board, col)
                if row != -1:
                    drop_piece(board, row, col, AI_PIECE)
                if winning_move(board, AI_PIECE):
                    reward = 1
                    game_over = True
                elif is_terminal_node(board):
                    reward = 0
                    game_over = True
                else:
                    reward = 0
                    game_over = False

                next_board = board.copy()
                key = next_board.tostring()
                if key in qtable:
                    next_q_value = qtable[key]
                else:
                    next_q_value = 0

                current_board = board.copy()
                key = current_board.tostring()
                if key in qtable:
                    current_q_value = qtable[key]
                else:
                    current_q_value = 0

                new_q_value = current_q_value + alpha * (reward + gamma * next_q_value - current_q_value)
                qtable[key] = new_q_value
                episode_reward += reward

                turn += 1
                turn = turn % 2

            else:  # PLAYER's turn
                col = get_bot_move(board, PLAYER_PIECE)
                row = get_next_open_row(board, col)
                if row != -1:
                    drop_piece(board, row, col, PLAYER_PIECE)

                if winning_move(board, PLAYER_PIECE):
                    game_over = True
                elif is_terminal_node(board):
                    game_over = True

                turn += 1
                turn = turn % 2

        training_rewards.append(episode_reward)

        if episode % validation_interval == 0:
            validation_reward_sum = 0  # Initialize the sum of validation rewards for this interval
            for _ in range(10):
                validation_board = create_board()
                validation_game_over = False
                validation_turn = random.randint(PLAYER, AI)

                while not validation_game_over:
                    if validation_turn == AI:
                        col = choose_best_action(qtable, validation_board, AI_PIECE, epsilon)
                        row = get_next_open_row(validation_board, col)
                        if row != -1:
                            drop_piece(board, row, col, AI_PIECE)
                        # drop_piece(validation_board, row, col, AI_PIECE)
                        if winning_move(validation_board, AI_PIECE):
                            reward = 1
                            validation_game_over = True
                        elif is_terminal_node(validation_board):
                            reward = 0
                            validation_game_over = True
                        else:
                            reward = 0
                            validation_game_over = False

                        validation_turn += 1
                        validation_turn = validation_turn % 2

                    else:  # PLAYER's turn
                        col = get_bot_move(validation_board, PLAYER_PIECE)
                        row = get_next_open_row(validation_board, col)
                        if row != -1:
                            drop_piece(validation_board, row, col, PLAYER_PIECE)

                        if winning_move(validation_board, PLAYER_PIECE):
                            validation_game_over = True
                        elif is_terminal_node(validation_board):
                            validation_game_over = True

                        validation_turn += 1
                        validation_turn = validation_turn % 2

                validation_reward_sum += reward  # Add the reward from this validation game to the sum
            validation_reward = validation_reward_sum / 10  # Calculate the average validation reward for this interval
            validation_rewards.append(validation_reward)

        if episode % 100 == 0:
            print(f"Episode: {episode}, Training Reward: {episode_reward}, Validation Reward: {validation_reward}")

    with open(os.path.join(path, save_file), 'wb') as f:
        pickle.dump(qtable, f)

    return qtable, training_rewards, validation_rewards

def board_to_key(board):
    key = ''
    for row in board:
        for cell in row:
            key += str(cell)
    return key

def choose_action(qtable, board, piece, col):
    temp_board = board.copy()
    row = get_next_open_row(temp_board, col)
    
    if row is not None:
        drop_piece(temp_board, row, col, piece)
        key = temp_board.tostring()

        if key in qtable:
            return qtable[key]
    return 0

# def choose_best_action(qtable, board, piece, epsilon=0.2):
#     if np.random.random() < epsilon:
#         return random.randint(0, COLUMN_COUNT - 1)
#     else:
#         actions = [choose_action(qtable, board, piece, col) for col in range(COLUMN_COUNT)]
#         return np.argmax(actions)
def choose_best_action(qtable, board, piece, epsilon):
    valid_locations = get_valid_locations(board)
    max_q_value = float('-inf')
    best_action = random.choice(valid_locations)

    if random.random() < epsilon:
        return best_action  # Choose a random action (exploration)

    for col in valid_locations:
        temp_board = board.copy()
        row = get_next_open_row(temp_board, col)
        drop_piece(temp_board, row, col, piece)
        key = temp_board.tostring()

        if key in qtable:
            q_value = qtable[key]
        else:
            q_value = 0

        if q_value > max_q_value:
            max_q_value = q_value
            best_action = col

    return best_action


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

def plot_learning_curves(training_rewards, validation_rewards):
    plt.figure()
    plt.plot(training_rewards, label='Training')
    plt.plot(validation_rewards, label='Validation')
    plt.xlabel('Episodes')
    plt.ylabel('Rewards')
    plt.title('Learning Curves')
    plt.legend()
    # plt.show()
    plt.savefig('training vs validation')

# plot_learning_curves(training_rewards, validation_rewards)

def player_vs_bot():
    pygame.display.set_caption('ConnectFour-Player vs Bot')
    board = create_board()
    print_board(board)
    game_over = False

    pygame.init()
    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 25, bold= True)

    turn = random.randint(PLAYER, AI)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                        if winning_move(board, PLAYER_PIECE):
                            label = myfont.render("Human wins!!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                        turn += 1
                        turn = turn % 2

                        print_board(board)
                        draw_board(board)

        if turn == AI and not game_over:
            col = get_bot_move(board, PLAYER_PIECE)
            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    label = myfont.render("Bot wins!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(3000)

def player_vs_minimax():
    pygame.display.set_caption('ConnectFour-Player vs Minimax')
    board = create_board()
    print_board(board)
    game_over = False

    pygame.init()
    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 25, bold= True)

    turn = random.randint(PLAYER, AI)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                        if winning_move(board, PLAYER_PIECE):
                            label = myfont.render("Human wins!!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                        turn += 1
                        turn = turn % 2

                        print_board(board)
                        draw_board(board)

        if turn == AI and not game_over:
            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    label = myfont.render("Minimax wins!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(3000)

def minimax_vs_minimax():
    pygame.display.set_caption('ConnectFour-Minimax vs Minimax')
    board = create_board()
    print_board(board)
    game_over = False

    pygame.init()

    SQUARESIZE = 100

    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT + 1) * SQUARESIZE

    size = (width, height)

    RADIUS = int(SQUARESIZE / 2 - 5)

    screen = pygame.display.set_mode(size)
    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 25, bold= True)

    turn = AI

    while not game_over:
        if turn == AI and not game_over:
            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    label = myfont.render("Bot wins!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(3000)

def player_vs_qlearning(episode = 5000, qtable_file='qtable.pkl'):
    pygame.display.set_caption('ConnectFour-Player vs Q-Learning')
    board = create_board()
    print_board(board)
    game_over = False

    pygame.init()
    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 25, bold=True)

    turn = random.randint(PLAYER, AI)

    # Load or train the Q-table
    path = "Implementing-AI-Algorithms-Part2\connect4\\"
    if os.path.isfile(path + qtable_file):
        with open(path + qtable_file, 'rb') as f:
            qtable = pickle.load(f)
    else:
        qtable, training_rewards, validation_rewards = qlearning(create_board(), episode)
        plot_learning_curves(training_rewards, validation_rewards)
        with open(os.path.join(path, qtable_file), 'wb') as f:
            pickle.dump(qtable, f)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == PLAYER:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, PLAYER_PIECE)

                        if winning_move(board, PLAYER_PIECE):
                            label = myfont.render("Human wins!!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                        turn += 1
                        turn = turn % 2

                        print_board(board)
                        draw_board(board)

        if turn == AI and not game_over:
            # Use the Q-table to choose the best action
            col = choose_best_action(qtable, board, AI_PIECE, epsilon = 0.1)
            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    label = myfont.render("Q-Learning wins!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                print_board(board)
                draw_board(board)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(3000)
            
def bot_vs_minimax(board):
    pygame.display.set_caption('ConnectFour-Bot vs Minimax')
    game_over = False

    pygame.init()

    screen = pygame.display.set_mode(size)
    draw_board(board)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 25, bold= True)
    BOT = 0
    ALGO = 1

    turn = random.randint(BOT, ALGO)

    while not game_over:
        if turn == BOT and not game_over:
            col = get_bot_move(board, PLAYER_PIECE)
            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)

                if winning_move(board, PLAYER_PIECE):
                    label = myfont.render("Bot wins!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                draw_board(board)

                turn += 1
                turn = turn % 2

        if turn == ALGO and not game_over:
            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    label = myfont.render("Minimax wins!!", 1, YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                draw_board(board)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(3000)

if __name__ == '__main__':
    board = create_board()
    # player_vs_bot()
    # player_vs_minimax()
    player_vs_qlearning()
    # bot_vs_minimax(board)
