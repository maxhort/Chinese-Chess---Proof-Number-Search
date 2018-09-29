import numpy as np

def translate_coord(pos):
    return (10-pos[0], 9-pos[1])
def to_board_rep(pieces_red,pieces_black):
    piece_list = []
    for p in pieces_red+pieces_black:
        index = p["type"] + (10 if p["color"] == "black" else 0)
        pos= p["pos"]
        piece_list.append((translate_coord(pos),index))
    return piece_list

def get_moves_king(board,position):
    moves = []
    current_r, current_c = translate_coord(position)
    color = board[current_r,current_c] // 10
    for r,c in [(1,0),(-1,0),(0,1),(0,-1)]:
        new_r,new_c = current_r + r, current_c + c
        if current_r<3 and new_r>=3:continue
        if current_r>6 and new_r<=6:continue
        if new_r >= 10 or new_r<0:continue
        if new_c<=2 or new_c >=6:continue
            
        if board[new_r][new_c] // 10 == color:continue
        moves.append((new_r,new_c))
    return moves

def get_moves_advisor(board,position):
    moves = []
    current_r, current_c = translate_coord(position)
    color = board[current_r,current_c] // 10
    for r,c in [(1,1),(-1,1),(-1,-1),(1,-1)]:
        new_r,new_c = current_r + r, current_c + c
        if current_r<3 and new_r>=3:continue
        if current_r>6 and new_r<=6:continue
        if new_r >= 10 or new_r<0:continue
        if new_c<=2 or new_c >=6:continue
            
        if board[new_r][new_c] // 10 == color:continue
        moves.append((new_r,new_c))
    return moves

def get_moves_elephant(board,position):
    moves = []
    current_r, current_c = translate_coord(position)
    color = board[current_r,current_c] // 10
    for r,c in [(2,2),(-2,2),(-2,-2),(2,-2)]:
        new_r,new_c = current_r + r, current_c + c
        if current_r<=4 and new_r>=5:continue
        if current_r>=5 and new_r<=4:continue
        if new_r >= 10 or new_r<0:continue
        if new_c<0 or new_c >=9:continue
            
        if board[new_r][new_c] // 10 == color:continue
        moves.append((new_r,new_c))
    return moves

def get_moves_horse(board,position):
    moves = []
    current_r, current_c = translate_coord(position)
    color = board[current_r,current_c] // 10
    for r,c in [(1,0),(-1,0),(0,-1),(0,1)]:
        # Check if orthogonal move is blocked
        intermediate_r,intermediate_c = current_r + r, current_c + c
        if intermediate_r >= 10 or intermediate_r<0:continue
        if intermediate_c<0 or intermediate_c >=9:continue
        if board[intermediate_r][intermediate_c] != -1:continue
            
        sides = []
        if c==0:sides = [(r,1),(r,-1)]
        else: sides = [(1,c),(-1,c)]
        for r2,c2 in sides:
            new_r = intermediate_r+r2
            new_c = intermediate_c+c2
            if new_r >= 10 or new_r<0:continue
            if new_c<0 or new_c >=9:continue

            if board[new_r][new_c] // 10 == color:continue
            moves.append((new_r,new_c))
    return moves

def get_moves_chariot(board,position):
    moves = []
    current_r, current_c = translate_coord(position)
    color = board[current_r,current_c] // 10
    for r,c in [(1,0),(-1,0),(0,-1),(0,1)]:
        # Check if orthogonal move is blocked
        i = 1
        while True:
            new_r,new_c = current_r + i*r, current_c + i*c
            if new_r >= 10 or new_r<0:break
            if new_c<0 or new_c >=9:break

            if board[new_r][new_c] // 10 == color:break
            elif board[new_r][new_c] == -1:
                moves.append((new_r,new_c))
            else: # capture opponent piece
                moves.append((new_r,new_c))
                break
            i+=1
    return moves

def get_moves_cannon(board,position):
    moves = []
    current_r, current_c = translate_coord(position)
    color = board[current_r,current_c] // 10
    for r,c in [(1,0),(-1,0),(0,-1),(0,1)]:
        # Check if orthogonal move is blocked
        i = 1
        jump = False
        while True:
            new_r,new_c = current_r + i*r, current_c + i*c
            i+=1
            if new_r >= 10 or new_r<0:break
            if new_c<0 or new_c >=9:break
            if board[new_r][new_c] != -1 and not jump: 
                jump = True
                continue
            if not jump:
                moves.append((new_r,new_c))
                continue
            
            if board[new_r][new_c] // 10 == color:
                break
            elif board[new_r][new_c] == -1:continue
            else: # capture opponent piece
                moves.append((new_r,new_c))
                break      
    return moves

def get_moves_soldier(board,position):
    moves = []
    current_r, current_c = translate_coord(position)
    color = board[current_r,current_c] // 10
    
    possible = []
    if color == 0 and current_r<=4:
        possible = [(-1,0),(0,-1),(0,1)]
    elif color == 0:
        possible = [(-1,0)]
    elif color == 1 and current_r>=5:
        possible = [(1,0),(0,-1),(0,1)]
    else:
        possible = [(1,0)]
    for r,c in possible:
        # Check if orthogonal move is blocked

        new_r,new_c = current_r + r, current_c + c
        if new_r >= 10 or new_r<0:continue
        if new_c<0 or new_c >=9:continue
        if board[new_r][new_c] // 10 == color:continue
        moves.append((new_r,new_c)) 
    return moves

move_per_type = {1:get_moves_king,
                2:get_moves_advisor,
                3:get_moves_elephant,
                4:get_moves_horse,
                5:get_moves_chariot,
                6:get_moves_cannon,
                7:get_moves_soldier}

# def in_check(board, current_pos, new_pos, color):
#     return False

def in_check(current_pos, new_pos, color,board,player_pieces,opponent_pieces):
    backup_player = [dict(x) for x in player_pieces]
    backup_oppenent = list(opponent_pieces)

    king_index = 1 + color * 10
    r,c = np.where(board==king_index)
    r = r[0]
    c = c[0]
    king_pos = (r,c) if (r,c) != current_pos else new_pos
    r,c = king_pos
    opponent_king = 1 + ((1+color)%2) * 10
    o_r,o_c = np.where(board==opponent_king)
    o_r = o_r[0]
    o_c = o_c[0]
    opponent_king_pos = (o_r,o_c)

    # check if kings in a row
    board[new_pos[0]][new_pos[1]] = int(board[current_pos[0]][current_pos[1]])
    board[current_pos[0]][current_pos[1]] = -1

    # check if both kings face each other
    if c == o_c:
        for r in range(min(o_r,r)+1,max(o_r,r)):
            if board[r][c] != -1:break
        else:
            return True

    # pieces are being updated
    translated_current = translate_coord(current_pos)
    translated_new = translate_coord(new_pos)
    #update player pieces
    move_index = [i for i,p in enumerate(player_pieces) if p["pos"] == translated_current][0]
    player_pieces[move_index]["pos"] = translated_new
    #update opponent pieces
    delete_piece = [p for i,p in enumerate(opponent_pieces) if p["pos"] == translated_new]
    if delete_piece:
        opponent_pieces.remove(delete_piece[0])
    for p in opponent_pieces:
        moves = get_possible_moves(player_pieces,opponent_pieces,p["pos"],p["type"],check=False)
        if king_pos in moves: 
            return True
    return False

def in_check2(current_pos, new_pos, color,player_pieces,opponent_pieces):
    r,c = translate_coord([p for p in player_pieces if p["type"]==1][0]["pos"])
    king_pos = (r,c) if (r,c) != current_pos else new_pos
    r,c = king_pos

    o_r,o_c = translate_coord([p for p in opponent_pieces if p["type"]==1][0]["pos"])
    opponent_king_pos = (o_r,o_c)

    # check if both kings face each other
    #print (c,o_c, player_pieces, opponent_pieces)
    check_c, check_op_c = 9-c, 9-o_c
    check_r, check_op_r = 10-r, 10-o_r
    if check_c == check_op_c:
        if any(p for p in player_pieces if p["pos"][1] == check_c and min(check_r,check_op_r)<p["pos"][0] and max(check_r,check_op_r)>p["pos"][0]):
            pass
        elif any(p for p in opponent_pieces if p["pos"][1] == check_c and min(check_r,check_op_r)<p["pos"][0] and max(check_r,check_op_r)>p["pos"][0]):
            pass
        else:
            return True
    # pieces are being updated
    translated_current = translate_coord(current_pos)
    translated_new = translate_coord(new_pos)
    #update player pieces
    move_index = [i for i,p in enumerate(player_pieces) if p["pos"] == translated_current][0]
    player_pieces[move_index]["pos"] = translated_new
    #update opponent pieces
    delete_piece = [p for i,p in enumerate(opponent_pieces) if p["pos"] == translated_new]
    if delete_piece:
        opponent_pieces.remove(delete_piece[0])
    for p in opponent_pieces:
        moves = get_possible_moves(player_pieces,opponent_pieces,p["pos"],p["type"],check=False)
        if king_pos in moves: 
            return True
    return False
def get_possible_moves(pieces_red,pieces_black,piece_position,piece_type,check=True):
    global move_per_type

    pieces = to_board_rep(pieces_red,pieces_black)
    board = np.zeros((10,9))
    board.fill(-1)
    for (r,c),t in pieces:
        board[r][c] = t
    current_r, current_c = translate_coord(piece_position)
    color = board[current_r,current_c] // 10
    opponent_pieces = pieces_black if color == 0 else pieces_red
    player_pieces = pieces_red if color == 0 else pieces_black
    moves = move_per_type[piece_type](board,piece_position)
    if check:
        pp = lambda: [dict(x) for x in player_pieces]
        op = lambda: [dict(x) for x in opponent_pieces]
        moves = [m for m in moves if not in_check2((current_r,current_c),m,color,#np.array(board),
                                            pp(),op())]
    else:
        # don't translate, just used for checking if attacked
        return moves
    moves = [translate_coord(c) for c in moves]
    return moves