import random, copy, pygame
from pygame.locals import *

human = 1
computer = 2

level = 2 # this represents half of the depth, i.e depth of minimax will be 4 right now 

element_size = 50 # red and black token size

clock_speed = 30 # fps speed for screen updation
screen_width = 640 # width of game screen
screen_height = 480 # height of game screen

board_width = 7  # number of columns
board_height = 6 # number of rows

x_margin = (screen_width - board_width * element_size) // 2 # margin left on left and right side of board
y_margin = (screen_height - board_height * element_size) // 2 # margin left on top and bottom of board

white = (255, 255, 255)

bgcolor = (150,200,150)


pygame.init()


redtoken_rect = pygame.Rect((element_size // 2), screen_height - (3 * element_size // 2), element_size, element_size) # rectangle object to hold token image on bottom right
blacktoken_rect = pygame.Rect(screen_width - int(3 * element_size / 2), screen_height - int(3 * element_size / 2), element_size, element_size)
redtoken_img = pygame.image.load('4row_red.png')
redtoken_img = pygame.transform.scale(redtoken_img, (element_size , element_size ))
blacktoken_img = pygame.image.load('4row_black.png')
blacktoken_img = pygame.transform.scale(blacktoken_img, (element_size, element_size))
element_img = pygame.image.load('4row_board.png')
element_img = pygame.transform.scale(element_img, (element_size, element_size))

clock = pygame.time.Clock()
game_display = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('COnnect 4')

human_winner_img = pygame.image.load('4row_humanwinner.png')
computer_winner_img = pygame.image.load('4row_computerwinner.png')
tie_img = pygame.image.load('4row_tie.png')
winner_rect = human_winner_img.get_rect()
winner_rect.center = (screen_width // 2, screen_height // 2)

help_img = pygame.image.load('4row_arrow.png')
help_rect = help_img.get_rect()
help_rect.left = redtoken_rect.right + 10
help_rect.centery = redtoken_rect.centery

def main():
    while True:
        game_play()# keep playing till user exits


def game_play():
                
        
    if random.randint(0, 1) == 0:# randomly choose who plays
        turn = computer
    else:
        turn = human
    
    help_show = True
    
    board = new_board()

    while True: # game loop
        if turn == human:
            human_move(board, help_show)
            if help_show:
                help_show = False
            if is_win(board, human):
                win_img = human_winner_img
                break
            turn = computer # switch to other player's turn
        else:
            # Computer player's turn.
            col = make_computer_move(board)
            computer_animate_effect(board, col)
            check_move(board, computer, col)
            if is_win(board, computer):
                win_img = computer_winner_img
                break
            turn = human # switch to other player's turn

        if is_full(board):
            # A completely filled board means it's a tie.
            win_img = tie_img
            break

    while True:
        # Keep looping until player clicks the mouse or quits.
        draw_board(board)
        game_display.blit(win_img, winner_rect)
        pygame.display.update()
        clock.tick()
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONUP:
                return
    help_show = False


def check_move(board, player, col):
    lowest = lowest_space(board, col)
    if lowest != -1:
        board[col][lowest] = player


def is_full(board):
    # Returns True if there are no empty spaces anywhere on the board.
    for x in range(board_width):
        if board[x][0] == None:
            return False
    return True

def is_valid(board, col):
    # Returns True if there is an empty space in the given col.
    # Otherwise returns False.
    if col < 0 or col >= (board_width) or board[col][0] != None:
        return False
    return True

def new_board():
    board = []
    for x in range(board_width):
        board.append([None] * board_height)
    return board

def lowest_space(board, col):
    # Return the row number of the lowest empty row in the given col.
    for y in range(board_height-1, -1, -1):
        if board[col][y] == None:
            return y
    return -1


def make_computer_move(board):
    possible_moves = minimax(board, computer, level)
    # get the best fitness from the potential moves
    best_move = -1
    for i in range(board_width):
        if possible_moves[i] > best_move and is_valid(board, i):
            best_move = possible_moves[i]
    # find all potential moves that have this best fitness
    best_moves = []
    for i in range(len(possible_moves)):
        if possible_moves[i] == best_move and is_valid(board, i):
            best_moves.append(i)
    return random.choice(best_moves)

def human_move(board, first_move):
    not_dragging = True
    pos_x, pos_y = None, None
    while True:
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN and not_dragging and redtoken_rect.collidepoint(event.pos):
                # start of dragging on red token pile.
                not_dragging = False
                pos_x, pos_y = event.pos
            elif event.type == MOUSEMOTION and not not_dragging:
                # update the position of the red token being dragged
                pos_x, pos_y = event.pos
            elif event.type == MOUSEBUTTONUP and not not_dragging:
                # let go of the token being dragged
                if pos_y < y_margin and pos_x > x_margin and pos_x < screen_width - x_margin:
                    # let go at the top of the screen.
                    col = int((pos_x - x_margin) / element_size)
                    if is_valid(board, col):
                        animate_drop_effect(board, col, human)
                        board[col][lowest_space(board, col)] = human
                        draw_board(board)
                        pygame.display.update()
                        return
                pos_x, pos_y = None, None
                not_dragging = True
        if pos_x != None and pos_y != None:
            draw_board(board, {'x':pos_x - element_size // 2, 'y':pos_y - element_size // 2, 'turn':human})
        else:
            draw_board(board)
            
        if first_move:
            # Show the help arrow for the player's first move.
            game_display.blit(help_img, help_rect)

        pygame.display.update()
        clock.tick()

def computer_animate_effect(board, col):
    pos_x = blacktoken_rect.left
    pos_y = blacktoken_rect.top
    speed = 8
    # moving the black tile up
    while pos_y > (y_margin - element_size):
        pos_y -= speed
        draw_board(board, {'x':pos_x, 'y':pos_y, 'turn':computer})
        pygame.display.update()
        clock.tick()
    # moving the black tile over
    pos_y = y_margin - element_size
    speed = 7
    while pos_x > (x_margin + col * element_size):
        pos_x -= speed
        draw_board(board, {'x':pos_x, 'y':pos_y, 'turn':computer})
        pygame.display.update()
        clock.tick()
    # dropping the black tile
    animate_drop_effect(board, col, computer)

def animate_drop_effect(board, col, player):
    pos_x = x_margin + col * element_size
    pos_y = y_margin - element_size
    speed = 3.0

    lowest = lowest_space(board, col)

    while True:
        pos_y += int(speed)
        if ((pos_y - y_margin) // element_size) >= lowest:
            return
        draw_board(board, {'x':pos_x, 'y':pos_y, 'turn':player})
        pygame.display.update()
        clock.tick()


def minimax(board, player, depth):
    if depth == 0 or is_full(board):
        return [0] * board_width

    if player == computer:
        opponent = human
    else:
        opponent = computer

    # Figure out the best move to make.
    possible_moves = [0] * board_width
    for moves in range(board_width):
        board_copy = copy.deepcopy(board)
        if not is_valid(board_copy, moves):
            continue
        check_move(board_copy, player, moves)
        if is_win(board_copy, player):
            # a winning move automatically gets a perfect fitness
            possible_moves[moves] = 1
            break # don't bother calculating other moves
        else:
            # do other player's counter moves and determine best one
            if is_full(board_copy):
                possible_moves[moves] = 0
            else:
                for opponent_moves in range(board_width):
                    board_copy2 = copy.deepcopy(board_copy)
                    if not is_valid(board_copy2, opponent_moves):
                        continue
                    check_move(board_copy2, opponent, opponent)
                    if is_win(board_copy2, opponent):
                        # a losing move automatically gets the worst fitness
                        possible_moves[moves] = -1
                        break
                    else:
                        # do the recursive call to minimax()
                        results = minimax(board_copy2, player, depth - 1)
                        possible_moves[moves] += (sum(results) / board_width) / board_width
    return possible_moves


def is_win(board, player):
    
    for y in range(board_height - 3):
        for x in range(board_width):
            if board[x][y] == board[x][y+1] == board[x][y+2] ==  board[x][y+3] == player:
                return True
            
    for y in range(board_height - 3):
        for x in range(board_width):
            if board[x][y] ==  board[x][y+1] == board[x][y+2] == board[x][y+3] == player:
                return True

    for x in range(board_width - 3):
        for y in range(board_height - 3):
            if board[x][y] == board[x+1][y+1] == board[x+2][y+2] == board[x+3][y+3] == player:
                return True
            

    for x in range(board_width - 3):
        for y in range(3, board_height):
            if board[x][y] == board[x+1][y-1] == board[x+2][y-2] == board[x+3][y-3] == player:
                return True
    

    return False

def draw_board(board, extra_token=None):
    game_display.fill(bgcolor)

    # draw tokens
    token_rect = pygame.Rect(0, 0, element_size, element_size)
    for x in range(board_width):
        for y in range(board_height):
            token_rect.topleft = (x_margin + (x * element_size), y_margin + (y * element_size))
            if board[x][y] == human:
                game_display.blit(redtoken_img, token_rect)
            elif board[x][y] == computer:
                game_display.blit(blacktoken_img, token_rect)

    # draw the extra token
    if extra_token != None:
        if extra_token['turn'] == human:
            game_display.blit(redtoken_img, (extra_token['x'], extra_token['y'], element_size, element_size))
        elif extra_token['turn'] == computer:
            game_display.blit(blacktoken_img, (extra_token['x'], extra_token['y'], element_size, element_size))

    # draw board over the tokens
    for x in range(board_width):
        for y in range(board_height):
            token_rect.topleft = (x_margin + (x * element_size), y_margin + (y * element_size))
            game_display.blit(element_img, token_rect)

    # draw the red and black tokens off to the side
    game_display.blit(redtoken_img, redtoken_rect) # red on the left
    game_display.blit(blacktoken_img, blacktoken_rect) # black on the right


if __name__ == '__main__':
    main()
