import numpy as np
import pandas as pd
from connectFour import ConnectFour

class ConnectFourQLearning(ConnectFour):
    def __init__(self, learning_rate=0.1, discount_factor=0.99, exploration_rate=0.2):
        super().__init__()
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.q_table = {}

    def get_bot_move(self):
        state_key = self.get_state_key()
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.COLUMN_COUNT)
        
        if np.random.uniform(0, 1) < self.exploration_rate:
            valid_columns = [col for col in range(self.COLUMN_COUNT) if self.is_valid_location(col)]
            return np.random.choice(valid_columns)
        else:
            return np.argmax(self.q_table[state_key])

    def update_q_table(self, current_state_key, action, reward, next_state_key):
        if current_state_key not in self.q_table:
            self.q_table[current_state_key] = np.zeros(self.COLUMN_COUNT)
        if next_state_key not in self.q_table:
            self.q_table[next_state_key] = np.zeros(self.COLUMN_COUNT)

        current_q_value = self.q_table[current_state_key][action]
        max_next_q_value = np.max(self.q_table[next_state_key])

        self.q_table[current_state_key][action] = current_q_value + self.learning_rate * (reward + self.discount_factor * max_next_q_value - current_q_value)

    def get_state_key(self):
        return str(self.board)

    def save_q_table(self, filename):
        q_table_df = pd.DataFrame.from_dict(self.q_table, orient='index')
        q_table_df.to_csv(filename)

    def load_q_table(self, filename):
        q_table_df = pd.read_csv(filename, index_col=0)
        self.q_table = q_table_df.to_dict(orient='index')

    
