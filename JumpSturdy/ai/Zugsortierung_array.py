
import random
import sys 
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from board.Array import convert_fen_to_board, generate_moves, change_board
from ai.Bewertungsfunktion_array import evaluate_position


#Zugsortierung
def order_moves(moves, board, color):

    ordered_moves = []

    #Endmoves
    def is_end_move(move, color):
        if color == 'blue':
            return move[1][1] == 8
        if color == 'red':
            return move[1][1] == 1

    end_moves = [move for move in moves if is_end_move(move, color)]
    if end_moves:
        ordered_moves = end_moves
        return ordered_moves
    
    #Anfangsmoves
    if board == convert_fen_to_board('b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 r'):
        tower_moves = []
        remaining_moves = []
        for move in moves:
            if any(move[1] == other_move[0] for other_move in moves if move != other_move):
                tower_moves.append(move)
            else:
                remaining_moves.append(move)

        # Randomly pick 3 tower moves
        three_tower = random.sample(tower_moves, min(5, len(tower_moves)))
        
        # Randomly pick 3 remaining moves
        three_remaining = random.sample(remaining_moves, min(5, len(remaining_moves)))

        ordered_moves = three_tower + three_remaining
        return ordered_moves

    capturing_moves = []
    non_capturing_moves = []

    #Capturing und non-capturing moves 
    for move in moves:
        if is_capturing_move(board, move, color):
            capturing_moves.append(move)
        else:
            non_capturing_moves.append(move)

    #Geordnet nach Nähe zum Ziel
    if color == 'blue':
        capturing_moves.sort(key=lambda move: move[1][1], reverse=True)
        non_capturing_moves.sort(key=lambda move: move[1][1], reverse=True)
    else:
        capturing_moves.sort(key=lambda move: move[1][1])
        non_capturing_moves.sort(key=lambda move: move[1][1])

    #Züge mit höherer Priorität
    if color == 'blue':
        high_priority_captures = [move for move in capturing_moves if move[1][1] in [2, 3, 6, 7]]
        high_priority_non_captures = [move for move in non_capturing_moves if move[1][1] in [6, 7]]

        def high_priority_order(move):
            if move[1][1] == 2:
                return 0
            elif move[1][1] == 7 and move in capturing_moves:
                return 1
            elif move[1][1] == 7 and move in non_capturing_moves:
                return 2
            elif move[1][1] == 3:
                return 3
            elif move[1][1] == 6 and move in capturing_moves:
                return 4
            elif move[1][1] == 6 and move in non_capturing_moves:
                return 5
            return 6
    if color == 'red' : 
        high_priority_captures = [move for move in capturing_moves if move[1][1] in [2, 3, 6, 7]]
        high_priority_non_captures = [move for move in non_capturing_moves if move[1][1] in [2, 3]]

        def high_priority_order(move):
            if move[1][1] == 7:
                return 0
            elif move[1][1] == 2 and move in capturing_moves:
                return 1
            elif move[1][1] == 2 and move in non_capturing_moves:
                return 2
            elif move[1][1] == 6:
                return 3
            elif move[1][1] == 3 and move in capturing_moves:
                return 4
            elif move[1][1] == 3 and move in non_capturing_moves:
                return 5
            return 6   

    high_priority_moves = high_priority_captures + high_priority_non_captures
    high_priority_moves.sort(key=high_priority_order)
    capturing_moves = [move for move in capturing_moves if move not in high_priority_moves]
    non_capturing_moves = [move for move in non_capturing_moves if move not in high_priority_moves]

    # Kombinieren
    ordered_moves = high_priority_moves + capturing_moves + non_capturing_moves

    return ordered_moves


#Alternative
def order_moves2(moves, board, color, maximizingP):
        capturing_moves = []
        non_capturing_moves = []
        
        for move in moves:
            if is_capturing_move(board, move, color):
                capturing_moves.append(move)
            else:
                non_capturing_moves.append(move)
        if color == 'blue':
            capturing_moves.sort(key=lambda move: move[1][1], reverse = True)
            non_capturing_moves.sort(key=lambda move: move[1][1], reverse = True)
        else:
            capturing_moves.sort(key=lambda move: move[1][1])     
            non_capturing_moves.sort(key=lambda move: move[1][1])     
        

        def is_end_move(move, color):
            if color == 'blue' : 
                return move[1][1] == 8
            if color == 'red' : 
                return move[1][1] == 1
        ordered_moves = []
        end_moves = [move for move in moves if not is_end_move(move, color)] 
        if end_moves: 
            ordered_moves = end_moves
            return ordered_moves

        if capturing_moves and non_capturing_moves: 
            first_capture_move = capturing_moves[0]  
            first_non_capture_move = non_capturing_moves[0] 
            capture_board = change_board(board, first_capture_move[0], first_capture_move[1])
            eval_cap = evaluate_position(capture_board, color, maximizingP)
            non_capture_board = change_board(board, first_non_capture_move[0], first_non_capture_move[1])
            eval_nocap = evaluate_position(non_capture_board, color, maximizingP) 
            if eval_cap >= eval_nocap:
                capturing_moves = capturing_moves[1:]
                non_capturing_moves = non_capturing_moves[1:]
                ordered_moves = [first_capture_move] + [first_non_capture_move] + capturing_moves + non_capturing_moves

            else:
                non_capturing_moves = non_capturing_moves[1:]
                ordered_moves = [first_non_capture_move] + capturing_moves + non_capturing_moves
        elif capturing_moves:
            ordered_moves = end_moves + capturing_moves
        elif non_capturing_moves:
            tower_moves = []
            remaining_moves = []
            for move in non_capturing_moves:
                if any(move[1] == other_move[0] for other_move in non_capturing_moves if move != other_move):
                    tower_moves.append(move)
                else:
                    remaining_moves.append(move)
            if tower_moves and remaining_moves: 
                first_tower_move = tower_moves[0]  
                first_remaining_move = remaining_moves[0] 
                tower_board = change_board(board, first_tower_move[0], first_tower_move[1])
                eval_tower = evaluate_position(tower_board, color, maximizingP)
                remaining_board = change_board(board, first_remaining_move[0], first_remaining_move[1])
                eval_notower = evaluate_position(remaining_board, color, maximizingP) 
                if eval_tower >= eval_notower:
                    tower_moves = tower_moves[1:]
                    remaining_moves = remaining_moves[1:]
                    ordered_moves = [first_tower_move] + [first_remaining_move] + tower_moves + remaining_moves
                else:
                    non_capturing_moves = non_capturing_moves[1:]
                    ordered_moves = [first_remaining_move] + tower_moves + remaining_moves

            else: 
                ordered_moves = capturing_moves       
        return ordered_moves  

def is_end_move(move, color):
    if color == 'blue':
        return move[1][1] == 8
    if color == 'red':
        return move[1][1] == 1


def generate_capture_moves(board, color):
    capturing_moves = []
    moves = generate_moves(board, color)
    for move in moves:
        if is_capturing_move(board, move, color):
            capturing_moves.append(move)

    return capturing_moves

def generate_end_moves(board, color):
    end_moves = []
    moves = generate_moves(board, color)
    for move in moves:
        if is_end_move(move, color):
            end_moves.append(move)

    return end_moves

def is_capturing_move(board, move, color):
    row_map_back = {'8':0, '7': 1,'6':2, '5':3 , '4':4, '3':5, '2':6, '1':7}
    col_map_back = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
    #row_map = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}
    #col_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H'}

    start, end = move

    start_col, start_row = start
    end_col, end_row = end

    if color == 'red' and board[row_map_back[str(end_row)]][col_map_back[end_col]] != '--' and board[row_map_back[str(end_row)]][col_map_back[end_col]] != 'R' : 
     #   print('True')
        return True 

    if color == 'blue' and board[row_map_back[str(end_row)]][col_map_back[end_col]] != '--' and board[row_map_back[str(end_row)]][col_map_back[end_col]] != 'B' : 
      #  print('True')
        return True
    
    else : 
       # print('False')
        return False