import pygame

import numpy as np
from pygame.locals import *

pygame.init()

def move_left():
    # slide tiles
    for index, row in enumerate(board):
        cur_ele = row[row!=-1]
        n_ele = cur_ele.size
        board[index][:n_ele] = cur_ele[:]
        board[index][n_ele:] = -1
        for j, ele in enumerate(row):
            if ele == row[ele+1]
    # merge twins
    
    return board

def handle_event(event):
    if event.type == KEYDOWN and event.key in (K_UP, K_DOWN, K_LEFT, K_RIGHT):        
        if event.key == K_UP:
            print("You pressed up arrow")
        elif event.key == K_DOWN:
             print("You pressed down arrow")
        elif event.key == K_LEFT:
            move_left()
        elif event.key == K_RIGHT:
            print("You pressed right arrow")
        else:
            print("Press one of the arrow keys!")
        add_new_number(board)
        draw_board(display_surf, board)
    
display_surf = pygame.display.set_mode((400, 400))

TILE_COLOR     = (175,238,238)
BLACK = (0, 0, 0)
GREEN        = (  0, 155,   0)
BLUE         = (  0,   0, 155)

BASICFONT = pygame.font.Font(pygame.font.match_font('calibri'), 16)
BASICFONT.set_bold(True)

def makeTile(text, left, top, color=BLACK, bkg_color=TILE_COLOR):
    pygame.draw.rect(display_surf, TILE_COLOR, (left+1, top+1, 47, 47))
    tile_label = str(text) if text != -1 else ''
    text_surf = BASICFONT.render(tile_label, True, color, bkg_color)
    text_rect = text_surf.get_rect()
    text_rect.centerx = left + 25
    text_rect.centery = top + 25
    display_surf.blit(text_surf, text_rect)

def make_game_window():
    pygame.display.set_caption('2048')
    textSurf = BASICFONT.render('Can you reach 2048?', True, GREEN, BLACK)
    textRec = textSurf.get_rect()
    textRec.centerx = 200
    textRec.centery = 50
    # textRec.topleft = (10, 10)
    display_surf.blit(textSurf, textRec)


def draw_board(display_surf, board):
    pygame.draw.rect(display_surf, BLACK, (70, 70, 150, 150))

    rect_0 = makeTile(board[0][0], 75, 75)
    rect_1 = makeTile(board[0][1], 125, 75)
    rect_2 = makeTile(board[0][2], 175, 75)
    makeTile(board[0][3], 225, 75)
    rect_3 = makeTile(board[1][0], 75, 125)
    rect_4 = makeTile(board[1][1], 125, 125)
    rect_5 = makeTile(board[1][2], 175, 125)
    makeTile(board[1][3], 225, 125)
    rect_6 = makeTile(board[2][0], 75, 175)
    rect_7 = makeTile(board[2][1], 125, 175)
    rect_8 = makeTile(board[2][2], 175, 175)
    makeTile(board[2][3], 225, 175)
    makeTile(board[3][0], 75, 225)
    makeTile(board[3][1], 125, 225)
    makeTile(board[3][2], 175, 225)
    makeTile(board[3][3], 225, 225)
    
def add_new_number(board):
    prob = np.random.random_sample()
    new_val = -1
    if prob < 0.4:
        new_val = 4
    else:
        new_val = 2
    while(True):
        row = np.random.randint(0, 4)
        col = np.random.randint(0, 4)
        if board[row][col] == -1:
            board[row][col] = new_val
            break
    return board


make_game_window()

board = np.asarray([[-1 for _ in np.arange(4)] for _ in np.arange(4)])
# print board
add_new_number(board)
# print board
add_new_number(board)
# print board

draw_board(display_surf, board)


running = True
while running:
    for event in pygame.event.get():
        handle_event(event)
        if event.type == QUIT:
            running = False
    pygame.display.update()
            
if not running:
    pygame.quit()
    
 