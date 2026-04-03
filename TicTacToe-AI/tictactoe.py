import math
import time

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        print("Board structure (0-8):")
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')
        print()

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # check row
        row_ind = square // 3
        row = self.board[row_ind*3 : (row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True

        # check column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        # check diagonals
        if square % 2 == 0:
            diagonal1 = [self.board[0], self.board[4], self.board[8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[2], self.board[4], self.board[6]]
            if all([spot == letter for spot in diagonal2]):
                return True

        return False


def minimax(state, depth, alpha, beta, is_maximizing, ai_letter, human_letter):
    """
    Minimax algorithm with Alpha-Beta Pruning.
    """
    # Base cases: Check if previous move resulted in a win/loss or draw
    if state.current_winner == ai_letter:
        return {'position': None, 'score': 1 * (state.num_empty_squares() + 1)}
    elif state.current_winner == human_letter:
        return {'position': None, 'score': -1 * (state.num_empty_squares() + 1)}
    elif not state.empty_squares():
        return {'position': None, 'score': 0}

    if is_maximizing:
        best = {'position': None, 'score': -math.inf}
        for possible_move in state.available_moves():
            # Make a move
            state.make_move(possible_move, ai_letter)
            
            # Simulate a game after making that move
            sim_score = minimax(state, depth + 1, alpha, beta, False, ai_letter, human_letter)
            
            # Undo move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            # Update best score and alpha
            if sim_score['score'] > best['score']:
                best = sim_score
                
            alpha = max(alpha, best['score'])
            if beta <= alpha:
                break # Alpha-beta pruning
        return best
    else:
        best = {'position': None, 'score': math.inf}
        for possible_move in state.available_moves():
            # Make a move
            state.make_move(possible_move, human_letter)
            
            # Simulate a game after making that move
            sim_score = minimax(state, depth + 1, alpha, beta, True, ai_letter, human_letter)
            
            # Undo move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            # Update best score and beta
            if sim_score['score'] < best['score']:
                best = sim_score
                
            beta = min(beta, best['score'])
            if beta <= alpha:
                break # Alpha-beta pruning
        return best


def play_game():
    game = TicTacToe()
    
    print("=======================================")
    print("       Unbeatable Tic-Tac-Toe AI       ")
    print("=======================================\n")
    game.print_board_nums()
    
    human_letter = 'X'
    ai_letter = 'O'
    turn = 'X'
    
    while game.empty_squares():
        if turn == human_letter:
            valid_square = False
            val = None
            while not valid_square:
                square = input(f"Your turn ({human_letter}). Input move (0-8): ")
                try:
                    val = int(square)
                    if val not in game.available_moves():
                        raise ValueError
                    valid_square = True
                except ValueError:
                    print("Invalid move. Try again.")
            
            game.make_move(val, human_letter)
            print(f"\nYou moved to square {val}")
            
        else:
            print(f"\nAI ({ai_letter}) is thinking...")
            time.sleep(0.5) # Slight delay to feel like the AI is thinking
            
            if len(game.available_moves()) == 9:
                square = 4 # Optimize first move (center is generally best)
            else:
                # Use Minimax with Alpha-Beta Pruning
                result = minimax(game, 0, -math.inf, math.inf, True, ai_letter, human_letter)
                square = result['position']
                
            game.make_move(square, ai_letter)
            print(f"AI moved to square {square}")
            
        game.print_board()
        print("")
        
        if game.current_winner:
            if game.current_winner == human_letter:
                print("You win! (Wait, that's impossible...)")
            else:
                print("AI wins! Better luck next time.")
            return

        # Alternate turns
        turn = ai_letter if turn == human_letter else human_letter

    print("It's a tie!")

if __name__ == '__main__':
    play_game()
