import pygame,copy,random
from pygame.locals import *

black = (0,0,0)
bgcolor = (150,200,150)
white = (0,0,0)
clock = pygame.time.Clock()
fps = 30

best_col = -1

board_height = 6 # number of rows
board_width = 7 # number of columns
screen_height = 480
screen_width = 650  # optimise later according to  better gui

element_size = 50 # size in pixels of each element of board

redtoken_img = pygame.image.load('4row_red.png')
redtoken_img = pygame.transform.scale(redtoken_img,(element_size,element_size))

blacktoken_img = pygame.image.load('4row_black.png')
blacktoken_img = pygame.transform.scale(blacktoken_img,(element_size,element_size))

computer_win_img = pygame.image.load('computer.png')
computer_win_img = pygame.transform.scale(computer_win_img,(element_size,element_size))
gameover_rect = computer_win_img.get_rect()
gameover_rect.center = (screen_width / 2, screen_height / 2)

player_win_img = pygame.image.load('image 1.png')
player_win_img = pygame.transform.scale(player_win_img,(element_size,element_size))

element_img = pygame.image.load('4row_board.png')
element_img = pygame.transform.scale(element_img,(element_size,element_size))

tie_img = pygame.image.load('4row_tie.png')
tie_img = pygame.transform.scale(tie_img,(element_size,element_size))

help_img = pygame.image.load('4row_arrow.png')
help_img = pygame.transform.scale(help_img,(element_size,element_size))


redtoken_rect = pygame.Rect(element_size /2, screen_height - (3 * element_size)/2, element_size, element_size)
blacktoken_rect = pygame.Rect(screen_width - 3 * element_size/2, screen_height - (3 * element_size)/2, element_size, element_size)

help_rect = help_img.get_rect()
help_rect.left = redtoken_rect.right + 10
help_rect.centery = redtoken_rect.centery

display_surf = pygame.display.set_mode((screen_width, screen_height))
x_margin = (screen_width - element_size * board_width)//2
y_margin = (screen_height - element_size * board_height)//2

human = 0
computer = 1
level = 4
initial_score = -100000
global max_score
max_score = initial_score
def main():

    #show_help = True
    while True:
        game_loop()
        
def game_loop():
    show_help = True
    board = get_newboard()
    
    #v draw_board(board)

    if random.randint(0,1) == 0:
        turn = human
    else:
        turn = computer

    while True:
        if turn == human:
            make_humanmove(board, show_help)
            turn = computer
            if is_winner(board, human):
                gameover_img = player_win_img
                break
        elif turn == computer:
            make_computermove(board,show_help)# change explore
            turn = human
            if is_winner(board, computer):
                gameover_img = computer_win_img
                break
        if isboard_full(board) == True:
            gameover_img = tie_img
            break
        show_help = False
        
    while True:
        draw_board(board)
        display_surf.blit(gameover_img,gameover_rect)
        pygame.display.update()
        clock.tick()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            elif event.type == MOUSEBUTTONUP:
                return
        pygame.display.update()
        
def get_newboard():
    board = []
    for i in range(board_width):
        board.append([None] * board_height)
    return board

def make_humanmove(board,show_help):
    not_dragging = True
    pos_x = None
    pos_y = None
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
                
            elif event.type == MOUSEBUTTONDOWN and not_dragging and redtoken_rect.collidepoint(event.pos):
                not_dragging = False
                pos_x, pos_y = event.pos
                
            elif event.type == MOUSEMOTION and  not not_dragging:
                pos_x, pos_y = event.pos
                if pos_x > x_margin and pos_x < screen_width - x_margin and pos_y < screen_height - y_margin:
                    col = (pos_x - x_margin)//element_size 
                    draw_board(board, None, {'x' : x_margin + col * element_size, 'y' : screen_height - y_margin + element_size/2, 'turn' : human})
                    pygame.display.update()
                    ####CHECK
                    #clock.tick()
                    
            elif event.type == MOUSEBUTTONUP and not not_dragging:
                if pos_x > x_margin and pos_x < screen_width - x_margin and pos_y < screen_height - y_margin:
                    col = ((pos_x - x_margin)//element_size)
                    if isvalid_move(board,col):
                        animate_dropping_effect(board, col, human)
                        board[col][lowest_empty_space(board, col)] = human
                        draw_board(board)
                        pygame.display.update()
                        return
                    
                pos_x = None
                pos_y = None
                not_dragging = True
                
        if pos_x != None and pos_y != None:
            draw_board(board , {'x':pos_x - (element_size//2),'y':pos_y - (element_size//2),'turn':human})
        else:
            draw_board(board)
            
        if show_help == True:
            display_surf.blit(help_img, help_rect)
        pygame.display.update()
        clock.tick()

def is_winner(board, player):
    for x in range(board_width):
        for y in range(board_height - 3):
            if board[x][y] ==  board[x][y+1] ==  board[x][y+2] == board[x][y+3] == player:
                return True
    for x in range(board_width - 3):
        for y in range(board_height):
            if board[x][y] == board[x+1][y] == board[x+2][y] == board[x+3][y] == player:
                return True

    for x in range(board_width - 3):
        for y in range(board_height - 3):
            if board[x][y] == board[x+1][y+1] == board[x+2][y+2] == board[x+3][y+3] == player:
                return True

    for x in range(board_width - 3):
        for y in range(3, board_height -3):
            if board[x][y] == board[x+1][y-1] == board[x+2][y-2] == board[x+3][y-3] == player:
                return True
    return False

def isboard_full(board):
    for x in range(board_width):
        for y in range(board_height):
            if board[x][y] == None:
                return False
    return True
    
def draw_board(board, extra_token = None, indicator_token  = None):
    token_rect = pygame.Rect(0, 0, element_size, element_size)
    display_surf.fill(bgcolor)
    
    for x in range(board_width):
        for y in range(board_height):
            token_rect.topleft == (x_margin + x * element_size, y_margin + y * element_size)
            if(board[x][y] == human):
                display_surf.blit(redtoken_img, token_rect)
            elif(board[x][y] == computer):
                display_surf.blit(blacktoken_img, token_rect)
                
    if indicator_token != None:
        display_surf.blit(redtoken_img , (indicator_token['x'], indicator_token['y'], element_size, element_size))

    if extra_token != None:
        if extra_token['turn'] == human:
            display_surf.blit(redtoken_img, (extra_token['x'], extra_token['y'], element_size, element_size))
        elif extra_token['turn'] == computer:
            display_surf.blit(blacktoken_img, (extra_token['x'], extra_token['y'], element_size, element_size))
    
    for x in range(board_width):
        for y in range(board_height):
            token_rect.topleft = (x_margin + x * element_size, y_margin + y * element_size)
            display_surf.blit(element_img, token_rect)

    display_surf.blit(redtoken_img, redtoken_rect)
    display_surf.blit(blacktoken_img, blacktoken_rect)

def lowest_empty_space(board, col):
    if col < 0 or col >= board_width:
        return -1
    for y in range (board_height - 1, -1, -1):
        if board[col][y] == None:
            return y
    return -1

def isvalid_move(board, col):
    if col >= 0 and col < board_width and board[col][0]== None:
        return True
    return False
        
def animate_dropping_effect(board, col ,player):
    speed = 2.0
    lowest_empty_pos = lowest_empty_space(board, col)
    pos_x = x_margin + col * element_size
    pos_y = y_margin - element_size
    
    while True:
        pos_y = pos_y + speed
        if (pos_y - y_margin)//element_size >= lowest_empty_space(board, col):
            return
        draw_board(board,None,{'x' : pos_x,'y' : pos_y,'type' : player})
        pygame.display.update()
        clock.tick()

def number_of_threes(board, player):
    count = 0
    for x in range(board_width):
        for y in range(board_height-2):
            if board[x][y] == board[x][y+1] == board[x][y+2] == player:
                count = count + 1

    for x in range(board_width - 2):
        for y in range(board_height):
            if board[x][y] == board[x+1][y] == board[x+2][y] == player:
                count = count + 1

    for x in range(board_width - 2):
        for y in range(board_height - 2):
            if board[x][y] == board[x+1][y+1] == board[x+2][y+2] == player:
                count = count + 1

    for x in range(2, board_width):
        for y in range(board_height - 2):
            if board[x][y] == board[x-1][y+1] == board[x-2][y+2] == player:
                count = count + 1

    return count

def number_of_twos(board, player):
    count = 0
    for x in range(board_width):
        for y in range(board_height - 1):
            if board[x][y] == board[x][y+1] == player:
                count = count + 1

    for x in range(board_width - 1):
        for y in range(board_height):
            if board[x][y] == board[x+1][y] == player:
                count = count + 1

    for x in range(board_width - 1):
        for y in range(board_height - 1):
            if board[x][y] == board[x+1][y+1] == player:
                count = count + 1

    for x in range(1, board_width):
        for y in range(board_height - 1):
            if board[x][y] == board[x-1][y+1] == player:
                count = count + 1
                
    return count

def get_bestmove(board, player, depth, alpha, beta):
    
    if player == human:
        opponent = computer
    elif player == computer:
        opponent = human
        
    if is_winner(board, opponent):
        if opponent == computer:
            return pow(10, depth+3)#change
        else:
            return -pow(10, depth+3)#change
        
    elif depth == 0:
        threes = number_of_threes(board, player)
        twos = number_of_twos(board, player)
        opponent_threes = number_of_threes(board, opponent)
        opponent_twos = number_of_twos(board, opponent)
        heuristic_value  = 100 * threes + 10 * twos - 100 * opponent_threes - 10 * opponent_twos
        return heuristic_value
        ##
        ##
        ##evaluate board here
        ##
        ##

    column = -1
    if player == computer:
        max_eval = -100000
        for moves in range(board_width):
            lowest_space = lowest_empty_space(board, moves)
            if lowest_space == -1:
                continue
            board[moves][lowest_space] = player
            if is_winner(board, player):
                return pow(10, depth+3)
            evaluate = get_bestmove(board, opponent, depth - 1, alpha, beta)
            if evaluate > max_eval:
                best_col = moves
                max_eval = evaluate
            alpha = max(alpha, evaluate)
            if beta <= alpha:
                break
            board[moves][lowest_space] = None
        return max_eval
    
    elif player == human:
        min_eval = 100000
        for moves in range(board_width):
            lowest_space = lowest_empty_space(board, moves)
            if lowest_space == -1:
                continue
            board[moves][lowest_space] = player
            evaluate = get_bestmove(board, opponent, depth - 1, alpha, beta)
            if evaluate < min_eval:
                best_col = moves
                min_eval = evaluate
            beta = min(beta, evaluate)
            if beta <= alpha:
                break
            board[moves][lowest_space] = None
        return min_eval

def make_computermove(board, show_help):

    best_move = get_bestmove(board, computer, level, -100000, 100000)
    animate_dropping_effect(board, best_col, computer)
    board[best_col][lowest_empty_space(board, best_col)] = computer
    draw_board(board)
    
    if show_help == True:
        display_surf.blit(help_img, help_rect)
    pygame.display.update()
    clock.tick()
        
if __name__ == '__main__':
    main()
