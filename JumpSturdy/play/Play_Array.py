import sys 
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from board.Array import convert_fen_to_board, get_color, print_board, game_over, generate_moves, change_board, parse_move
from ai.Minimax_array import minimax, minimax_zugsortierung, minimax_pvs, minimax_pvs_ruhesuche

def start_game(board_string): 

    the_board = convert_fen_to_board(board_string)
    our_color = get_color(board_string)
    print_board(the_board)
    #play(the_board, our_color)
    play_interaktiv(the_board, our_color)

#Let the AI play against eachother    
def play(board, color):    
    if game_over(board, color):
        return print('Game over: ' + color + ' lost')

    x = minimax_zugsortierung(board, '', 3, float('-inf'), float('inf'), True, color, 200, 0, 0)
    #x = minimax_pvs_ruhesuche(board, '', 3, float('-inf'), float('inf'), True, color, 200, 0, 0)

    ai_move = x[1]
    if ai_move is None:
        return print('Game over: ' + color + ' lost')
    
    new_board = change_board(board, ai_move[0], ai_move[1])
    print('New turn : ' + color )
    print('Move :')
    print(ai_move)
    print('New board: ')
    print_board(new_board)
    new_color = 'blue' if color == 'red' else 'red'
        
    return play(new_board,new_color)

#Play against the AI
def play_interaktiv(board, ai_color):
    human_color = 'red' if ai_color == 'blue' else 'blue'
    
    while not game_over(board, ai_color):
        print("AI is thinking...")
        print("AI color:", ai_color)
        x = minimax_zugsortierung(board, '', 3, float('-inf'), float('inf'), True, ai_color, 200, 0, 0) 
        #x = minimax_pvs_ruhesuche(board, '', 3, float('-inf'), float('inf'), True, color, 200, 0, 0)

        ai_move = x[1]
        if ai_move is None:
            return print('Game over: ' + ai_color + ' lost')

        board = change_board(board, ai_move[0], ai_move[1])    
        print_board(board)
        print(ai_move)
        if game_over(board, human_color):
            print("Game over! AI wins!")
            break

        print("Your turn:")

        while True:
            try:
                print("Human color:", human_color)
                move = input("Enter your move (e.g., e2e4): ")
                new_move = parse_move(move)
                if new_move not in generate_moves(board, human_color):
                    print("Try again!")
                else: 
                    new_board = change_board(board,new_move[0], new_move[1])
                    print_board(new_board)
                    break
            except ValueError as e:
                print(e)
                print("Invalid move. Please try again.")
        
        if game_over(board, ai_color):
            print("Game over! You win!")
            break


start_game('b0b0b0b0b0b0/1b0b0b0b0b0b01/8/8/8/8/1r0r0r0r0r0r01/r0r0r0r0r0r0 r')
#RUN
