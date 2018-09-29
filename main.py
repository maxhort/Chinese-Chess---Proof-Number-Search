import pygame
from draw import update_game, get_coords_intersection
import board
import Button
from field_to_coords import get_coord_mapping
from move_calculation import get_possible_moves
from PN import performPN
pygame.init()

delete_icon = pygame.image.load("images/delete_button.png")
possible_move_overlay = pygame.image.load("images/possible_move.png")
width, length = 800,600
gameDisplay = pygame.display.set_mode((width, length))
pygame.display.set_caption("XiangQi")

clock = pygame.time.Clock() # FPS
done =  False

black = (0,0,0)
white = (255,255,255)

piece_size = (min(width,length)*0.9) / 10
delete_icon = pygame.transform.scale(delete_icon,(int(piece_size),int(piece_size)))
possible_move_overlay = pygame.transform.scale(possible_move_overlay,(int(piece_size/2),int(piece_size/2)))
board_width = piece_size*10
board_length = piece_size*9

coord_mapping = get_coord_mapping(board_width,piece_size)

pieces_red = []
pieces_black = []

def reset_selection():
    global delete,place_piece,possible_moves,mousefollow,pieces_red,pieces_black
    delete = False
    if place_piece:
        place_piece = False
        possible_moves = []
        if mousefollow['color']=="red":pieces_red.append(mousefollow)
        else:pieces_black.append(mousefollow)
    mousefollow = None

def init_pieces():
    global pieces_red,pieces_black
    reset_selection()
    clear_pieces()
    pieces_red,pieces_black = board.get_initial_board(piece_size)

def clear_pieces():
    global pieces_red,pieces_black
    reset_selection()
    pieces_red,pieces_black = board.clean_board()

def change_turn():
    global turn
    if turn == "red":
        turn = "black"
    else:
        turn = "red"
    button_turn.change_turn()

def select_delete():
    global delete_icon,mousefollow,delete
    mousefollow = {"img":delete_icon}
    delete = True

def check_delete(mouse_position,piece_size=piece_size):
    global coord_mapping,pieces_red,pieces_black
    def distance(c1,c2):
        return (abs(c1[0]-c2[0])**2 +  abs(c1[1]-c2[1])**2)**0.5
    for k,v in coord_mapping.items():
        if distance(mouse_position,v) <= piece_size/3:
            if any(k==p["pos"] for p in pieces_red):
                pieces_red.remove([p for p in pieces_red if p["pos"]==k][0])
                return
            if any(k==p["pos"] for p in pieces_black):
                pieces_black.remove([p for p in pieces_black if p["pos"]==k][0])
                return
            return 


def select_piece(image,t,color,size=(50,50)):
    global mousefollow,pieces_red,pieces_black
    max_freq = {1:1,2:2,3:2,4:2,5:2,6:2,7:5}
    freq = max_freq[t]
    if color == "red":
        current = sum(p["type"] == t for p in pieces_red)
        if current >= freq:return
    else:
        current = sum(p["type"] == t for p in pieces_black)
        if current >= freq:return
    mousefollow = {"img":pygame.transform.scale(image,size),
                    "type":t,
                    "color":color}

def release_piece_add(mouse_position,piece_size=piece_size):
    global coord_mapping,pieces_red,pieces_black
    def distance(c1,c2):
        return (abs(c1[0]-c2[0])**2 +  abs(c1[1]-c2[1])**2)**0.5
    for k,v in coord_mapping.items():
        if distance(mouse_position,v) <= piece_size/3:
            if any(k==p["pos"] for p in pieces_black + pieces_red):return
            mousefollow["pos"] = k
            if mousefollow["color"] == 'red':
                pieces_red.append(mousefollow)
            else:
                pieces_black.append(mousefollow)
            return 


def release_piece_move(mouse_position):
    global coord_mapping,pieces_red,pieces_black,possible_moves,mousefollow,place_piece,turn
    def distance(c1,c2):
        return (abs(c1[0]-c2[0])**2 +  abs(c1[1]-c2[1])**2)**0.5
    for k,v in coord_mapping.items():
        if distance(mouse_position,v) <= piece_size/3:
            if k not in possible_moves:return
            mousefollow["pos"] = k
            if turn == "red":
                pieces_red.append(mousefollow)
                if any(k==p["pos"] for p in pieces_black):
                    remove_piece = [p for p in pieces_black if k==p["pos"]][0]
                    pieces_black.remove(remove_piece)
            else:
                pieces_black.append(mousefollow)
                if any(k==p["pos"] for p in pieces_red):
                    remove_piece = [p for p in pieces_red if k==p["pos"]][0]
                    pieces_red.remove(remove_piece)
            change_turn()
            place_piece = False
            mousefollow = None
            possible_moves = []
            
            

def select_piece_move(mouse_position):
    global turn, coord_mapping,pieces_red,pieces_black,place_piece,possible_moves,mousefollow
    def distance(c1,c2):
        return (abs(c1[0]-c2[0])**2 +  abs(c1[1]-c2[1])**2)**0.5
    for k,v in coord_mapping.items():
        if distance(mouse_position,v) <= piece_size/3:
            if any(k==p["pos"] for p in pieces_red):
                if turn != "red":break
                selected_piece = [p for p in pieces_red if p["pos"]==k][0]
                mousefollow = selected_piece
                possible_moves = get_possible_moves(pieces_red,pieces_black,
                                                    selected_piece["pos"],selected_piece["type"])
                pieces_red.remove(selected_piece)
                place_piece = True
                return
            if any(k==p["pos"] for p in pieces_black):
                if turn != "black":break
                selected_piece = [p for p in pieces_black if p["pos"]==k][0]
                possible_moves = get_possible_moves(pieces_red,pieces_black,
                                                    selected_piece["pos"],selected_piece["type"])
                pieces_black.remove(selected_piece)
                mousefollow = selected_piece
                place_piece = True
                return
            return 


def solve_endgame():
    global pieces_red,pieces_black,turn
    print (pieces_red)
    print (pieces_black)
    performPN(pieces_red,pieces_black,turn,turn)
turn = "red"
buttons = []
button_turn = Button.TurnButton(pygame.image.load("images/turn_red.png"),
                        pygame.image.load("images/turn_black.png"),
                        (width-230,10),(200,20),turn,lambda: change_turn())
button_init = Button.ImageButton(pygame.image.load("images/init_board.png"),
                        (width-230,50),(200,50),lambda: init_pieces())
button_clear = Button.ImageButton(pygame.image.load("images/clear_board.png"),
                        (width-230,125),(200,50),lambda: clear_pieces())

# due to late bindings
def return_lambda(piece,t,color):
    return lambda:select_piece(piece, t,color)
for i,(red, red_bw) in enumerate(zip(board.RED_PIECES,board.RED_PIECES_BW)):
    new_button = Button.PieceButton(red, red_bw,
                        (width-230+i*50-(200 if i>3 else 0),180 + (50 if i>3 else 0)),(50,50),
                        return_lambda(red, i+1,"red"))
    buttons.append(new_button)

for i,(black, black_bw) in enumerate(zip(board.BLACK_PIECES,board.BLACK_PIECES_BW)):
    new_button = Button.PieceButton(black, black_bw,
                        (width-230+i*50-(200 if i>3 else 0),285 + (50 if i>3 else 0)),(50,50),
                        return_lambda(black, i+1,"black"))
    buttons.append(new_button)

button_delete = Button.ImageButton(pygame.image.load("images/delete_button.png"),
                        (width-230,390),(50,50),lambda: select_delete())
button_solve = Button.ImageButton(pygame.image.load("images/analyze_button.png"),
                        (width-180,390),(50,50),lambda: solve_endgame())
buttons.append(button_turn)
buttons.append(button_init)
buttons.append(button_clear)
buttons.append(button_delete)
buttons.append(button_solve)

changed = True
mousefollow = None
delete = False
place_piece = False
possible_moves = []
def check_buttons():
    global pieces_red, pieces_black
    max_freq = {1:1,2:2,3:2,4:2,5:2,6:2,7:5}
    for i,button in enumerate(buttons[:14]):
        check_pieces = []
        if i<7:check_pieces = pieces_red
        else: check_pieces = pieces_black
        freq = max_freq[(i%7)+1]
        current = sum(p["type"] == (i%7+1) for p in check_pieces)
        if current >= freq:
            button.set_inactive()
        else:
            button.set_active()
while not done:
    if changed:
        update_game(gameDisplay,board_width,board_length,piece_size,pieces_red, pieces_black)
        if not place_piece:
            check_buttons()
        for button in buttons:
            button.draw(gameDisplay)
        for (r,f) in possible_moves:
            pos_x,pos_y = get_coords_intersection(r,f,board_width,piece_size)
            gameDisplay.blit(possible_move_overlay, (pos_x-int(piece_size/4),pos_y-int(piece_size/4)))
        changed = False
        if mousefollow:
            Mouse_x,Mouse_y = pygame.mouse.get_pos()
            gameDisplay.blit(mousefollow['img'], (Mouse_x-25,Mouse_y-25))
            changed = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: # Right mouseclick left = 1
            reset_selection()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and delete: # delete piece
            #delete = False  # DESIGN Choice, keep deletion tool after successful deletion
            check_delete(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mousefollow and not place_piece: # release piece add
            release_piece_add(pygame.mouse.get_pos())
            reset_selection()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and mousefollow and place_piece: # release piece move
            release_piece_move(pygame.mouse.get_pos())
            reset_selection()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # pick piece
            select_piece_move(pygame.mouse.get_pos())
        for button in buttons:
            button.event_handler(event)
        changed = True
    pygame.display.update()
    clock.tick(60)
