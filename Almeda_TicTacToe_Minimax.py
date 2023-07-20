import time

import pygame
import numpy as np
import sys
import re


# Initialize Pygame
pygame.init()
pygame.font.init()

clock = pygame.time.Clock()

# Define the dimensions of the grid
grid_size = 3
cell_size = 300
grid_width = grid_size * cell_size
grid_height = grid_size * cell_size

# Define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Create the Pygame window
screen = pygame.display.set_mode((grid_width, grid_height))
pygame.display.set_caption("Clickable Grid")
pygame.mouse.set_visible(True)

# Create a 2D array to represent the grid
tictactoe_str = 'xxxxxxxxx'
grid = list(zip(*[iter(tictactoe_str)]*3))
grid = [list(tup) for tup in grid]
states = []

def replacenth(string, sub, wanted, n):
    where = [m.start() for m in re.finditer(sub, string)][n-1]
    before = string[:where]
    after = string[where:]
    after = after.replace(sub, wanted, 1)
    newString = before + after
    return newString

def draw_grid():
    screen.fill(WHITE)

    for row in range(grid_size):
        for col in range(grid_size):
            rect = pygame.Rect(
                col * cell_size, row * cell_size, cell_size, cell_size
            )
            pygame.draw.rect(screen, BLACK, rect, 1)

            if grid[row][col] == 'X':
                x = (col * cell_size + cell_size // 2) - 50
                y = (row * cell_size + cell_size // 2) - 100
                draw_X(x, y)

            if grid[row][col] == 'O':
                x = (col * cell_size + cell_size // 2) - 50
                y = (row * cell_size + cell_size // 2) - 100
                draw_O(x, y)




    pygame.display.flip()

def Value(state, depth):
    # X = Player
    # O = Opponent(AI)
    win_pattern = r"^\s*(?:...){0,2}(XXX|OOO)|^\s*(O|X)..\2..\2..|^\s*.(O|X)..\3..\3.|^\s*..(O|X)..\4..\4|^\s*(O|X)...\5...\5|^\s*..(O|X).\6.\6.."
    x_win_pattern = r"^\s*(?:...){0,2}(XXX)|^\s*(X)..\2..\2..|^\s*.(X)..\3..\3.|^\s*..(X)..\4..\4|^\s*(X)...\5...\5|^\s*..(X).\6.\6.."
    o_win_pattern = r"^\s*(?:...){0,2}(OOO)|^\s*(O)..\2..\2..|^\s*.(O)..\3..\3.|^\s*..(O)..\4..\4|^\s*(O)...\5...\5|^\s*..(O).\6.\6.."


    if re.search(x_win_pattern, state):
        return 10 + depth
    if re.search(o_win_pattern, state):
        return depth - 10

    if not re.search(win_pattern, state) and 'x' not in state:
        return 0

def check_win(state):
    win_pattern = r"^\s*(?:...){0,2}(XXX|OOO)|^\s*(O|X)..\2..\2..|^\s*.(O|X)..\3..\3.|^\s*..(O|X)..\4..\4|^\s*(O|X)...\5...\5|^\s*..(O|X).\6.\6.."
    x_win_pattern = r"^\s*(?:...){0,2}(XXX)|^\s*(X)..\2..\2..|^\s*.(X)..\3..\3.|^\s*..(X)..\4..\4|^\s*(X)...\5...\5|^\s*..(X).\6.\6.."
    o_win_pattern = r"^\s*(?:...){0,2}(OOO)|^\s*(O)..\2..\2..|^\s*.(O)..\3..\3.|^\s*..(O)..\4..\4|^\s*(O)...\5...\5|^\s*..(O).\6.\6.."


    if re.search(x_win_pattern, state):
        return 'WON'
    if re.search(o_win_pattern, state):
        return 'LOST'
    if not re.search(win_pattern, state) and 'x' not in state:
        return 'DRAW'



def actions(state, player):
    possible_states = []
    populate = None
    if player == 'MAX':
        populate = 'X'
    if player == 'MIN':
        populate = 'O'

    count = 0
    for l in state:
        if l == 'x':
            count += 1
            newstr = replacenth(state, 'x', populate, count)
            possible_states.append(newstr)

    return possible_states


def minimax(state, player, depth):
    #print(state)
    terminal = Value(state, depth)

    if terminal:
        return terminal

    if player == 'MAX':
        value = -np.inf
        for a in actions(state, player):
            value = max(value, minimax(a, 'MIN', depth + 1))
        return value

    if player == 'MIN':
        value = np.inf
        for a in actions(state, player):
            value = min(value, minimax(a, 'MAX', depth + 1))

        return value



def player_click(row, col):
    # player = 'MAX'
    over = False
    grid[row][col] = 'X'
    state = ''.join(item for innerlist in grid for item in innerlist)
    print(state)
    inds = opponent_click(state)
    if inds:
        row, col = inds
    else:
        over = True
    grid[row][col] = 'O'
    state = ''.join(item for innerlist in grid for item in innerlist)

    verdict = check_win(state)
    return verdict




    #state = ''.join(item for innerlist in grid for item in innerlist)


def get_diff_ind(s1, s2):
    try:
        n = [i for i in range(len(s1)) if s1[i] != s2[i]]
        return n[0] // 3, n[0] % 3
    except:
        return None

def opponent_click(state):
    moves = actions(state, 'MAX')
    best_score = 1000
    best_move = None
    for move in moves:
        #print(move)
        score = minimax(move, 'MIN', 0)
        print(move, score)
        if score < best_score:

            best_score = score
            best_move = move


    try:
        inds = get_diff_ind(best_move, state)
        return inds
    except:
        return None


def get_clicked_cell(mouse_pos):
    x, y = mouse_pos
    row = y // cell_size
    col = x // cell_size
    return row, col


def display_text(verdict):
    if verdict == 'LOST':
        my_font = pygame.font.SysFont('Comic Sans MS', 150)
        text_surface = my_font.render('LOST', False, (2, 54, 13))
        screen.blit(text_surface, (screen.get_width()//2, screen.get_height()//2))


    if verdict == 'DRAW':
        my_font = pygame.font.SysFont('Comic Sans MS', 150)
        text_surface = my_font.render('DRAW', False, (50, 2, 13))
        screen.blit(text_surface, (screen.get_width()//2, screen.get_height()//2))

    if verdict == 'WON':
        my_font = pygame.font.SysFont('Comic Sans MS', 150)
        text_surface = my_font.render('WON', False, (142, 70, 120))
        screen.blit(text_surface, (screen.get_width()//2, screen.get_height()//2))


def draw_X(x, y):
    my_font = pygame.font.SysFont('Comic Sans MS', 150)
    text_surface = my_font.render('X', False, (0, 0, 0))
    screen.blit(text_surface, (x,y))

def draw_O(x, y):
    my_font = pygame.font.SysFont('Comic Sans MS', 150)
    text_surface = my_font.render('O', False, (0, 0, 0))
    screen.blit(text_surface, (x,y))





# X

running = True
verdict = None
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                row, col = get_clicked_cell(mouse_pos)
                verdict = player_click(row, col)




    draw_grid()

    pygame.display.flip()

    if verdict:
        display_text(verdict)

        pygame.display.flip()

        time.sleep(2)
        running = False



    # clock.tick(60)

pygame.quit()
