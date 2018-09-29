from collections import defaultdict
import board
from move_calculation import translate_coord, get_possible_moves
import pickle
pieces_red,pieces_black = board.get_initial_board(10)
turn = None
current_player = None
node_index = 1
pn_tree = defaultdict(dict)

def performPN(pieces_red, pieces_black,turn_color,player):
    global pn_tree, turn,current_player,node_index
    turn = turn_color
    current_player = player
    node_index = 1
    pieces_red,pieces_black = transform_piece_information(pieces_red,pieces_black)
    pn_tree = defaultdict(dict)
    pn_tree[0]["red"] = pieces_red
    pn_tree[0]["black"] = pieces_black
    pn_tree[0]["turn"] = "red"
    pn_tree[0]["type"] = "OR"
    pn_tree[0]["pn"] = 1
    pn_tree[0]["dpn"] = 1
    pn_tree[0]["children"] = []
    pn_tree[0]["parent"] = None
    pn_tree[0]["expanded"] = False
    pn_tree[0]["move"] = None
    PN(0)

def transform_piece_information(pieces_red,pieces_black):
    new_red = []
    new_black = []
    for p in pieces_red:
        new_red.append({"pos": p["pos"],"type":p["type"],"color":p["color"]})
    for p in pieces_black:
        new_black.append({"pos": p["pos"],"type":p["type"],"color":p["color"]})
    return new_red,new_black

def evaluate_node(node):
    global pn_tree
    check_pieces = pn_tree[node]["red"] if pn_tree[node]["turn"] == "red" else pn_tree[node]["black"]
    for piece in check_pieces:
        moves = get_possible_moves(pn_tree[node]["red"],pn_tree[node]["black"],piece["pos"],piece["type"])
        if moves:
            break
    # game is over
    else:
        # no move possible, of current player -> lost
        if current_player == pn_tree[node]["turn"]: return 0
        # opponent can't make a move -> won
        else: return 1
    return 2

def set_pn_dpn(node,evaluation = None):
    global pn_tree
    # set according to children
    if pn_tree[node]["expanded"]:
        if pn_tree[node]["type"] == "AND":
            pn_tree[node]["pn"] = sum(pn_tree[c]["pn"] for c in pn_tree[node]["children"])
            pn_tree[node]["dpn"] = min(pn_tree[c]["dpn"] for c in pn_tree[node]["children"])
        # OR Node
        else:
            pn_tree[node]["pn"] = min(pn_tree[c]["pn"] for c in pn_tree[node]["children"])
            pn_tree[node]["dpn"] = sum(pn_tree[c]["dpn"] for c in pn_tree[node]["children"])
    else:
        if evaluation == 0:
            pn_tree[node]["pn"] = float("inf")
            pn_tree[node]["dpn"] = 0
        elif evaluation == 1:
            pn_tree[node]["pn"] = 0
            pn_tree[node]["dpn"] = float("inf")
        else:
            pn_tree[node]["pn"] = 1
            pn_tree[node]["dpn"] = 1
            
def PN(root,max_nodes = 25000):
    global pn_tree,node_index
    evaluate_node(root)
    set_pn_dpn(root)
    while pn_tree[root]["pn"] != 0 and pn_tree[root]["dpn"] != 0 and node_index<max_nodes:
        mostProving = selectMostProvingNode(root) # can also be root itself
        expandNode(mostProving)
        root = updateAncestors(mostProving, root)
        # print (root,mostProving,pn_tree[mostProving]["move"],"nodes",node_index)
        # print ("___________________")
    #print (root,node_index)
    print ("nodes_used",node_index)
    printMostPromising(0)
    pickle.dump(pn_tree,open( "solution.p", "wb" ))
def selectMostProvingNode(root,verbose=False):
    global pn_tree
    while pn_tree[root]["expanded"]:
        children = pn_tree[root]["children"]
        # Lowest DPN
        if pn_tree[root]["type"] == "AND":
            vals = [pn_tree[c]["dpn"] for c in children]
        # Lowest PN
        else:
            vals = [pn_tree[c]["pn"] for c in children]
        root = children[vals.index(min(vals))]
        if verbose:
            print (root,pn_tree[root]["move"])
    return root

def printMostPromising(root):
    global pn_tree
    while pn_tree[root]["children"]:
        children = pn_tree[root]["children"]
        # Lowest DPN
        if pn_tree[root]["type"] == "AND":
            vals = [pn_tree[c]["dpn"] for c in children]
        # Lowest PN
        else:
            vals = [pn_tree[c]["pn"] for c in children]
        root = children[vals.index(min(vals))]
        print (root,pn_tree[root]["move"])
    return root
def expandNode(node):
    global pn_tree,node_index
    # generate all children
    # evaluate, check if any lost or won based on node type
    # set pn and dpn
    pn_tree[node]["expanded"] = True
    child_type = "AND" if pn_tree[node]["type"] == "OR" else "OR"
    child_turn = "red" if pn_tree[node]["turn"] == "black" else "black"
    pieces_red = pn_tree[node]["red"]
    pieces_black = pn_tree[node]["black"]
    pieces_to_check = pieces_red if pn_tree[node]["turn"] == "red" else pieces_black 
    pieces_opponent = pieces_black if pn_tree[node]["turn"] == "red" else pieces_red  
    #red = lambda: list(pieces_red)
    #black = lambda: list(pieces_black)
    current_pieces = lambda j,m,pieces: [p if j!= i else {"pos":m,"type":p["type"],"color":p["color"]} for j,p in enumerate(list(pieces))]
    #[p if j!= i else {"pos":move,"type":p["type"],"color":p["color"]} for j,p in enumerate(red())]
    opponent_pieces = lambda m,pieces: [p for p in list(pieces) if p["pos"] != m]
    #[p for p in black() if p["pos"] != move]
    for i,piece in enumerate(pieces_to_check):
        moves = get_possible_moves(pieces_red,pieces_black,piece["pos"],piece["type"])
        for move in moves:
            #print (piece["pos"],move)
            #new_red = red()
            #new_black = [p for p in black() if p["pos"] != move] 
            pn_tree[node]["children"].append(node_index)
            #new_red[i]["pos"] = move
            if pn_tree[node]["turn"] == "red":
                add_node(node_index,current_pieces(i,move,pieces_red),opponent_pieces(move,pieces_black),
                        child_turn,child_type,node,(piece["pos"],move))
            else:
                add_node(node_index,opponent_pieces(move,pieces_red),current_pieces(i,move,pieces_black),
                        child_turn,child_type,node,(piece["pos"],move))
            evaluation_result = evaluate_node(node_index)
            
            set_pn_dpn(node_index,evaluation_result)
            node_index += 1
            if evaluation_result == 1 and pn_tree[node]["type"] == "OR":return     # won
            if evaluation_result == 0 and pn_tree[node]["type"] == "AND":return    # lost
    

def add_node(node_id,pieces_red,pieces_black,turn,node_type,parent,move):
    global pn_tree
    pn_tree[node_id]["red"] = pieces_red
    pn_tree[node_id]["black"] = pieces_black
    pn_tree[node_id]["turn"] = turn
    pn_tree[node_id]["type"] = node_type
    pn_tree[node_id]["pn"] = 1
    pn_tree[node_id]["dpn"] = 1
    pn_tree[node_id]["children"] = []
    pn_tree[node_id]["parent"] = parent
    pn_tree[node_id]["expanded"] = False
    pn_tree[node_id]["move"] = move

def updateAncestors(node, root):
    global pn_tree
    while True:
        old_pn = pn_tree[node]["pn"]
        old_dpn = pn_tree[node]["dpn"]
        
        set_pn_dpn(node)
        if pn_tree[node]["pn"] == old_pn and pn_tree[node]["dpn"] == old_dpn:
            return node
        #
        if pn_tree[node]["pn"] == 0 or pn_tree[node]["dpn"] == 0:
            delete_subtree(node)
        #delete subtree
        if node == root:
            return root
        node = pn_tree[node]["parent"]
        
def delete_subtree(node,parent = True):
    return
    global pn_tree
    for c in pn_tree[node]["children"]:
        delete_subtree(c,parent = False)
    if not parent:
        del pn_tree[node]