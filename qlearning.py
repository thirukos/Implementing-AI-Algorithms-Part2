import numpy as np
import random
import csv

class QLearningAgent:
    def __init__(self, alpha=0.5, gamma=0.9, epsilon=0.1):
        self.q_table = {}
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

    def get_state(self, board):
        return tuple(board.reshape(1, -1).flatten().tolist())

    def get_available_actions(self, board):
        return [i for i, x in enumerate(board.flatten()) if x == 0]

    def action_to_coordinates(self, action):
        row, col = divmod(action, 3)
        return row, col

    def update_q_table(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = np.zeros(9)

        if next_state not in self.q_table:
            self.q_table[next_state] = np.zeros(9)

        self.q_table[state][action] += self.alpha * (reward + self.gamma * np.max(self.q_table[next_state]) - self.q_table[state][action])
    
    def create_empty_q_table(self):
        self.q_table = {}

    # def choose_action(self, state, available_actions):
    #     if random.uniform(0, 1) < self.epsilon:
    #         return random.choice(available_actions)
    #     else:
    #         q_values = {action: self.q_table[state][action] for action in available_actions}
    #         return max(q_values, key=q_values.get)
    # def choose_action(self, state, available_actions):
    #     if state not in self.q_table:
    #         self.q_table[state] = {action: 0 for action in self.action_space}
            
    #     if np.random.rand() < self.epsilon:
    #         action = np.random.choice(available_actions)
    #     else:
    #         q_values = {action: self.q_table[state][action] for action in available_actions}
    #         max_q_value = max(q_values.values())
    #         best_actions = [action for action, q_value in q_values.items() if q_value == max_q_value]
    #         action = np.random.choice(best_actions)
    #     return action
    def choose_action(self, state, available_actions):
        if state not in self.q_table:
            self.q_table[state] = {action: 0 for action in available_actions}
            
        if np.random.rand() < self.epsilon:
            action = np.random.choice(available_actions)
        else:
            q_values = {action: self.q_table[state][action] for action in available_actions}
            max_q_value = max(q_values.values())
            best_actions = [action for action, q_value in q_values.items() if q_value == max_q_value]
            action = np.random.choice(best_actions)
        return action

    def train(self, board, num_episodes):
        for _ in range(num_episodes):
            game_over = False
            board.reset()

            while not game_over:
                state = self.get_state(board.board)
                available_actions = self.get_available_actions(board.board)
                action = self.choose_action(state, available_actions)
                row, col = self.action_to_coordinates(action)

                reward, game_over = board.mark_square(row, col, player=1)
                next_state = self.get_state(board.board)

                if game_over:
                    self.update_q_table(state, action, reward, next_state)
                    break

                available_actions = self.get_available_actions(board.board)
                if not available_actions:
                    break

                next_action = random.choice(available_actions)
                row, col = self.action_to_coordinates(next_action)

                _, game_over = board.mark_square(row, col, player=2)
                next_next_state = self.get_state(board.board)

                self.update_q_table(state, action, 0, next_next_state)

    def save_q_table(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for state, q_values in self.q_table.items():
                writer.writerow([state, *q_values])

    def load_q_table(self, filename):
        with open(filename, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                state = tuple(map(int, row[0][1:-1].split(',')))
                q_values = np.array(list(map(float, row[1:])))
                self.q_table[state] = q_values
