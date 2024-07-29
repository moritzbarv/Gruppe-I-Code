#Print the board format in terminal
def print_board(board):
    board_width = max(len(cell) for row in board for cell in row)
    
    column_letters = " " * (len(str(len(board))) + 1) + " ".join(f'{chr(65 + col):>{board_width}}' for col in range(len(board[0])))
    print(column_letters)
    
    for row_idx, row in enumerate(board):
        row_numbers = f'{8 - row_idx:>{len(str(len(board)))}}'
        print(f'{row_numbers} ' + ' '.join(f'{cell:>{board_width}}' for cell in row))
    print("\n")


#Change format of input
def parse_move(move):
    try:
        start_col = move[0].upper()
        start_row = int(move[1]) 
        end_col = move[2].upper()
        end_row = int(move[3]) 
        return ((start_col, start_row), (end_col, end_row))
    except (ValueError, IndexError):
        raise ValueError("Invalid format. Please enter a move like 'e2e4'.")

#Get color from String
def get_color(board_string):
    if board_string[-1] == 'b':
        return 'blue'
    elif board_string[-1] == 'r':
        return 'red'
    else:
        return None     

#Check if game is over
def game_over(board, color):

    for col in range(1, len(board[0]) -1):
            if board[0][col] == 'B' or board[0][col] == 'RB':
                return True

    for col in range(1, len(board[-1])-1):
            if board[-1][col] == 'R'or board[-1][col] == 'BR' :
                return True

    if not generate_moves(board,color):
        return True

    return False


def generate_column(letter):
    return ord(letter.upper()) - ord('A')

#Change the board after a move is made
def change_board(board, start, ziel): 
    start_spalte, start_zeile = generate_column(start[0]), 8 - int(start[1])
    ziel_spalte, ziel_zeile = generate_column(ziel[0]), 8 - int(ziel[1])

    if 0 <= start_spalte < 8 and 0 <= start_zeile < 8 and 0 <= ziel_spalte < 8 and 0 <= ziel_zeile < 8 and board[start_zeile][start_spalte] != "XX" and board[ziel_zeile][ziel_spalte] != "XX":
       
        figur = board[start_zeile][start_spalte]
        if figur == 'R' : 
            board[start_zeile][start_spalte] = "--" 
            if board[ziel_zeile][ziel_spalte] == "--" : 
                board[ziel_zeile][ziel_spalte] = figur
                #print('Auf leeres Feld gegangen')
            elif board[ziel_zeile][ziel_spalte] == "B" : 
                board[ziel_zeile][ziel_spalte] = figur
                #print('Gegner geschlagen')
            elif board[ziel_zeile][ziel_spalte] == "RB" or board[ziel_zeile][ziel_spalte] == "BB":
                board[ziel_zeile][ziel_spalte] = board[ziel_zeile][ziel_spalte][0] + figur
                #print('Turm geschlagen')  
            elif board[ziel_zeile][ziel_spalte] == "R": 
                board[ziel_zeile][ziel_spalte] = board[ziel_zeile][ziel_spalte] + figur 
                #print("Turm gebaut")
        elif figur == 'B' :  
            board[start_zeile][start_spalte] = "--" 
            if board[ziel_zeile][ziel_spalte] == "--" : 
                board[ziel_zeile][ziel_spalte] = figur
                #print('Auf leeres Feld gegangen')
            elif board[ziel_zeile][ziel_spalte] == "R" : 
                board[ziel_zeile][ziel_spalte] = figur
                #print('Gegner geschlagen')
            elif board[ziel_zeile][ziel_spalte] == "BR" or board[ziel_zeile][ziel_spalte] == "RR":
                board[ziel_zeile][ziel_spalte] =  board[ziel_zeile][ziel_spalte][0] + figur 
                #print('Turm geschlagen')  
            elif board[ziel_zeile][ziel_spalte] == "B": 
                board[ziel_zeile][ziel_spalte] =  board[ziel_zeile][ziel_spalte] + figur 
                #print("Turm gebaut")
        
        elif figur == 'RR' or figur == 'BR':
            board[start_zeile][start_spalte] = figur[0]
            if board[ziel_zeile][ziel_spalte] == "--":
                board[ziel_zeile][ziel_spalte] = figur[1]
                #print('Turm: Auf leeres Feld gegangen')
            elif board[ziel_zeile][ziel_spalte] == "B" : 
                board[ziel_zeile][ziel_spalte] = figur[1]
                #print('Turm: Gegner geschlagen')
            elif board[ziel_zeile][ziel_spalte] == "RB" or board[ziel_zeile][ziel_spalte] == "BB":
                board[ziel_zeile][ziel_spalte] = board[ziel_zeile][ziel_spalte][0] + figur[1]
                #print('Turm: Gegnerischen Turm geschlagen') 
            elif board[ziel_zeile][ziel_spalte] == "R": 
                board[ziel_zeile][ziel_spalte] = board[ziel_zeile][ziel_spalte] + figur[1] 
                #print("Turm: Eigenen Turm gebaut")
        elif figur == 'BB' or figur == 'RB':
            board[start_zeile][start_spalte] = figur[0]
            if board[ziel_zeile][ziel_spalte] == "--":
                board[ziel_zeile][ziel_spalte] = figur[1]
                #print('Turm: Auf leeres Feld gegangen')
            elif board[ziel_zeile][ziel_spalte] == "R" : 
                board[ziel_zeile][ziel_spalte] = figur[1]
                #print('Turm: Gegner geschlagen')
            elif board[ziel_zeile][ziel_spalte] == "BR" or board[ziel_zeile][ziel_spalte] == "RR":
                board[ziel_zeile][ziel_spalte] = board[ziel_zeile][ziel_spalte][0] + figur[1]
                #print('Turm: Gegnerischen Turm geschlagen') 
            elif board[ziel_zeile][ziel_spalte] == "B": 
                board[ziel_zeile][ziel_spalte] = board[ziel_zeile][ziel_spalte] + figur[1] 
                #print("Turm: Eigenen Turm gebaut")
        new_board = []
        for row in board:
            new_board.append(row[:])  
        
        
        return new_board  

#Create board from fen-string
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
                #empty_count = empty_count * 10 + int(char)
                empty_count = int(char)

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
    
    board[0].insert(0, "XX")
    board[0].append("XX")
    board[-1].insert(0, "XX")
    board[-1].append("XX")
    
    return board

#Generate all possible moves
def generate_moves(board, color):
    moves = [] 
    if color == 'red': 
        for row in range(len(board)):
            for col in range(len(board[row])):
                piece = board[row][col]
                if piece == 'R':
                    single_piece_moves = generate_single_moves(row, col, piece, board)
                    moves.extend(single_piece_moves)
                if piece in ['RR', 'BR']: 
                    multi_piece_moves = generate_multi_moves(row, col, piece, board)
                    moves.extend(multi_piece_moves)

    elif color == 'blue': 
        for row in range(len(board)):
            for col in range(len(board[row])):
                piece = board[row][col]
                if piece == 'B':
                    single_piece_moves = generate_single_moves(row, col, piece, board)
                    moves.extend(single_piece_moves)
                if piece in ['BB', 'RB']: 
                    multi_piece_moves = generate_multi_moves(row, col, piece, board)
                    moves.extend(multi_piece_moves)          

    translated_moves = [translate_move(move) for move in moves]    
    return translated_moves

#Moves for single pieces
def generate_single_moves(row, col, piece, board):
    moves = []
    if piece == 'R':
        directions = [(1, 0), (0, 1), (0, -1)]
        for drow, dcol in directions:
            new_row = row + drow
            new_col = col + dcol
            if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]):
                if board[new_row][new_col] == '--' or board[new_row][new_col] == 'R':
                    moves.append(((row, col), (new_row, new_col)))
                if row + 1 < len(board) and col - 1 >= 0 and board[row+1][col-1] in ['B', 'BB', 'RB']: 
                    move = ((row, col), (row + 1, col - 1))
                    if move not in moves:  
                        moves.append(move)

                if row + 1 < len(board) and col + 1 < len(board[0]) and board[row+1][col+1] in ['B', 'BB', 'RB']:
                    move = ((row, col), (row + 1, col + 1))
                    if move not in moves:  
                        moves.append(move)

    elif piece == 'B': 
        directions = [(-1, 0), (0, 1), (0, -1)]
        for drow, dcol in directions:
            new_row = row + drow
            new_col = col + dcol
            if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]):
                if board[new_row][new_col] == '--' or board[new_row][new_col] == 'B':
                    moves.append(((row, col), (new_row, new_col)))
                if row - 1 >= 0 and col + 1 < len(board[0]) and board[row-1][col+1] in ['R', 'RR', 'BR']:
                    move = ((row, col), (row - 1, col + 1))
                    if move not in moves:  
                        moves.append(move)
                if row - 1 >= 0 and col - 1 >= 0 and board[row-1][col-1] in ['R', 'RR', 'BR']:
                    move = ((row, col), (row - 1, col - 1))
                    if move not in moves:  
                        moves.append(move)
    return moves

#Moves for towers
def generate_multi_moves(row, col, piece, board):
    moves = []
    if piece == 'RR' or piece == 'BR':
        directions = [(1, -2), (2, -1), (2, 1), (1, 2)]
        for drow, dcol in directions:
            new_row = row + drow
            new_col = col + dcol
            if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]) and board[new_row][new_col] != 'XX':
                if board[new_row][new_col] not in ['BR', 'RR']:
                    moves.append(((row, col), (new_row, new_col)))

    if piece == 'BB' or piece == 'BR':
        directions = [(-1, -2), (-2, -1), (-2, 1), (-1, 2)]
        for drow, dcol in directions:
            new_row = row + drow
            new_col = col + dcol
            if 0 <= new_row < len(board) and 0 <= new_col < len(board[0]) and board[new_row][new_col] != 'XX':
                if board[new_row][new_col] not in ['BR', 'BB']:
                    moves.append(((row, col), (new_row, new_col)))
    return moves

#Translate move into right format
def translate_move(move):
    row_map = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}
    col_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}
    
    start, end = move
    start_row, start_col = start
    end_row, end_col = end
    
    start_position = (col_map[start_col], int(row_map[start_row]))
    end_position = (col_map[end_col], int(row_map[end_row]))
    return (start_position, end_position)
   







