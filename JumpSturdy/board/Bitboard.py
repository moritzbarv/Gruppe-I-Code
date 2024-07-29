
def print_bitboard(bitboard):
    for rank in range(7, -1, -1):
        line = ""
        for file in range(7, -1, -1):
            square = rank * 8 + file
            if square in {0, 7, 56, 63}:
                line += "XX "
            else:
                if (bitboard >> square) & 1:
                    line += " 1 "
                else:
                    line += " 0 "
        print(line)
    print("\n")

def print_board(board):
    cell_width = max(len(cell) for row in board for cell in row)
    
    column_labels = " " * (len(str(len(board))) + 1) + " ".join(f'{chr(65 + col):>{cell_width}}' for col in range(len(board[0])))
    print(column_labels)
    
    for row_idx, row in enumerate(board):
        row_label = f'{8 - row_idx:>{len(str(len(board)))}}'
        print(f'{row_label} ' + ' '.join(f'{cell:>{cell_width}}' for cell in row))
    print("\n")


def parse_move(move):
    try:
        start_col = move[0].upper()
        start_row = int(move[1]) 
        end_col = move[2].upper()
        end_row = int(move[3]) 
        return ((start_col, start_row), (end_col, end_row))
    except (ValueError, IndexError):
        raise ValueError("Invalid move format. Please enter a move like 'e2e4'.")


def get_color(board_string):
    if board_string[-1] == 'b':
        return 'blue'
    elif board_string[-1] == 'r':
        return 'red'
    else:
        return None     


def game_over(bitboards, color):
    red_bitboard = bitboards['r'] | bitboards['rr'] | bitboards['br']
    blue_bitboard = bitboards['b'] | bitboards['bb'] | bitboards['rb']
    
    for col in range(1, 7):
        if (blue_bitboard >> (63 - col)) & 1:
            return True

    for col in range(1, 7):
        if (red_bitboard >> (63 - (56 + col))) & 1:
            return True

    if not generate_moves(bitboards, color):
        return True

    return False


def generate_column1(column):
    return ord(column.upper()) - ord('A')

def bitboard_to_array(bitboard):
    board_array = [['--' for _ in range(8)] for _ in range(8)]
    for pos in range(64):
        if bitboard & (1 << pos):
            row, col = divmod(63 - pos, 8)
            board_array[row][col] = '1'
    return board_array

def combine_bitboards(bitboards):
    combined_board = [['--' for _ in range(8)] for _ in range(8)]
    piece_symbols = {
        'r': 'R', 'b': 'B', 'rr': 'RR', 'rb': 'RB',
        'br': 'BR', 'bb': 'BB'
    }
    
    for piece, bitboard in bitboards.items():
        array = bitboard_to_array(bitboard)
        for row in range(8):
            for col in range(8):
                if array[row][col] == '1':
                    combined_board[row][col] = piece_symbols[piece]
    
    return combined_board

def change_board(bitboards, start, ziel):
    start_spalte, start_zeile = generate_column1(start[0]), 8 - int(start[1])
    ziel_spalte, ziel_zeile = generate_column1(ziel[0]), 8 - int(ziel[1])

    start_position = 63 - (start_zeile * 8 + start_spalte)
    ziel_position = 63 - (ziel_zeile * 8 + ziel_spalte)

    moving_piece = None
    for piece, bitboard in bitboards.items():
        if bitboard & (1 << start_position):
            moving_piece = piece
            break

    if not moving_piece:
        #print("Keine bewegliche Figur an der Startposition gefunden.")
        return bitboards

    bitboards[moving_piece] &= ~(1 << start_position)
    
    if moving_piece in ['r', 'b']:
        if not any(bitboards[p] & (1 << ziel_position) for p in bitboards):
            bitboards[moving_piece] |= (1 << ziel_position)
            #print('Auf leeres Feld gegangen')
        elif any(bitboards[p] & (1 << ziel_position) for p in ['b', 'bb', 'rb'] if moving_piece == 'r') or any(bitboards[p] & (1 << ziel_position) for p in ['r', 'rr', 'br'] if moving_piece == 'b'):
            for p in bitboards:
                if bitboards[p] & (1 << ziel_position):
                    bitboards[p] &= ~(1 << ziel_position)
            bitboards[moving_piece] |= (1 << ziel_position)
            #print('Gegner geschlagen')
        elif any(bitboards[p] & (1 << ziel_position) for p in ['rb', 'bb'] if moving_piece == 'r') or any(bitboards[p] & (1 << ziel_position) for p in ['rr', 'br'] if moving_piece == 'b'):
            for p in bitboards:
                if bitboards[p] & (1 << ziel_position):
                    bitboards[p] &= ~(1 << ziel_position)
            new_piece = 'rr' if moving_piece == 'r' else 'bb'
            bitboards[new_piece] |= (1 << ziel_position)
            #print('Turm geschlagen')
        elif any(bitboards[p] & (1 << ziel_position) for p in ['r'] if moving_piece == 'r') or any(bitboards[p] & (1 << ziel_position) for p in ['b'] if moving_piece == 'b'):
            new_piece = 'rr' if moving_piece == 'r' else 'bb'
            bitboards[new_piece] |= (1 << ziel_position)
            bitboards[moving_piece] &= ~(1 << ziel_position)
            #print('Turm gebaut')
    elif moving_piece in ['rr', 'rb', 'br', 'bb']:
        top_piece = moving_piece[1]
        remaining_piece = moving_piece[0]
        if not any(bitboards[p] & (1 << ziel_position) for p in bitboards):
            bitboards[top_piece] |= (1 << ziel_position)
            bitboards[remaining_piece] |= (1 << start_position)
            #print('Turm: Auf leeres Feld gegangen')
        elif any(bitboards[p] & (1 << ziel_position) for p in ['b', 'bb', 'rb'] if top_piece == 'r') or any(bitboards[p] & (1 << ziel_position) for p in ['r', 'rr', 'br'] if top_piece == 'b'):
            for p in bitboards:
                if bitboards[p] & (1 << ziel_position):
                    bitboards[p] &= ~(1 << ziel_position)
            bitboards[top_piece] |= (1 << ziel_position)
            bitboards[remaining_piece] |= (1 << start_position)
            #print('Turm: Gegner geschlagen')
        elif any(bitboards[p] & (1 << ziel_position) for p in ['rb', 'bb'] if top_piece == 'r') or any(bitboards[p] & (1 << ziel_position) for p in ['rr', 'br'] if top_piece == 'b'):
            for p in bitboards:
                if bitboards[p] & (1 << ziel_position):
                    bitboards[p] &= ~(1 << ziel_position)
            new_piece = remaining_piece + top_piece
            bitboards[new_piece] |= (1 << ziel_position)
            bitboards[remaining_piece] |= (1 << start_position)
            #print('Turm: Gegnerischen Turm geschlagen')
        elif any(bitboards[p] & (1 << ziel_position) for p in ['r'] if top_piece == 'r') or any(bitboards[p] & (1 << ziel_position) for p in ['b'] if top_piece == 'b'):
            new_piece = remaining_piece + top_piece
            bitboards[new_piece] |= (1 << ziel_position)
            bitboards[remaining_piece] |= (1 << start_position)
            #print('Turm: Eigenen Turm gebaut')

    return bitboards



def generate_moves(bitboards, color):
    moves = []
    piece_positions = {'r': [], 'rr': [], 'rb': [], 'b': [], 'bb': [], 'br': []}

    # Gather all piece positions
    def gather_positions(piece):
        piece_bitboard = bitboards[piece]
        positions = []
        while piece_bitboard:
            piece_position = (piece_bitboard & -piece_bitboard).bit_length() - 1
            row, col = divmod(63 - piece_position, 8)
            positions.append((row, col))
            piece_bitboard &= piece_bitboard - 1  # Reset the found bit
        return positions

    if color == 'red':
        piece_positions['r'] = gather_positions('r')
        piece_positions['rr'] = gather_positions('rr')
        piece_positions['br'] = gather_positions('br')
    elif color == 'blue':
        piece_positions['b'] = gather_positions('b')
        piece_positions['bb'] = gather_positions('bb')
        piece_positions['rb'] = gather_positions('rb')
    else:
        return moves

    # Generate moves based on gathered positions
    def generate_moves_for_positions(positions, generate_move_func, piece):
        for position in positions:
            row, col = position
            moves.extend(generate_move_func(row, col, piece, bitboards))

    if color == 'red':
        generate_moves_for_positions(piece_positions['r'], generate_single_moves, 'r')
        generate_moves_for_positions(piece_positions['rr'], generate_multi_moves, 'rr')
        generate_moves_for_positions(piece_positions['br'], generate_multi_moves, 'br')
    elif color == 'blue':
        generate_moves_for_positions(piece_positions['b'], generate_single_moves, 'b')
        generate_moves_for_positions(piece_positions['bb'], generate_multi_moves, 'bb')
        generate_moves_for_positions(piece_positions['rb'], generate_multi_moves, 'rb')

    #print(f"Generated moves for {color}: {moves}")
    translated_moves = [translate_move(move) for move in moves]
    return translated_moves

def generate_single_moves(row, col, piece, bitboards):
    moves = []
    directions = []
    diagonal_directions = []
    not_allowed = [(7, 0), (7, 7), (0, 7), (0, 0)]
    
    if piece == 'r':
        directions = [(1, 0), (0, 1), (0, -1)]
        opponent_pieces = ['b', 'bb', 'rb']
        diagonal_directions = [(1, 1), (1, -1)]
    elif piece == 'b':
        directions = [(-1, 0), (0, 1), (0, -1)]
        opponent_pieces = ['r', 'rr', 'br']
        diagonal_directions = [(-1, 1), (-1, -1)]
    
    # Regular moves
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8 and (new_row, new_col) not in not_allowed:
            new_position = 63 - (new_row * 8 + new_col)
            if not any(bitboards[p] & (1 << new_position) for p in bitboards):
                moves.append(((row, col), (new_row, new_col)))
    
    # Diagonal attacks
    for dr, dc in diagonal_directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8 and (new_row, new_col) not in not_allowed:
            new_position = 63 - (new_row * 8 + new_col)
            for opponent in opponent_pieces:
                if bitboards[opponent] & (1 << new_position):
                    if piece == 'r':
                        if opponent == 'b':
                            moves.append(((row, col), (new_row, new_col), 'r'))  
                        elif opponent == 'bb':
                            moves.append(((row, col), (new_row, new_col), 'br'))  
                        elif opponent == 'rb':
                            moves.append(((row, col), (new_row, new_col), 'rr')) 
                    elif piece == 'b':
                        if opponent == 'r':
                            moves.append(((row, col), (new_row, new_col), 'b')) 
                        elif opponent == 'rr':
                            moves.append(((row, col), (new_row, new_col), 'rb'))  
                        elif opponent == 'br':
                            moves.append(((row, col), (new_row, new_col), 'bb'))  
                    break

    # Check for tower building with adjacent pieces of the same color
    if piece == 'r':
        adjacent_positions = [(row + 1, col), (row, col + 1), (row, col - 1)]
    elif piece == 'b':
        adjacent_positions = [(row - 1, col), (row, col + 1), (row, col - 1)]

    for adj_row, adj_col in adjacent_positions:
        if 0 <= adj_row < 8 and 0 <= adj_col < 8:
            new_position = 63 - (adj_row * 8 + adj_col)
            if bitboards[piece] & (1 << new_position):
                if piece == 'r':
                    moves.append(((row, col), (adj_row, adj_col), 'rr'))
                elif piece == 'b':
                    moves.append(((row, col), (adj_row, adj_col), 'bb'))

    #print(f"Generated single moves for {piece} at ({row}, {col}): {moves}")
    return moves

def generate_multi_moves(row, col, piece, bitboards):
    moves = []
    directions = []
    not_allowed = [(7, 0), (7, 7), (0, 7), (0, 0)]
    
    if piece in ['rr', 'br']:
        directions = [(1, -2), (2, -1), (2, 1), (1, 2)]
        opponent_pieces = ['b', 'bb', 'rb', 'r']
    elif piece in ['bb', 'rb']:
        directions = [(-1, -2), (-2, -1), (-2, 1), (-1, 2)]
        opponent_pieces = ['r', 'rr', 'br', 'b']
    
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8 and (new_row, new_col) not in not_allowed:
            new_position = 63 - (new_row * 8 + new_col)
            if not any(bitboards[p] & (1 << new_position) for p in bitboards):
                moves.append(((row, col), (new_row, new_col)))
            else:
                for opponent in opponent_pieces:
                    if bitboards[opponent] & (1 << new_position):
                        if piece == 'rr' or piece == 'br':
                            if opponent == 'b':
                                moves.append(((row, col), (new_row, new_col), 'r'))  
                            elif opponent == 'bb':
                                moves.append(((row, col), (new_row, new_col), 'br'))  
                            elif opponent == 'rb':
                                moves.append(((row, col), (new_row, new_col), 'rr'))  
                            elif opponent == 'r':
                                moves.append(((row, col), (new_row, new_col), 'rr')) 
                        elif piece == 'bb' or piece == 'rb':
                            if opponent == 'r':
                                moves.append(((row, col), (new_row, new_col), 'b'))  
                            elif opponent == 'rr':
                                moves.append(((row, col), (new_row, new_col), 'rb'))  
                            elif opponent == 'br':
                                moves.append(((row, col), (new_row, new_col), 'bb'))  
                            elif opponent == 'b':
                                moves.append(((row, col), (new_row, new_col), 'bb'))
                        break

    #print(f"Generated multi moves for {piece} at ({row}, {col}): {moves}")
    return moves


def translate_move(move):
    row_map = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}
    col_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}
    
    start, end = move[:2]
    start_row, start_col = start
    end_row, end_col = end
    
    start_position = (col_map[start_col], int(row_map[start_row]))
    end_position = (col_map[end_col], int(row_map[end_row]))
    return (start_position, end_position)



def convert_fen_to_bitboard(fen_string):
    parts = fen_string.split()
    fen_rows = parts[0].split('/')
    bitboards = {
        'b': 0, 'r': 0, 'bb': 0, 'rr': 0, 'rb': 0, 'br': 0
    }

    # Reverse the order of rows because the bottom row comes first in FEN
    fen_rows.reverse()

    for row_index, row in enumerate(fen_rows):
        square_index = row_index * 8  # Calculate the start position for the current row
        i = 0
        while i < len(row):
            char = row[i]
            if row_index == 0 or row_index == 7:
                if square_index == row_index * 8:  # Left edge (0 or 56)
                        square_index += 1  # Shift everything one position to the right
            if char.isdigit():
                square_index += int(char)
            else:
                
                if square_index < row_index * 8 + 8:
                    if i + 1 < len(row):
                        next_char = row[i + 1]
                        if char == 'b' and next_char == 'b':
                            bitboards['bb'] |= (1 << (63 - square_index))
                            i += 1
                        elif char == 'r' and next_char == 'r':
                            bitboards['rr'] |= (1 << (63 - square_index))
                            i += 1
                        elif char == 'r' and next_char == 'b':
                            bitboards['rb'] |= (1 << (63 - square_index))
                            i += 1
                        elif char == 'b' and next_char == 'r':
                            bitboards['br'] |= (1 << (63 - square_index))
                            i += 1
                        elif char == 'b':
                            bitboards['b'] |= (1 << (63 - square_index))
                        elif char == 'r':
                            bitboards['r'] |= (1 << (63 - square_index))
                    else:
                        if char == 'b':
                            bitboards['b'] |= (1 << (63 - square_index))
                        elif char == 'r':
                            bitboards['r'] |= (1 << (63 - square_index))
                    square_index += 1
            i += 1


    return bitboards



def convert_fen_to_board(fen_string):

    rows = fen_string.split('/')
    board = []

    for row in rows:
        board_row = []
        empty_count = 0
        x = False
        
        for i in range(len(row)):
            char = row[i]
            
            if char.isdigit():
                empty_count = empty_count * 10 + int(char)
            else:
                if empty_count > 0:
                    for _ in range(empty_count):
                        board_row.append("--")
                    empty_count = 0

                if char == 'b' and i + 1 < len(row) and row[i + 1] == '0':
                    board_row.append("B")
                elif char == 'r' and i + 1 < len(row) and row[i + 1] == '0':
                    board_row.append("R")
                elif char == 'b' and i + 2 < len(row) and row[i + 1] == 'b' and (row[i + 2] == 'b' or row[i + 2] == 'r'):
                    if x == False:
                        board_row.append("BB")
                        x = True
                    else:
                        x = False
                elif char == 'r' and i + 2 < len(row) and row[i + 1] == 'r' and (row[i + 2] == 'r' or row[i + 2] == 'b'):
                    if x == False:
                        board_row.append("RR")
                        x = True 
                    else: 
                        x = False
                elif char == 'b' and i + 1 < len(row) and row[i + 1] == 'b':
                    if x == False : 
                        board_row.append("BB")
                    else : 
                        x = False
                elif char == 'r' and i + 1 < len(row) and row[i + 1] == 'r':
                    if x == False : 
                        board_row.append("RR")
                    else : 
                        x = False
               
                elif char == 'r' and i + 2 < len(row) and row[i + 1] == 'b' and (row[i + 2] == 'r' or row[i + 2] == 'b'):
                    if x == False : 
                        board_row.append("RB")
                        x = True
                    else : 
                        x = False 
             
                elif char == 'b' and i + 2 < len(row) and row[i + 1] == 'r' and (row[i + 2] == 'r' or row[i + 2] == 'b'):
                    if x == False : 
                        board_row.append("BR")
                        x = True
                    else : 
                        x = False 
                elif char == 'r' and i + 1 < len(row) and row[i + 1] == 'b':
                    if x == False : 
                        board_row.append("RB")
                    else : 
                        x = False 
     
                elif char == 'b' and i + 1 < len(row) and row[i + 1] == 'r':
                    if x == False : 
                        board_row.append("BR")
                    else : 
                        x = False
                
        if empty_count > 0:
            for _ in range(empty_count):
                board_row.append("--")
        board.insert(0, board_row)
    

    board2 = replace_sides(board)
    return board2

def replace_sides(board):
    if len(board) > 0 and len(board[0]) > 1:
        board[0][0] = 'XX'
        board[0][-1] = 'XX'
        board[7][0] = 'XX'
        board[7][-1] = 'XX'
    return board


def print_bitboard(bitboard):
    for rank in range(7, -1, -1):
        line = ""
        for file in range(7, -1, -1):
            square = rank * 8 + file
            if square in {0, 7, 56, 63}:
                line += "XX "
            else:
                if (bitboard >> square) & 1:
                    line += " 1 "
                else:
                    line += " 0 "
        print(line)
    print("\n")

def bitboard_to_fen(bitboards):
    piece_map = {
        'r': 'r0',
        'b': 'b0',
        'rr': 'rr',
        'bb': 'bb',
        'rb': 'rb',
        'br': 'br'
    }

    fen_rows = []

    for row_idx in range(8):
        fen_row = ''
        empty_count = 0
        for col_idx in range(8):
            bit_position = (7 - row_idx) * 8 + (7 - col_idx)
            piece_found = False

            for piece, bitboard in bitboards.items():
                if bitboard & (1 << bit_position):
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    fen_row += piece_map[piece]
                    piece_found = True
                    break
            
            if not piece_found:
                empty_count += 1

        if empty_count > 0:
            fen_row += str(empty_count)

        fen_rows.insert(0, fen_row)

    return '/'.join(fen_rows)

