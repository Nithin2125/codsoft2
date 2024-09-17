import pygame
import numpy as np
import random
import sys

# Constants
WINDOW_SIZE = 300
GRID_SIZE = 3
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
LINE_WIDTH = 5
BOARD_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
X_COLOR = (0, 0, 255)
O_COLOR = (255, 0, 0)

# Initialize pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Tic Tac Toe')
font = pygame.font.Font(None, 74)

# Initialize board
board = np.full((GRID_SIZE, GRID_SIZE), '', dtype=str)

def draw_board():
    window.fill(BOARD_COLOR)
    
    # Draw the grid
    for i in range(1, GRID_SIZE):
        pygame.draw.line(window, LINE_COLOR, (0, i * CELL_SIZE), (WINDOW_SIZE, i * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(window, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_SIZE), LINE_WIDTH)

    # Draw X and O
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i, j] == 'X':
                draw_x(i, j)
            elif board[i, j] == 'O':
                draw_o(i, j)
    
    pygame.display.update()

def draw_x(row, col):
    pygame.draw.line(window, X_COLOR, (col * CELL_SIZE + 15, row * CELL_SIZE + 15),
                     ((col + 1) * CELL_SIZE - 15, (row + 1) * CELL_SIZE - 15), LINE_WIDTH)
    pygame.draw.line(window, X_COLOR, ((col + 1) * CELL_SIZE - 15, row * CELL_SIZE + 15),
                     (col * CELL_SIZE + 15, (row + 1) * CELL_SIZE - 15), LINE_WIDTH)

def draw_o(row, col):
    pygame.draw.circle(window, O_COLOR, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                       CELL_SIZE // 2 - 15, LINE_WIDTH)

def check_winner():
    # Check rows and columns
    for i in range(GRID_SIZE):
        if np.all(board[i, :] == 'X') or np.all(board[:, i] == 'X'):
            return 'X'
        if np.all(board[i, :] == 'O') or np.all(board[:, i] == 'O'):
            return 'O'
    
    # Check diagonals
    if np.all(np.diag(board) == 'X') or np.all(np.diag(np.fliplr(board)) == 'X'):
        return 'X'
    if np.all(np.diag(board) == 'O') or np.all(np.diag(np.fliplr(board)) == 'O'):
        return 'O'
    
    return None

def is_board_full():
    return not np.any(board == '')

def ai_move():
    # AI tries to win or block
    for player in ['O', 'X']:
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if board[i, j] == '':
                    board[i, j] = player
                    if check_winner() == player:
                        if player == 'O':
                            board[i, j] = ''
                            return (i, j)
                        board[i, j] = ''
                    else:
                        board[i, j] = ''
    
    # Random move if no immediate win or block
    empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if board[i, j] == '']
    if empty_cells:
        return random.choice(empty_cells)
    return None

def main():
    current_player = 'X'  # Player starts first
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = pygame.mouse.get_pos()
                row, col = y // CELL_SIZE, x // CELL_SIZE

                if board[row, col] == '':
                    board[row, col] = current_player
                    if check_winner():
                        print(f"{current_player} wins!")
                        game_over = True
                    elif is_board_full():
                        print("It's a draw!")
                        game_over = True
                    else:
                        current_player = 'O'
                        move = ai_move()
                        if move:
                            row, col = move
                            board[row, col] = 'O'
                            if check_winner():
                                print("AI wins!")
                                game_over = True
                            elif is_board_full():
                                print("It's a draw!")
                                game_over = True
                            else:
                                current_player = 'X'

        draw_board()

if __name__ == "__main__":
    main()