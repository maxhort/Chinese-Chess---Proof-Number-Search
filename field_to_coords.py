from draw import get_coords_intersection
def get_coord_mapping(board_width,piece_size):
    mapping = dict()
    for r in range(1,11):
        for f in range(1,10):
            mapping[(r,f)] = get_coords_intersection(r,f,board_width,piece_size)
    return mapping