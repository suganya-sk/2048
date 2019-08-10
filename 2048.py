import pygame

import numpy as np
from pygame.locals import *

TILE_COLOR   = (175,238,238)
BLACK        = (0, 0, 0)
GREEN        = (  0, 155,   0)
BLUE         = (  0,   0, 155)
RED          = (255, 0, 0)



def _shift_and_merge(arr):
    result = np.copy(arr)
    
    # shift
    all_ele = arr[arr!=-1]
    count = all_ele.size
    if count != arr.size:
        result[:count] = all_ele[:]
        result[count:] = -1

    # merge neighbouring twins
    for index, ele in enumerate(result[:-1]):
        if ele == result[index + 1] and ele != -1:
            result[index] = ele * 2            
            result[index + 1] = -1
            result[(index + 1):] = _shift_and_merge(result[(index + 1):])

    return result



class Game():
    pygame.init()
    FONT = pygame.font.Font(pygame.font.match_font('calibri'), 16)
    FONT.set_bold(True)
   

    def _make_game_window(self):
        pygame.display.set_caption('2048')
        text_surf = Game.FONT.render('Can you reach 2048?', True, GREEN, BLACK)
        text_rect = text_surf.get_rect()
        text_rect.centerx = 200
        text_rect.centery = 50
        # text_rect.topleft = (10, 10)
        self.display_surf.blit(text_surf, text_rect)


    def _add_new_numer_to_board(self):
        prob = np.random.random_sample()
        new_val = -1
        if prob < 0.4:
            new_val = 4
        else:
            new_val = 2
        while(True):
            row = np.random.randint(0, 4)
            col = np.random.randint(0, 4)
            if self.board[row][col] == -1:
                self.board[row][col] = new_val
                break


    def _make_tile(self, text, left, top, color=BLACK, bkg_color=TILE_COLOR):
        pygame.draw.rect(self.display_surf, TILE_COLOR, (left + 1, top + 1, 47, 47))
        tile_label = str(text) if text != -1 else ''
        text_surf = Game.FONT.render(tile_label, True, color, bkg_color)
        text_rect = text_surf.get_rect()
        text_rect.centerx = left + 25
        text_rect.centery = top + 25
        self.display_surf.blit(text_surf, text_rect)


    def _draw_board(self):
        # draw background so cells have black border
        pygame.draw.rect(self.display_surf, BLACK, (70, 70, 150, 150))
    
        self._make_tile(self.board[0][0], 75, 75)
        self._make_tile(self.board[0][1], 125, 75)
        self._make_tile(self.board[0][2], 175, 75)
        self._make_tile(self.board[0][3], 225, 75)
        self._make_tile(self.board[1][0], 75, 125)
        self._make_tile(self.board[1][1], 125, 125)
        self._make_tile(self.board[1][2], 175, 125)
        self._make_tile(self.board[1][3], 225, 125)
        self._make_tile(self.board[2][0], 75, 175)
        self._make_tile(self.board[2][1], 125, 175)
        self._make_tile(self.board[2][2], 175, 175)
        self._make_tile(self.board[2][3], 225, 175)
        self._make_tile(self.board[3][0], 75, 225)
        self._make_tile(self.board[3][1], 125, 225)
        self._make_tile(self.board[3][2], 175, 225)
        self._make_tile(self.board[3][3], 225, 225)


    def _move_left(self):
        for row_index, row in enumerate(self.board):
            self.board[row_index] = _shift_and_merge(row)


    def _move_right(self):
        # since _shift_and_merge always shifts elements to the front of the array (left), to 
        # to shift right, flip the array, invoke _shift_and_merge and flip result again
        for row_index, row in enumerate(self.board):
            flipped_arr = row[::-1]
            result = _shift_and_merge(flipped_arr)
            self.board[row_index] = result[::-1]

    def _move_up(self):
        # use transpose to iterate through columns
        temp_board = self.board.T
        # print("Flipped board")
        # print(temp_board)
        for row_index, row in enumerate(temp_board):
            temp_board[row_index] = _shift_and_merge(row)
        self.board = temp_board.T

    def _move_down(self):
        # use transpose to iterate through columns
        temp_board = self.board.T
        # print("Flipped board")
        # print(temp_board)
        for row_index, row in enumerate(temp_board):
            flipped_arr = row[::-1]
            result = _shift_and_merge(flipped_arr)
            temp_board[row_index] = result[::-1]
        self.board = temp_board.T


    # def is_board_full(self):
    #     if -1 not in self.board:
    #         if:
    #             return False
    #         else:
    #             return True
    #     return False


    def _handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key in (K_UP, K_DOWN, K_LEFT, K_RIGHT):
                self.move_count += 1       
                if event.key == K_UP:
                    self._move_up()
                elif event.key == K_DOWN:
                    self._move_down()
                elif event.key == K_LEFT:
                    self._move_left()
                elif event.key == K_RIGHT:
                    self._move_right()
                self._add_new_numer_to_board()
                self._draw_board()
            else:
                print("Press one of the arrow keys!")

            if 2048 in self.board:
                msg_surf = Game.FONT.render('Congrats! You reached 2048 in %s moves! :)' %self.move_count , True, GREEN, BLACK)
                self.game_over = True
            elif -1 not in self.board:
                msg_surf = Game.FONT.render('Game over! Better luck next time!' , True, RED, BLACK)
                self.game_over = True
            if self.game_over:
                msg_rect = msg_surf.get_rect()
                msg_rect.centerx = 200
                msg_rect.centery = 320
                self.display_surf.blit(msg_surf, msg_rect)
            

   
    def __init__(self):
        self.display_surf = pygame.display.set_mode((400, 400))
        self._make_game_window()

        # initialize board
        self.board = np.asarray([[-1 for _ in np.arange(4)] for _ in np.arange(4)])
        self._add_new_numer_to_board()
        self._add_new_numer_to_board()

        self._draw_board()
        self.game_over = False
        self.move_count = 0

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif not self.game_over:
                    self._handle_event(event)
                    pygame.display.update()
                    
        if not running:
            pygame.quit()
            
            
            
if __name__ == "__main__":
    Game()