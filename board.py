# piece_test = pygame.image.load("images/red/king.png")
# piece_test = pygame.transform.scale(piece_test, (int(piece_size-10), int(piece_size-10)))
import pygame
RED_KING = pygame.image.load("images/red/king.png")
RED_ADVISOR = pygame.image.load("images/red/advisor.png")
RED_ELEPHANT = pygame.image.load("images/red/elephant.png")
RED_HORSE = pygame.image.load("images/red/horse.png")
RED_CHARIOT = pygame.image.load("images/red/chariot.png")
RED_CANNON = pygame.image.load("images/red/cannon.png")
RED_SOLDIER = pygame.image.load("images/red/soldier.png")
RED_PIECES = [RED_KING,RED_ADVISOR,RED_ELEPHANT,RED_HORSE,RED_CHARIOT,RED_CANNON,RED_SOLDIER]

RED_KING_BW = pygame.image.load("images/red/king_bw.png")
RED_ADVISOR_BW = pygame.image.load("images/red/advisor_bw.png")
RED_ELEPHANT_BW = pygame.image.load("images/red/elephant_bw.png")
RED_HORSE_BW = pygame.image.load("images/red/horse_bw.png")
RED_CHARIOT_BW = pygame.image.load("images/red/chariot_bw.png")
RED_CANNON_BW = pygame.image.load("images/red/cannon_bw.png")
RED_SOLDIER_BW = pygame.image.load("images/red/soldier_bw.png")
RED_PIECES_BW = [RED_KING_BW,RED_ADVISOR_BW,RED_ELEPHANT_BW,RED_HORSE_BW,RED_CHARIOT_BW,RED_CANNON_BW,RED_SOLDIER_BW]

BLACK_KING = pygame.image.load("images/black/king.png")
BLACK_ADVISOR = pygame.image.load("images/black/advisor.png")
BLACK_ELEPHANT = pygame.image.load("images/black/elephant.png")
BLACK_HORSE = pygame.image.load("images/black/horse.png")
BLACK_CHARIOT = pygame.image.load("images/black/chariot.png")
BLACK_CANNON = pygame.image.load("images/black/cannon.png")
BLACK_SOLDIER = pygame.image.load("images/black/soldier.png")
BLACK_PIECES = [BLACK_KING,BLACK_ADVISOR,BLACK_ELEPHANT,BLACK_HORSE,BLACK_CHARIOT,BLACK_CANNON,BLACK_SOLDIER]

BLACK_KING_BW = pygame.image.load("images/black/king_bw.png")
BLACK_ADVISOR_BW = pygame.image.load("images/black/advisor_bw.png")
BLACK_ELEPHANT_BW = pygame.image.load("images/black/elephant_bw.png")
BLACK_HORSE_BW = pygame.image.load("images/black/horse_bw.png")
BLACK_CHARIOT_BW = pygame.image.load("images/black/chariot_bw.png")
BLACK_CANNON_BW = pygame.image.load("images/black/cannon_bw.png")
BLACK_SOLDIER_BW = pygame.image.load("images/black/soldier_bw.png")
BLACK_PIECES_BW = [BLACK_KING_BW,BLACK_ADVISOR_BW,BLACK_ELEPHANT_BW,BLACK_HORSE_BW,BLACK_CHARIOT_BW,BLACK_CANNON_BW,BLACK_SOLDIER_BW]

def get_piece(piece, pos,piece_size,t,color):
    return {"img":pygame.transform.scale(piece, (int(piece_size-10), int(piece_size-10))),
            "pos":pos,
            "type":t,
            "color":color}



def get_initial_board(piece_size):
    red_pieces = [get_piece(RED_KING,(1,5),piece_size,1,"red"),
                get_piece(RED_ADVISOR,(1,4),piece_size,2,"red"),
                get_piece(RED_ADVISOR,(1,6),piece_size,2,"red"),
                get_piece(RED_ELEPHANT,(1,3),piece_size,3,"red"),
                get_piece(RED_ELEPHANT,(1,7),piece_size,3,"red"),
                get_piece(RED_HORSE,(1,2),piece_size,4,"red"),
                get_piece(RED_HORSE,(1,8),piece_size,4,"red"),
                get_piece(RED_CHARIOT,(1,1),piece_size,5,"red"),
                get_piece(RED_CHARIOT,(1,9),piece_size,5,"red"),
                get_piece(RED_CANNON,(3,2),piece_size,6,"red"),
                get_piece(RED_CANNON,(3,8),piece_size,6,"red"),
                get_piece(RED_SOLDIER,(4,1),piece_size,7,"red"),
                get_piece(RED_SOLDIER,(4,3),piece_size,7,"red"),
                get_piece(RED_SOLDIER,(4,5),piece_size,7,"red"),
                get_piece(RED_SOLDIER,(4,7),piece_size,7,"red"),
                get_piece(RED_SOLDIER,(4,9),piece_size,7,"red")]
    black_pieces = [get_piece(BLACK_KING,(10,5),piece_size,1,"black"),
                get_piece(BLACK_ADVISOR,(10,4),piece_size,2,"black"),
                get_piece(BLACK_ADVISOR,(10,6),piece_size,2,"black"),
                get_piece(BLACK_ELEPHANT,(10,3),piece_size,3,"black"),
                get_piece(BLACK_ELEPHANT,(10,7),piece_size,3,"black"),
                get_piece(BLACK_HORSE,(10,2),piece_size,4,"black"),
                get_piece(BLACK_HORSE,(10,8),piece_size,4,"black"),
                get_piece(BLACK_CHARIOT,(10,1),piece_size,5,"black"),
                get_piece(BLACK_CHARIOT,(10,9),piece_size,5,"black"),
                get_piece(BLACK_CANNON,(8,2),piece_size,6,"black"),
                get_piece(BLACK_CANNON,(8,8),piece_size,6,"black"),
                get_piece(BLACK_SOLDIER,(7,1),piece_size,7,"black"),
                get_piece(BLACK_SOLDIER,(7,3),piece_size,7,"black"),
                get_piece(BLACK_SOLDIER,(7,5),piece_size,7,"black"),
                get_piece(BLACK_SOLDIER,(7,7),piece_size,7,"black"),
                get_piece(BLACK_SOLDIER,(7,9),piece_size,7,"black")]
    return red_pieces,black_pieces
     

def clean_board():
    return [],[]