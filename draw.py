import pygame
black = (0,0,0)
white = (255,255,255)
background_image = pygame.image.load("images/background.jpg")
rect = background_image.get_rect()
def set_background(gameDisplay):
    gameDisplay.fill(white)
    gameDisplay.blit(background_image, rect)


def draw_lines(gameDisplay,board_width,board_length,piece_size):
    pygame.draw.rect(gameDisplay,black,(piece_size,piece_size,board_width-2*piece_size,board_length),4)
    place_text(gameDisplay,'10',(piece_size-piece_size/1.5,piece_size-piece_size/8))
    place_text(gameDisplay,'1',(board_width-piece_size+piece_size/1.5,piece_size-piece_size/8),True)

    place_text(gameDisplay,str(1),(piece_size,board_length+piece_size+piece_size/2))
    place_text(gameDisplay,str(9),(piece_size,piece_size-piece_size/1.5),True)
    # draw rows
    for r in range(1,10):
        pygame.draw.line(gameDisplay,black,(piece_size,piece_size+piece_size*r),
                        (board_width-piece_size,piece_size+piece_size*r),2)
        place_text(gameDisplay,str(10-r),(piece_size-piece_size/1.5,piece_size+piece_size*r-piece_size/8))
        place_text(gameDisplay,str(r+1),(board_width-piece_size+piece_size/1.5,piece_size+piece_size*r-piece_size/8),True)
    for c in range(1,9):
        pygame.draw.line(gameDisplay,black,(piece_size+piece_size*c,piece_size),
                        (piece_size+piece_size*c,piece_size*4+piece_size),2)
        pygame.draw.line(gameDisplay,black,(piece_size+piece_size*c,piece_size*5+piece_size),
                        (piece_size+piece_size*c,board_length+piece_size),2)
        place_text(gameDisplay,str(c+1),(piece_size+piece_size*c,board_length+piece_size+piece_size/2))
        place_text(gameDisplay,str(9-c),(piece_size+piece_size*c,piece_size-piece_size/1.5),True)


def place_text(gameDisplay,text, pos, rotate = False):
    font = pygame.font.SysFont('Arial', 12)
    textSurface = font.render(text, True, black)
    if rotate:
        textSurface = pygame.transform.rotate(textSurface,180)
    gameDisplay.blit(textSurface, pos)


def get_coords_intersection(r,f,board_width,piece_size):
    # rank from 1-10
    # file from 1-9
    y = board_width-piece_size*(r-1)
    x = piece_size*f
    return (x,y)
def draw_castle(gameDisplay,board_width,piece_size):
    from_intersection = get_coords_intersection(1,4,board_width,piece_size)
    to_intersection = get_coords_intersection(3,6,board_width,piece_size)
    pygame.draw.line(gameDisplay,black,from_intersection,to_intersection,2)

    from_intersection = get_coords_intersection(1,6,board_width,piece_size)
    to_intersection = get_coords_intersection(3,4,board_width,piece_size)
    pygame.draw.line(gameDisplay,black,from_intersection,to_intersection,2)

    from_intersection = get_coords_intersection(8,4,board_width,piece_size)
    to_intersection = get_coords_intersection(10,6,board_width,piece_size)
    pygame.draw.line(gameDisplay,black,from_intersection,to_intersection,2)

    from_intersection = get_coords_intersection(8,6,board_width,piece_size)
    to_intersection = get_coords_intersection(10,4,board_width,piece_size)
    pygame.draw.line(gameDisplay,black,from_intersection,to_intersection,2)



def get_coords_piece(board_width,piece_size,r,f):
    # rank from 1-10
    # file from 1-9
    y = board_width-piece_size*.4-piece_size*(r-1)
    x = piece_size*.6+piece_size*(f-1)
    return (x,y)

def draw_pieces(gameDisplay,board_width,piece_size,pieces_red, pieces_black):
    for piece in pieces_red + pieces_black:
        pos = get_coords_piece(board_width,piece_size,piece['pos'][0],piece['pos'][1])
        gameDisplay.blit(piece['img'], pos)


def update_game(gameDisplay,board_width,board_length,piece_size,pieces_red, pieces_black):
    set_background(gameDisplay)
    draw_lines(gameDisplay,board_width,board_length,piece_size)
    draw_castle(gameDisplay,board_width,piece_size)


    draw_pieces(gameDisplay,board_width,piece_size,pieces_red, pieces_black)