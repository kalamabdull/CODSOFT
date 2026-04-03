# Tic-Tac-Toe AI with Minimax and Alpha-Beta Pruning

This project implements an unbeatable Tic-Tac-Toe agent in Python using the **Minimax algorithm with Alpha-Beta Pruning**.

## How to Play

Run the script from your terminal:

```bash
cd "c:\Users\User\Desktop\TIC-TAC-TOE AI"
python tictactoe.py
```

The board is represented by numbers 0-8:
```
| 0 | 1 | 2 |
| 3 | 4 | 5 |
| 6 | 7 | 8 |
```
When it's your turn, simply input the number of the square where you'd like to place your 'X'.

---

## Understanding the AI implementation

### 1. The Minimax Algorithm
Minimax is a classic decision-making algorithm commonly used in game theory. It explores all possible future moves assuming that both players are playing perfectly:
- The **Maximizer** (the AI) tries to maximize the score.
- The **Minimizer** (the human) tries to minimize the score.

In our representation:
- State where AI wins: Positive score (e.g., +1 multiplied by remaining spaces to win faster)
- State where Human wins: Negative score (e.g., -1 multiplied by remaining spaces)
- Tie: 0

The algorithm simulates all paths recursively, down to the end of the game, and bubbles the final score all the way up to choose the optimal move.

### 2. Alpha-Beta Pruning
If we only use Minimax, the algorithm explores *every* possible terminal state. Although the total number of possibilities in Tic-Tac-Toe is relatively small (total 9! permutations, around 362,880), the approach can be perfectly optimized using Alpha-Beta Pruning. 

Alpha-Beta Pruning stops exploring paths completely when it determines that a certain branch will never be selected:
- **Alpha**: The best alternative for the maximizer (AI) on the current path.
- **Beta**: The best alternative for the minimizer (Human) on the current path.

If `beta <= alpha` at any point, the algorithm safely abandons the current branch, because it knows that the path would never be reached during perfectly optimal play. This drastically reduces the time complexity without altering the final optimal decision!
