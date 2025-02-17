# Importing Modules
import pygame
import requests
import rembg
from io import BytesIO

# Initialising pygame module
pygame.init()

# Setting Width and height of the Chess Game screen
WIDTH = 500
HEIGHT = 450

check = False
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Chess Game')

font = pygame.font.Font('freesansbold.ttf', 10)
medium_font = pygame.font.Font('freesansbold.ttf', 20)
big_font = pygame.font.Font('freesansbold.ttf', 25)

timer = pygame.time.Clock()
fps = 60

# game variables and images
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']

white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

white_moved = [False, False,False, False,False, False,False, False,
               False, False,False, False,False, False,False, False,]
black_moved = [False, False,False, False,False, False,False, False,
               False, False,False, False,False, False,False, False,]

captured_pieces_white = []
captured_pieces_black = []

piece_list = ['rook', 'knight', 'bishop', 'queen', 'king', 'pawn']
promote_pieces = ['rook', 'knight', 'bishop', 'queen']

# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
turn_step = 0
selection = 50
valid_moves = []

# url for chess pieces images
imagePath = []
assertPath = "D:/sourceCode/Python/python_games/pygameChess-main/assets/images/"
for i in piece_list:
    imagePath.append(assertPath + "black" + i +".png")

for i in piece_list:
    imagePath.append(assertPath + "white" + i +".png")

# load in game piece images (queen, king, rook, bishop, knight, pawn) x 2
black_rook = pygame.image.load(imagePath[0])
black_rook = pygame.transform.scale(black_rook, (40, 40))
black_rook_small = pygame.transform.scale(black_rook, (22.5, 22.5))

black_knight = pygame.image.load(imagePath[1])
black_knight = pygame.transform.scale(black_knight, (40, 40))
black_knight_small = pygame.transform.scale(black_knight, (22.5, 22.5))

black_bishop = pygame.image.load(imagePath[2])
black_bishop = pygame.transform.scale(black_bishop, (40, 40))
black_bishop_small = pygame.transform.scale(black_bishop, (22.5, 22.5))

black_queen = pygame.image.load(imagePath[3])
black_queen = pygame.transform.scale(black_queen, (40, 40))
black_queen_small = pygame.transform.scale(black_queen, (22.5, 22.5))

black_king = pygame.image.load(imagePath[4])
black_king = pygame.transform.scale(black_king, (40, 40))
black_king_small = pygame.transform.scale(black_king, (22.5, 22.5))

black_pawn = pygame.image.load(imagePath[5])
black_pawn = pygame.transform.scale(black_pawn, (32.5, 32.5))
black_pawn_small = pygame.transform.scale(black_pawn, (22.5, 22.5))

white_rook = pygame.image.load(imagePath[6])
white_rook = pygame.transform.scale(white_rook, (40, 40))
white_rook_small = pygame.transform.scale(white_rook, (22.5, 22.5))

white_knight = pygame.image.load(imagePath[7])
white_knight = pygame.transform.scale(white_knight, (40, 40))
white_knight_small = pygame.transform.scale(white_knight, (22.5, 22.5))

white_bishop = pygame.image.load(imagePath[8])
white_bishop = pygame.transform.scale(white_bishop, (40, 40))
white_bishop_small = pygame.transform.scale(white_bishop, (22.5, 22.5))

white_queen = pygame.image.load(imagePath[9])
white_queen = pygame.transform.scale(white_queen, (40, 40))
white_queen_small = pygame.transform.scale(white_queen, (22.5, 22.5))

white_king = pygame.image.load(imagePath[10])
white_king = pygame.transform.scale(white_king, (40, 40))
white_king_small = pygame.transform.scale(white_king, (22.5, 22.5))

white_pawn = pygame.image.load(imagePath[11])
white_pawn = pygame.transform.scale(white_pawn, (32.5, 32.5))
white_pawn_small = pygame.transform.scale(white_pawn, (22.5, 22.5))

white_images = [white_rook, white_knight, white_bishop, white_queen, white_king, white_pawn]
small_white_images = [white_rook_small, white_knight_small, white_bishop_small, white_king_small, white_queen_small, white_pawn_small]

black_images = [black_rook, black_knight, black_bishop, black_queen, black_king, black_pawn]
small_black_images = [black_rook_small, black_knight_small, black_bishop_small, black_queen_small, black_king_small, black_pawn_small]

# check variables/ flashing counter
counter = 0
winner = ''
game_over = False

white_promote = False
black_promote = False
promote_index = 50

black_ep = (50, 50)
white_ep = (50, 50)

# draw main game board
def draw_board():
    for i in range(0, 32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [column * 100, row * 50, 50, 50])
        else:
            pygame.draw.rect(screen, 'light gray', [column * 100 + 50, row * 50, 50, 50])
            
        pygame.draw.rect(screen, 'gray', [0, 400, WIDTH, 50])
        pygame.draw.rect(screen, 'gold', [0, 400, WIDTH, 50], 5)
        pygame.draw.rect(screen, 'gold', [400, 0, 100, HEIGHT], 5)
        status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                       'Black: Select a Piece to Move!', 'Black: Select a Destination!']
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 410))
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 50 * i), (400, 50 * i), 2)
            pygame.draw.line(screen, 'black', (50 * i, 0), (50 * i, 400), 2)
        screen.blit(medium_font.render('SURRENDER', True, 'black'), (405, 415))
        if white_promote or black_promote:
            draw_promote_bar()

# draw pieces onto board
def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 50 + 11, white_locations[i][1] * 50 + 15))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 50 + 5, white_locations[i][1] * 50 + 5))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * 50 + 1, white_locations[i][1] * 50 + 1, 50, 50], 2)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(
                black_pawn, (black_locations[i][0] * 50 + 11, black_locations[i][1] * 50 + 15))
        else:
            screen.blit(black_images[index], (black_locations[i]
                                              [0] * 50 + 5, black_locations[i][1] * 50 + 5))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 50 + 1, black_locations[i][1] * 50 + 1,
                                                  50, 50], 2)

# function to check all pieces valid options on board
def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    global castlingMoves
    castlingMoves = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list, castlingMoves = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list

#check if there is any pawns can be promoted
def check_promote():
    #change the promote flag to default
    white_promotion = False
    black_promotion = False
    promote_index = 50
    
    for i in range(len(white_pieces)):
        if white_pieces[i] == 'pawn':
            if white_locations[i][1] == 7:
                white_promotion = True
                promote_index = i
    for i in range(len(black_pieces)):
        if black_pieces[i] == 'pawn':
            if black_locations[i][1] == 0:
                black_promotion = True
                promote_index = i

    return white_promotion, black_promotion, promote_index

# draw a promote bar on the right of board
def draw_promote_bar():
    pygame.draw.rect(screen, 'light gray',(425, 0, 50, 200))
    if white_promote:
        for i in range(len(promote_pieces)):
            screen.blit(white_images[i],  [425, i * 50])
    else:
        for i in range(len(piece_list) - 2):
            screen.blit(black_images[i], [425, i * 50])
#listen to the mouse and choose the piece which pawn will promote to
def check_promote_select():
    mouse = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]
    
    x_pos = mouse[0] // 50
    y_pos = mouse[1] // 50
    if white_promote and left_click and x_pos > 7 and y_pos < 4:
        white_pieces[promote_index] = promote_pieces[y_pos]
    elif black_promote and left_click and x_pos > 7 and y_pos < 4:
        black_pieces[promote_index] = promote_pieces[y_pos]
# check king valid moves
def check_king(position, color):
    moves_list = []
    castlingMoves = check_castling()
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for kings, they can go one square any direction
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list, castlingMoves

# check queen valid moves
def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list

# check bishop moves
def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # up-right, up-left, down-right, down-left
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append(
                    (position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

# check rook moves
def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # down, up, right, left
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append(
                    (position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

# check valid pawn moves
def check_pawn(position, color):
    moves_list = []
    if color == 'white':
        if (position[0], position[1] + 1) not in white_locations and (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
            if (position[0], position[1] + 2) not in white_locations and (position[0], position[1] + 2) not in black_locations and position[1] == 1:
                moves_list.append((position[0], position[1] + 2))
        #check there is any thing pawn can captured
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
            
        #check if can en passant
        if(position[0] + 1, position[0] + 1) == black_ep:
            moves_list.append((position[0] + 1, position[1] + 1))
        if(position[0] - 1, position[0] + 1) == black_ep:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
            if (position[0], position[1] - 2) not in white_locations and \
                    (position[0], position[1] - 2) not in black_locations and position[1] == 6:
                moves_list.append((position[0], position[1] - 2))
        #check if there any thing pawn can captured
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
        
        #check if can en passant
        if (position[0] + 1, position[1] - 1) == white_ep:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) == white_ep:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list

# check valid knight moves
def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1),
               (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list

# check for valid moves for just selected piece
def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options

# draw valid moves on screen
def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(
            screen, color, (moves[i][0] * 50 + 25, moves[i][1] * 50 + 25), 5)

# draw captured pieces on side of screen
def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (412.5, 5 + 25 * i))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (462.5, 5 + 25 * i))

# draw a flashing square around king if in check
def draw_check():
    global check
    check = False
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    check = True
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [white_locations[king_index][0] * 50 + 1,
                                                              white_locations[king_index][1] * 50 + 1, 50, 50], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    check = True
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [black_locations[king_index][0] * 50 + 1,
                                                               black_locations[king_index][1] * 50 + 1, 50, 50], 5)

def draw_game_over():
    pygame.draw.rect(screen, 'black', [100, 100, 200, 35])
    screen.blit(font.render(f'{winner} won the game!', True, 'white'), (105, 105))
    screen.blit(font.render(f'Press ENTER to Restart!',True, 'white'), (105, 120))

#making castling
def check_castling():
    castle_moves = []
    rook_indexes = []
    rook_locations = []
    king_index = 0
    king_pos = (0, 0)
    if turn_step > 1:#if there is black's turn
        for i in range(len(white_pieces)):
            if white_pieces[i] == 'rook':
                rook_indexes.append(white_moved[i])
                rook_locations.append(white_locations[i])
            if white_pieces[i] == 'king':
                king_index = i
                king_pos = white_locations[i]
        if not white_moved[king_index] and False in rook_indexes and not check:
            for i in range(len(rook_indexes)):
                castle = True
                if rook_locations[i][0] > king_pos[0]:
                    #empty square between right rook of king and king
                    empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1]),
                                     (king_pos[0] + 3, king_pos[1])]
                else:
                    # empty squares between left rook of king and king
                    empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1])]
                for j in range(len(empty_squares)):
                    if empty_squares[j] in white_locations or empty_squares[j] in black_locations or \
                            empty_squares[j] in black_options or rook_indexes[i]:
                        castle = False
                if castle:
                    castle_moves.append((empty_squares[1], empty_squares[0]))
    else:
        for i in range(len(black_pieces)):
            if black_pieces[i] == 'rook':
                rook_indexes.append(black_moved[i])
                rook_locations.append(black_locations[i])
            if black_pieces[i] == 'king':
                king_index = i
                king_pos = black_locations[i]
        if not black_moved[king_index] and False in rook_indexes and not check:
            for i in range(len(rook_indexes)):
                castle = True
                if rook_locations[i][0] > king_pos[0]:
                    empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1]),
                                     (king_pos[0] + 3, king_pos[1])]
                else:
                    empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1])]
                for j in range(len(empty_squares)):
                    if empty_squares[j] in white_locations or empty_squares[j] in black_locations or \
                            empty_squares[j] in white_options or rook_indexes[i]:
                        castle = False
                if castle:
                    castle_moves.append((empty_squares[1], empty_squares[0]))
    return castle_moves

# draw a dot to know which king and rook will move to
def draw_castling(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0][0] * 50 + 25, moves[i][0][1] * 50 + 25), 5)

def check_en_passant(old_coords, new_coords):
    if turn_step <= 1:
        index = white_locations.index(old_coords)
        en_passant_piece = (new_coords[0], new_coords[1] - 1)
        piece = white_pieces[index]
    else:
        index = black_locations.index(old_coords)
        en_passant_piece = (new_coords[0], new_coords[1] + 1)
        piece = black_pieces[index]
    if piece == 'pawn' and abs(old_coords[1] - new_coords[1]) > 1:
        # if piece was pawn and moved two spaces, return EP coords as defined above
        pass
    else:
        en_passant_piece = (50, 50)
    return en_passant_piece
    
# main game loop
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
run = True
while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill('dark gray')
    
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()
    #check promote
    if not game_over:
        white_promote, black_promote, promote_index = check_promote()
        if white_promote or black_promote:
            draw_promote_bar()
            check_promote_select()
    #check castling
    if selection != 50:
        valid_moves = check_valid_moves()
        if turn_step <= 1:
            selected_piece = white_pieces[selection]
        else:
            selected_piece = black_pieces[selection]
        if selected_piece == 'king':
            draw_castling(castlingMoves)
        draw_valid(valid_moves)

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // 50
            y_coord = event.pos[1] // 50
            click_coords = (x_coord, y_coord)
            if turn_step <= 1: # if white is moving
                if click_coords == (8, 8) or click_coords == (9, 8):#click on surrender
                    winner = 'black'
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    selected_piece = white_locations[selection]
                    if turn_step == 0:
                        turn_step = 1
                if click_coords in valid_moves and selection != 50:
                    # check the en passant
                    white_ep = check_en_passant(white_locations[selection], click_coords)
                    white_locations[selection] = click_coords
                    white_moved[selection] = True
                    if click_coords in black_locations:
                        black_piece = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece])
                        if black_pieces[black_piece] == 'king':
                            winner = 'white'
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                    #add en passant
                    if click_coords == black_ep:
                        black_piece = black_locations.index((black_ep[0], black_ep[1] - 1))
                        captured_pieces_white.append(black_pieces[black_piece])
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                        black_moved.pop(black_piece)
                    #reset options
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 50
                    valid_moves = []
                #add an options for castling
                elif selection != 50 and selected_piece == 'king':
                    for q in range(len(castlingMoves)):
                        if click_coords == castlingMoves[q][0]:
                            white_locations[selection] = click_coords
                            white_moved[selection] = True
                            if click_coords == (1, 0):
                                rook_coords = (0, 0)
                            else:
                                rook_coords = (7, 0)
                            rook_index = white_locations.index(rook_coords)
                            white_locations[rook_index] = castlingMoves[q][1]
                            black_options = check_options(black_pieces, black_locations, 'black')
                            white_options = check_options(white_pieces, white_locations, 'white')
                            turn_step = 2
                            selection = 50
                            valid_moves = []
            if turn_step > 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'white'
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3
                if click_coords in valid_moves and selection != 50:
                    black_ep = check_en_passant(black_locations[selection], click_coords)
                    black_locations[selection] = click_coords
                    black_moved[selection] = True
                    if click_coords in white_locations:
                        white_piece = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[white_piece])
                        if white_pieces[white_piece] == 'king':
                            winner = 'black'
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                    # add an en passant
                    if click_coords == white_ep:
                        white_piece = white_locations.index((white_ep[0], white_ep[1] - 1))
                        captured_pieces_black.append(white_pieces[white_piece])
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                        white_moved.pop(white_piece)
                    # reset option
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 0
                    selection = 50
                    valid_moves = []

                #add an options for castling
                elif selection != 50 and selected_piece == 'king':
                    for q in range(len(castlingMoves)):
                        if click_coords == castlingMoves[q][0]:
                            black_locations[selection] = click_coords
                            black_moved[selection] = True
                            if click_coords == (1, 7):
                                rook_coords = (0, 7)
                            else:
                                rook_coords = (7, 7)
                            rook_index = black_locations.index(rook_coords)
                            black_locations[rook_index] = castlingMoves[q][1]
                            black_options = check_options(black_pieces, black_locations, 'black')
                            white_options = check_options(white_pieces, white_locations, 'white')
                            turn_step = 2
                            selection = 50
                            valid_moves = []
                            
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                
                white_moved = [False, False,False, False,False, False,False, False,
                                False, False,False, False,False, False,False, False,]
                white_moved = [False, False,False, False,False, False,False, False,
                                False, False,False, False,False, False,False, False,]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 50
                valid_moves = []
                black_options = check_options(
                    black_pieces, black_locations, 'black')
                white_options = check_options(
                    white_pieces, white_locations, 'white')

    if winner != '':
        game_over = True
        draw_game_over()
    print(white_ep, black_ep)
    pygame.display.flip()

pygame.quit()
