import copy 
import time 


import sys 
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from board.Bitboard import game_over, generate_moves, change_board, print_bitboard
from ai.Bewertungsfunktion_bitboard import evaluate_position
from ai.Zugsortierung_bitboard import generate_capture_moves, generate_end_moves, order_moves, order_moves2


#Minimax with alphabeta

def minimax(board, move, depth, alpha, beta, maximizingP, color):
    #print('check if game is over')
    if game_over(board, color) :
        if maximizingP == False : 
            #print('game over detected, you won')
            #print_board(board)
            print(+500)
            return (+500, None)
        if maximizingP == True : 
            #print('game over detected, you lost')
            #print_board(board)
            print(-500) 
            return (-500, None)
    elif depth == 0: 
        #print('depth is 0')
        #print('evaluate the position')
        #print_board(board)
        eval_val = evaluate_position(board, color, maximizingP)
        print(eval_val , move)
        return (eval_val , move)
    #print('game not over and depth is : ' , depth)
    if maximizingP: 
        #print('max player')
        maxEvaluation = float("-inf")
        best_move = None
        for child_move in generate_moves(board, color):
            child_board = copy.deepcopy(board)
            child_board = change_board(child_board, child_move[0], child_move[1])
            print(child_move)
            #print_board(child_board)
            evaluation = minimax(child_board, child_move, depth - 1, alpha, beta, False, color)
            if evaluation[0] > maxEvaluation:
                maxEvaluation = evaluation[0]
                best_move = child_move
            alpha = max(alpha, evaluation[0])
            print(alpha)
            if beta <= alpha:
                print("Alpha-beta pruning (maximizing): alpha >= beta")
                break

        print(f"Maximizing player: returning {maxEvaluation}") 
        print(best_move)
        return (maxEvaluation , best_move)

    else: 
        #print('min Player')
        minEvaluation = float("inf")
        best_move = None
        opponent_color = 'red' if color == 'blue' else 'blue'
        for child_move in generate_moves(board, opponent_color):
            child_board = copy.deepcopy(board)
            child_board = change_board(child_board, child_move[0],child_move[1])
            #print_board(child_board)
            print(child_move)
            evaluation = minimax(child_board, child_move, depth - 1, alpha, beta, True, color)
            if evaluation[0] < minEvaluation:
                minEvaluation = evaluation[0]
                best_move = child_move
            beta = min(beta, evaluation[0])
            print(beta)
            if beta <= alpha:
                print("Alpha-beta pruning (minimizing): beta <= alpha")
                break
        #print(best_move)        
        print(f"Minimizing player: returning {minEvaluation}")
        return (minEvaluation, best_move)

#Minimax ohne alphabeta

def minimax2(board, move, depth, maximizingP, color):
    
    #print('check if game not over')
    #print(color)
    if game_over(board, color) :
        
        if maximizingP == True:
            #print('game over detected')
            print(board)
            print(-500)
            return (-500, None)
        if maximizingP == False:
            #print('game over detected')
            print(board)
            print(+500)
            return (+500, None)
    
    elif depth == 0: 
        eval_val = evaluate_position(board, color, maximizingP)
       
        #print('depth is 0')
        print(eval_val , move)
        return (eval_val , move)
    #print('game not over and depth not 0')
    
    if maximizingP: 
        #print('max player')
        maxEvaluation = float("-inf")
        best_move = None
        for child_move in generate_moves(board, color):
            child_board = copy.deepcopy(board)
            child_board = change_board(child_board, child_move[0], child_move[1])
            #print_board(child_board)
            print(child_move)
            evaluation = minimax2(child_board, child_move, depth - 1, False, color)
            if evaluation[0] > maxEvaluation:
                maxEvaluation = evaluation[0]
                best_move = child_move
        print(best_move)
        print(f"Maximizing player: returning {maxEvaluation}") 
        return (maxEvaluation , best_move)




    else: 
        minEvaluation = float("inf")
        best_move = None
        opponent_color = 'red' if color == 'blue' else 'blue'
        for child_move in generate_moves(board, opponent_color):
                child_board = copy.deepcopy(board)
                child_board = change_board(child_board, child_move[0], child_move[1])
                #print_board(child_board)
                #print(child_move)
                evaluation = minimax2(child_board, child_move, depth - 1, True, color)
                if evaluation[0] < minEvaluation:
                    minEvaluation = evaluation[0]
                    best_move = child_move
        print(best_move)        
        print(f"Minimizing player: returning {minEvaluation}")
        return (minEvaluation, best_move)



#Minimax ohne alphabta + states checked

def minimax3(board, move, depth, maximizingP, color, states_checked=0):
    # Die restliche Funktion bleibt unverändert, füge einfach die Variable states_checked hinzu
    #print('check if game not over')
    #print(color)
    states_checked += 1  # Zähle den aktuellen Zustand hinzu
    print(states_checked)
    if game_over(board, color) :
        if maximizingP == True:
            #print('game over detected')
            print(board)
            print(-500, states_checked)
            return (-500, None, states_checked)
        if maximizingP == False:
            #print('game over detected')
            print(board)
            print(+500, states_checked)
            return (+500, None, states_checked)

    elif depth == 0:
        eval_val = evaluate_position(board, color, maximizingP)
        #print('depth is 0')
        print(eval_val, move, states_checked)
        return (eval_val, move, states_checked)
    #print('game not over and depth not 0')

    if maximizingP:
        #print('max player')
        maxEvaluation = float("-inf")
        best_move = None
        for child_move in generate_moves(board, color):
            child_board = copy.deepcopy(board)
            child_board = change_board(child_board, child_move[0], child_move[1])
            #print_board(child_board)
            print(child_move)
            evaluation, _, states_checked = minimax3(child_board, child_move, depth - 1, False, color, states_checked)
            if evaluation > maxEvaluation:
                maxEvaluation = evaluation
                best_move = child_move
        #print(best_move)
        print(f"Maximizing player: returning {maxEvaluation}" , states_checked , best_move)
        return (maxEvaluation, best_move, states_checked)

    else:
        minEvaluation = float("inf")
        best_move = None
        opponent_color = 'red' if color == 'blue' else 'blue'
        for child_move in generate_moves(board, opponent_color):
            child_board = copy.deepcopy(board)
            child_board = change_board(child_board, child_move[0], child_move[1])
            #print_board(child_board)
            print(child_move)
            evaluation, _, states_checked = minimax3(child_board, child_move, depth - 1, True, color, states_checked)
            if evaluation < minEvaluation:
                minEvaluation = evaluation
                best_move = child_move
        print(best_move)
        print(f"Minimizing player: returning {minEvaluation}" , states_checked, best_move)
        return (minEvaluation, best_move, states_checked)
    
#Minimax mit alphabeta + states checked

def minimax4(board, move, depth, alpha, beta, maximizingP, color, states_checked=0):
    #print('check if game is over')
    states_checked += 1  # Zähle den aktuellen Zustand hinzu
    print(states_checked)
    if game_over(board, color) :
        if maximizingP == False : 
            #print('game over detected, you won')
            #print_board(board)
            #print(+500)
            return (+500, None, states_checked)
        if maximizingP == True : 
            #print('game over detected, you lost')
            #print_board(board)
            #print(-500) 
            return (-500, None, states_checked)
    elif depth == 0: 
        #print('depth is 0')
        #print('evaluate the position')
       # print_board(board)
        eval_val = evaluate_position(board, color, maximizingP)
        print(eval_val , move)
        return (eval_val , move, states_checked)
    #print('game not over and depth is : ' , depth)
    if maximizingP: 
        #print('max player')
        maxEvaluation = float("-inf")
        best_move = None
        for child_move in generate_moves(board, color):
            child_board = copy.deepcopy(board)
            child_board = change_board(child_board, child_move[0], child_move[1])
            #print(child_move)
            #print_board(child_board)
            evaluation, _, states_checked = minimax4(child_board, child_move, depth - 1, alpha, beta, False, color, states_checked)
            if evaluation > maxEvaluation:
                maxEvaluation = evaluation
                best_move = child_move
            alpha = max(alpha, evaluation)
           # print(alpha)
            if beta <= alpha:
                #print("Alpha-beta pruning (maximizing): alpha >= beta")
                break

        print(f"Maximizing player: returning {maxEvaluation}" , states_checked, best_move) 
        #print(best_move)
        return (maxEvaluation , best_move, states_checked)

    else: 
        #print('min Player')
        minEvaluation = float("inf")
        best_move = None
        opponent_color = 'red' if color == 'blue' else 'blue'
        for child_move in generate_moves(board, opponent_color):
            child_board = copy.deepcopy(board)
            child_board = change_board(child_board, child_move[0],child_move[1])
            #print_board(child_board)
            #print(child_move)
            evaluation, _, states_checked = minimax4(child_board, child_move, depth - 1, alpha, beta, True, color, states_checked)
            if evaluation < minEvaluation:
                minEvaluation = evaluation
                best_move = child_move
            beta = min(beta, evaluation)
            #print(beta)
            if beta <= alpha:
            #    print("Alpha-beta pruning (minimizing): beta <= alpha")
                break
        #print(best_move)        
        #print(f"Minimizing player: returning {minEvaluation}" , states_checked)
        return (minEvaluation, best_move, states_checked)

#Minimax + AlphaBeta + Zugsortierung + Dynamisches Zeitmanagement

def minimax_zugsortierung(board, move, depth, alpha, beta, maximizingP, color , total_time, states_checked, zuege):

    start_time = time.time()
    
    states_checked += 1
    #print('Board : ')
    #print_board(board)
    #print('States checked: ', states_checked)
    #print('Alpha current: ' , alpha)
    #print('Beta current: ' , beta)

    if game_over(board, color) :
        if maximizingP == False : 
            #print('game over detected, you won')
            #print_board(board)
            #print(+500)
            return (+500, None , states_checked)
        if maximizingP == True : 
            #print('game over detected, you lost')
            #print_board(board)
            #print(-500) 
            return (-500, None, states_checked)
    elif depth == 0: 
        #print('depth is 0')
        #print('evaluate the position' , move)
        eval_val = eval_val = evaluate_position(board, color, maximizingP)
        #print('Evaluation: ' , eval_val )
        return (eval_val , move, states_checked)
    #print('game not over and depth is : ' , depth)
    if maximizingP: 
        #print('max player')
        maxEvaluation = float("-inf")
        best_move = None
        moves = generate_moves(board, color)
        #print(moves)
        ordered_moves = order_moves(moves, board, color)
        #print(ordered_moves)
        for child_move in ordered_moves:
            child_board = copy.deepcopy(board)
            child_board = change_board(child_board, child_move[0], child_move[1])
            #print(child_move)

            evaluation, _, states_checked = minimax_zugsortierung(child_board, child_move, depth - 1, alpha, beta, False, color, total_time, states_checked, zuege)
            if evaluation > maxEvaluation:
                #print(best_move)
                
                maxEvaluation = evaluation
                best_move = child_move
            alpha = max(alpha, evaluation)
            #print(alpha)
            if beta <= alpha:
                #print("Alpha-beta pruning (maximizing): alpha >= beta")
                break
            elapsed_time = time.time() - start_time
            
			
            if zuege <= 1 and elapsed_time >= 2:
                #print('time over')
                break
            if zuege <= 3 and elapsed_time >= total_time / 10:
                #print('time over')
                break
            if zuege <= 5 and elapsed_time >= total_time / 8:
                #print('time over')
                break
            if zuege <= 8 and elapsed_time >= total_time / 6:
                #print('time over')
                break 
            if zuege <= 12 and elapsed_time >= total_time / 4:
                #print('time over')
                break 
            if 14 < zuege  and elapsed_time >= total_time / 2:
                #print('time over')
                break         

        #print(total_time)
        #x = time.time()
        #print(x)
        print(f"Maximizing player: returning {maxEvaluation}" , states_checked, best_move) 
    	#print('Best move : ' , best_move)
        #print('States checked : ' , states_checked)
        return (maxEvaluation , best_move, states_checked)

    else: 
        #print('min Player')
        minEvaluation = float("inf")
        best_move = None
        opponent_color = 'red' if color == 'blue' else 'blue'
        moves = generate_moves(board, opponent_color)
        ordered_moves = order_moves(moves, board, opponent_color)
        #print(moves)
        #print(ordered_moves)
        for child_move in ordered_moves:
            child_board = copy.deepcopy(board)
            child_board = change_board(child_board, child_move[0],child_move[1])

            #print(child_move)
            evaluation, _, states_checked = minimax_zugsortierung(child_board, child_move, depth - 1, alpha, beta, True, color, total_time, states_checked, zuege)
            if evaluation < minEvaluation:
                minEvaluation = evaluation
                best_move = child_move
            beta = min(beta, evaluation)
            #print(beta)
            if beta <= alpha:
                #print("Alpha-beta pruning (minimizing): beta <= alpha")
                break
        #print('Best move : ' , best_move)
        print('States checked : ' , states_checked)
        
        print(f"Minimizing player: returning {minEvaluation}")

        return (minEvaluation, best_move, states_checked)

# Dazu Principal Variation Search

def minimax_pvs(board, move, depth, alpha, beta, maximizingP, color, total_time, states_checked, zuege):

    start_time = time.time()
    
    states_checked += 1
    #print('Board : ')
    #print_board(board)
    #print('States checked: ', states_checked)
    #print('Alpha current: ' , alpha)
    #print('Beta current: ' , beta)
    
    if game_over(board, color):
        if not maximizingP:
            #print('game over detected, you won')
            return (+500, None, states_checked)
        else:
            #print('game over detected, you lost')
            return (-500, None, states_checked)
    elif depth == 0:
        #print('depth is 0')
        #print('evaluate the position', move)
        eval_val = evaluate_position(board, color, maximizingP)
        #print('Evaluation: ', eval_val)
        return (eval_val, move, states_checked)
    
    #print('game not over and depth is: ', depth)
    best_move = None
    if maximizingP:
        #print('max player')
        maxEvaluation = float("-inf")
        moves = generate_moves(board, color)
        ordered_moves = order_moves(moves, board, color)
        #print(ordered_moves)

        for i, child_move in enumerate(ordered_moves):
            child_board = copy.deepcopy(board)
            child_board = change_board(child_board, child_move[0], child_move[1])
            #print(child_move)
            if i == 0:  # Principal variation node
                evaluation, _, states_checked = minimax_pvs(child_board, child_move, depth - 1, alpha, beta, False, color, total_time, states_checked, zuege)
            else:  # Scout search
                evaluation, _, states_checked = minimax_pvs(child_board, child_move, depth - 1, alpha, alpha + 1, False, color, total_time, states_checked, zuege)
                if alpha < evaluation < beta:
                    evaluation, _, states_checked = minimax_pvs(child_board, child_move, depth - 1, alpha, beta, False, color, total_time, states_checked, zuege)
            
            if evaluation > maxEvaluation:
                maxEvaluation = evaluation
                best_move = child_move
            alpha = max(alpha, evaluation)
            #print(alpha)
            if beta <= alpha:
            #    print("Alpha-beta pruning (maximizing): alpha >= beta")
                break
            elapsed_time = time.time() - start_time
            
			
            if zuege <= 1 and elapsed_time >= 2:
                #print('time over')
                break
            if zuege <= 3 and elapsed_time >= total_time / 10:
                #print('time over')
                break
            if zuege <= 5 and elapsed_time >= total_time / 8:
                #print('time over')
                break
            if zuege <= 8 and elapsed_time >= total_time / 6:
                #print('time over')
                break 
            if zuege <= 12 and elapsed_time >= total_time / 4:
                #print('time over')
                break 
            if 14 < zuege  and elapsed_time >= total_time / 2:
                #print('time over')
                break  

        print(f"Maximizing player: returning {maxEvaluation}" , best_move , states_checked) 
        #print('Best move: ', best_move , states_checked)
        #print('States checked: ', states_checked)
        return (maxEvaluation, best_move, states_checked)

    else:
        #print('min Player')
        minEvaluation = float("inf")
        opponent_color = 'red' if color == 'blue' else 'blue'
        moves = generate_moves(board, opponent_color)
        ordered_moves = order_moves(moves, board, opponent_color)
        #print(ordered_moves)

        for i, child_move in enumerate(ordered_moves):
            child_board = copy.deepcopy(board)
            child_board = change_board(child_board, child_move[0], child_move[1])
         #   print(child_move)
            if i == 0:  # Principal variation node
                evaluation, _, states_checked = minimax_pvs(child_board, child_move, depth - 1, alpha, beta, True, color, total_time, states_checked, zuege)
            else:  # Scout search
                evaluation, _, states_checked = minimax_pvs(child_board, child_move, depth - 1, beta - 1, beta, True, color, total_time, states_checked, zuege)
                if alpha < evaluation < beta:
                    evaluation, _, states_checked = minimax_pvs(child_board, child_move, depth - 1, alpha, beta, True, color, total_time, states_checked, zuege)
            
            if evaluation < minEvaluation:
                minEvaluation = evaluation
                best_move = child_move
            beta = min(beta, evaluation)
          #  print(beta)
            if beta <= alpha:
           #     print("Alpha-beta pruning (minimizing): beta <= alpha")
                break

        #print('Best move: ', best_move)
        #print('States checked: ', states_checked)
        #print(f"Minimizing player: returning {minEvaluation}")
        return (minEvaluation, best_move, states_checked)


#Ruhesuche : Weiter suchen (Capturing oder endmoves)

def ruhesuche(board, alpha, beta, color, maximizingP, states_checked, dep):
    #print('ruhesuche')
    #print_board(board)
    #states_checked += 1
    current_eval = evaluate_position(board, color, maximizingP)
    #print('This is the current evaluation ' , current_eval)
    if dep == 3 : 
        return(current_eval, states_checked)
    if maximizingP:
        #print('its max player')
        capture_moves = generate_capture_moves(board, color)
        end_moves = generate_end_moves(board, color)
        #print(end_moves)

        moves = end_moves + capture_moves
        #print('ruhesuche moves', moves)

        if current_eval >= beta:
            return current_eval, states_checked
            #print('new : ' , stand_pat, states_checked)
        if alpha < current_eval:
            alpha = current_eval
        for move in moves:
            #print(move)
            child_board = copy.deepcopy(board)
            child_board = change_board(child_board, move[0], move[1])
            #print_board(child_board)

            score, states_checked = ruhesuche(child_board, alpha, beta, color, False, states_checked, dep+1)
            if score >= beta:
                return beta, states_checked
            if score > alpha:
                alpha = score
        return alpha, states_checked
    else:
        #print('its min player')
        if current_eval <= alpha:
            return current_eval, states_checked
            #print('new : ' , stand_pat, states_checked)
        if beta > current_eval:
            beta = current_eval

        opponent_color = 'red' if color == 'blue' else 'blue'
        capture_moves = generate_capture_moves(board, opponent_color)
        end_moves = generate_end_moves(board, opponent_color)
        
        moves = end_moves + capture_moves
        #print('ruhesuche moves', moves)

        for move in moves:
            #print(move)
            child_board = copy.deepcopy(board)
            child_board = change_board(child_board, move[0], move[1])
            #print_board(child_board)
            score, states_checked = ruhesuche(child_board, alpha, beta, color, True, states_checked, dep+1)
            if score <= alpha:
                return alpha, states_checked
            if score < beta:
                beta = score
        return beta, states_checked


#Dazu : Ruhesuche

def minimax_pvs_ruhesuche(board, move, depth, alpha, beta, maximizingP, color, total_time, states_checked, zuege):

    start_time = time.time()
    states_checked += 1
    #print('Board : ')
    #print_board(board)
    #print('States checked: ', states_checked)
    #print('Alpha current: ' , alpha)
    #print('Beta current: ' , beta)
    
    if game_over(board, color):
        if not maximizingP:
            #print('game over detected, you won')
            return (+500, None, states_checked)
        else:
            #print('game over detected, you lost')
            return (-500, None, states_checked)
    elif depth == 0:
        #print('depth is 0')
        #print('evaluate the position')
        #print_board(board)
        eval_val, states_checked = ruhesuche(board, alpha, beta, color, maximizingP, states_checked, dep = 0)
        #eval_val = evaluate_position(board, color, maximizingP)
        #print('Move ' , move)
        #print('Evaluation: ', eval_val)
        return (eval_val, move, states_checked)
    
    #print('game not over and depth is: ', depth)
    best_move = None
    if maximizingP:
        #print('max player')
        maxEvaluation = float("-inf")
        moves = generate_moves(board, color)
        ordered_moves = order_moves(moves, board, color)
        #print(ordered_moves)

        for i, child_move in enumerate(ordered_moves):
            child_board = copy.deepcopy(board)
            child_board = change_board(child_board, child_move[0], child_move[1])
            #print(child_move)
            if i == 0:  # Principal variation node
                evaluation, _, states_checked = minimax_pvs_ruhesuche(child_board, child_move, depth - 1, alpha, beta, False, color, total_time, states_checked, zuege)
            else:  # Scout search
                evaluation, _, states_checked = minimax_pvs_ruhesuche(child_board, child_move, depth - 1, alpha, alpha + 1, False, color, total_time, states_checked, zuege)
                if alpha < evaluation < beta:
                    evaluation, _, states_checked = minimax_pvs_ruhesuche(child_board, child_move, depth - 1, alpha, beta, False, color, total_time, states_checked, zuege)
            
            if evaluation > maxEvaluation:
                maxEvaluation = evaluation
                best_move = child_move
            alpha = max(alpha, evaluation)
            #print(alpha)
            if beta <= alpha:
                #print("Alpha-beta pruning (maximizing): alpha >= beta")
                break
            elapsed_time = time.time() - start_time
            
			
            if zuege <= 1 and elapsed_time >= 2:
                #print('time over')
                break
            if zuege <= 3 and elapsed_time >= total_time / 10:
                #print('time over')
                break
            if zuege <= 5 and elapsed_time >= total_time / 8:
                #print('time over')
                break
            if zuege <= 8 and elapsed_time >= total_time / 6:
                #print('time over')
                break 
            if zuege <= 12 and elapsed_time >= total_time / 4:
                #print('time over')
                break 
            if 14 < zuege  and elapsed_time >= total_time / 2:
                #print('time over')
                break  

        print(f"Maximizing player: returning {maxEvaluation}" , best_move , states_checked) 
        #print('Best move: ', best_move)
        #print('States checked: ', states_checked)
        return (maxEvaluation, best_move, states_checked)

    else:
        #print('min Player')
        minEvaluation = float("inf")
        opponent_color = 'red' if color == 'blue' else 'blue'
        moves = generate_moves(board, opponent_color)
        ordered_moves = order_moves(moves, board, opponent_color)
        #print(ordered_moves)

        for i, child_move in enumerate(ordered_moves):
            child_board = copy.deepcopy(board)
            child_board = change_board(child_board, child_move[0], child_move[1])
            #print(child_move)
            if i == 0:  # Principal variation node
                evaluation, _, states_checked = minimax_pvs_ruhesuche(child_board, child_move, depth - 1, alpha, beta, True, color, total_time, states_checked, zuege)
            else:  # Scout search
                evaluation, _, states_checked = minimax_pvs_ruhesuche(child_board, child_move, depth - 1, beta - 1, beta, True, color, total_time, states_checked, zuege)
                if alpha < evaluation < beta:
                    evaluation, _, states_checked = minimax_pvs_ruhesuche(child_board, child_move, depth - 1, alpha, beta, True, color, total_time, states_checked, zuege)
            
            if evaluation < minEvaluation:
                minEvaluation = evaluation
                best_move = child_move
            beta = min(beta, evaluation)
            #print(beta)
            if beta <= alpha:
                #print("Alpha-beta pruning (minimizing): beta <= alpha")
                break

        #print('Best move: ', best_move)
        #print('States checked: ', states_checked)
        #print(f"Minimizing player: returning {minEvaluation}")
        return (minEvaluation, best_move, states_checked)

