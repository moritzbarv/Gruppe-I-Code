import math 
import random 

import sys 
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from board.Bitboard import get_color, change_board, generate_moves, game_over, convert_fen_to_bitboard


#Monte Carlo Algorithm

#Calculate UCT Valu
def uct(total_visits, node_wins, node_visits, c_param=1):

    if node_visits == 0:
        return float('inf')
    return (node_wins / node_visits) + c_param * math.sqrt(math.log(total_visits) / node_visits)


#Select best node/highest UCT
def select(nodes):

    total_visits = sum(node['visits'] for node in nodes)
    best_node = max(nodes, key=lambda node: uct(total_visits, node['wins'], node['visits']))
    return best_node

#Expand with new child node
def expand(node):

    move = node['untried_moves'].pop()
    new_bitboard = change_board(node['bitboard'], move[0], move[1])
    next_player = 'blue' if node['current_player'] == 'red' else 'red'
    child_node = {
        'bitboard': new_bitboard,
        'current_player': next_player,
        'parent': node,
        'children': [],
        'visits': 0,
        'wins': 0,
        'untried_moves': generate_moves(new_bitboard, next_player),
        'move' : move
    }
    node['children'].append(child_node)
    
    return child_node

#Simulate a game
def simulate_random_game(bitboard, current_player):

    while True:
        possible_moves_list = generate_moves(bitboard, current_player)
        if not possible_moves_list:
            break
        move = random.choice(possible_moves_list)
        bitboard = change_board(bitboard, move[0], move[1])
        current_player = 'blue' if current_player == 'red' else 'red'
        if game_over(bitboard, current_player):
            break
    if current_player == 'red':
        return -1  #You lost
    else:
        return 1  #You won

#Backpropagate the result
def backpropagate(node, result):

    while node:
        node['visits'] += 1
        node['wins'] += result
        node = node['parent']

#Monte Carlo Tree Search
def mcts(root, iterations):
    for _ in range(iterations):
        node = root

        while node['untried_moves'] == [] and node['children'] != []:
            node = select(node['children'])

        if node['untried_moves'] != []:
            node = expand(node)

        result = simulate_random_game(node['bitboard'], node['current_player'])
        backpropagate(node, result)
    return select(root['children'])

fen = 'bb4bb/3b02b01/r07/2r02r02/4b03/2b02r02/2r01r01r0r0/1r01r02 r'
color = get_color(fen)
bitboards = convert_fen_to_bitboard(fen)

#Wurzelknoten
root_node = {
    'bitboard': bitboards,
    'current_player': color,
    'parent': None,
    'children': [],
    'visits': 0,
    'wins': 0,
    'untried_moves': generate_moves(bitboards, color)
}

#Ausführen
best_move_node = mcts(root_node, 1000)  # 1000 Iterationen
print(best_move_node)
print(f"Best move: {best_move_node['move']}")
