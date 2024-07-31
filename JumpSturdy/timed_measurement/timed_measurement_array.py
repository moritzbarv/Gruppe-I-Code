import time 
import sys 
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from board.Array import generate_moves, convert_fen_to_board
from ai.Bewertungsfunktion_array import evaluate_position
from ai.Minimax_array import minimax, minimax2, minimax3, minimax4, minimax_zugsortierung, minimax_pvs, minimax_pvs_ruhesuche

#FEN String ... (convert)


#Time measured for generate moves
def timed_measurement_generate_moves(board, color, maxP , iterations):
    start_time = time.time()
    for i in range(iterations):
        generate_moves(board, color)
    end_time = time.time()
    duration = (end_time - start_time) * 1000  
    print(iterations , "Iterationen dauern: ", duration, "Millisekunden")

#Time measured for evaluate position
def timed_measurement_evaluation(board, color, maxP , iterations):
    start_time = time.time()
    for i in range(iterations):
        evaluate_position(board, color, maxP)
    end_time = time.time()
    duration = (end_time - start_time) * 1000  
    print(iterations , "Iterationen dauern: ", duration, "Millisekunden")

#Time measured for minimax with alphabeta 
def timed_measurement_minimax(board, move, depth, alpha, beta, maxP, color , iterations):
    start_time = time.time()
    for i in range(iterations):
        minimax(board, move, depth, alpha, beta, maxP, color)
    end_time = time.time()
    duration = (end_time - start_time) * 1000  
    print(iterations , "Iteration dauert: ", duration, "Millisekunden")

#Time measured for minimax without alphabeta 
def timed_measurement_minimax2(board, move, depth, maxP, color , iterations):
    start_time = time.time()
    for i in range(iterations):
        minimax2(board, move, depth, maxP, color)
    end_time = time.time()
    duration = (end_time - start_time) * 1000 
    print(iterations , "Iteration dauert: ", duration, "Millisekunden")

#Time measured for minimax without alphabeta + states checked
def timed_measurement_minimax3(board, move, depth, maxP, color , status_checked, iterations):
    start_time = time.time()
    for i in range(iterations):
        minimax3(board, move, depth, maxP, color, status_checked)
    end_time = time.time()
    duration = (end_time - start_time) * 1000 
    print(iterations , "Iteration dauert: ", duration, "Millisekunden")

#Time measured for minimax with alphabeta + states checked
def timed_measurement_minimax4(board, move, depth, alpha, beta, maxP, color , status_checked, iterations):
    start_time = time.time()
    for i in range(iterations):
        x = minimax4(board, move, depth, alpha, beta, maxP, color, status_checked)
    end_time = time.time()
    duration = (end_time - start_time) * 1000  
    print(iterations , "Iteration dauert: ", duration, "Millisekunden")
    return (duration, x[1], x[2])

#Timed measured for minimax with Alpha Beta + states checked + Zugsortierung
def timed_measurement_minimax_zugsortierung(board, move, depth, alpha, beta, maxP, color , total_time, status_checked, zuege ,iterations):
    start_time = time.time()
    for i in range(iterations):
        x = minimax_zugsortierung(board, move, depth, alpha, beta, maxP, color, total_time, status_checked, zuege)
    end_time = time.time()
    duration = (end_time - start_time) * 1000 
    print(iterations , "Iteration dauert: ", duration, "Millisekunden")
    return (duration, x[1], x[2])

#Timed Measurement for minimax with Alpha Beta + states checked + Zugsortierung + PVS
def timed_measurement_pvs(board, move, depth, alpha, beta, maxP, color , total_time, status_checked, zuege,  iterations):
    start_time = time.time()
    for i in range(iterations):
        x = minimax_pvs(board, move, depth, alpha, beta, maxP, color, total_time, status_checked, zuege)
    end_time = time.time()
    duration = (end_time - start_time) * 1000 
    print(iterations , "Iteration dauert: ", duration, "Millisekunden")
    return (duration, x[1], x[2])

#Timed Measurement for minimax with Alpha Beta + states checked + Zugsortierung + PVS + Ruhesuche
def timed_measurement_pvs_ruhesuche(board, move, depth, alpha, beta, maxP, color , total_time, status_checked, zuege,  iterations):
    start_time = time.time()
    for i in range(iterations):
        x = minimax_pvs_ruhesuche(board, move, depth, alpha, beta, maxP, color, total_time, status_checked, zuege)
    end_time = time.time()
    duration = (end_time - start_time) * 1000 
    print(iterations , "Iteration dauert: ", duration, "Millisekunden")
    return (duration, x[1], x[2])

#Run function





