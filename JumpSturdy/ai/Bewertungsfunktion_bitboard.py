#Bewertungsfunktion 


def evaluate_position(bitboards, color, maximizingP): ###Test Funktion für bitboards

    player_pieces = 0
    opponent_pieces = 0

    position_bonus_blue = 0
    position_bonus_red = 0

    blue_pieces = 0
    red_pieces = 0
    
	
	#Anzahl Pieces
    def count_pieces(bitboard):
        count = 0
        while bitboard:
            count += bitboard & 1
            bitboard >>= 1
        return count
    
    def calculate_position_bonus(bitboard):
        position_bonus = 0
        while bitboard:
            if bitboard & 1:
                position_bonus += 2
            bitboard >>= 1
        return position_bonus


    r_bitboard = bitboards['r']
    rr_bitboard = bitboards['rr']
    b_bitboard = bitboards['b']
    bb_bitboard = bitboards['bb']
    rb_bitboard = bitboards['rb']
    br_bitboard = bitboards['br']

    red_pieces += count_pieces(r_bitboard)
    red_pieces += 2 * count_pieces(rr_bitboard)
    blue_pieces += count_pieces(b_bitboard)
    blue_pieces += 2 * count_pieces(bb_bitboard)
    red_pieces += count_pieces(rb_bitboard)
    blue_pieces += count_pieces(rb_bitboard)
    red_pieces += count_pieces(br_bitboard)
    blue_pieces += count_pieces(br_bitboard)

    position_bonus_blue += calculate_position_bonus(rb_bitboard)
    position_bonus_red += calculate_position_bonus(br_bitboard)
    
    if red_pieces == 1:
        position_bonus_red -= 1
    if blue_pieces == 1:
        position_bonus_blue -= 1
    if red_pieces == 0:
        position_bonus_red -= 60
    if blue_pieces == 0:
        position_bonus_blue -= 60
    
	
	#Wer ist als nächstes dran
    next = ''

    if maximizingP == False and color == 'red':
        next = 'blue'
    if maximizingP == True and color == 'red':
        next = 'red'
    if maximizingP == False and color == 'blue':
        next = 'red'
    if maximizingP == True and color == 'blue':
        next = 'blue'        
    
    #Näher dran am Ziel

    closest_red_top = None
    closest_blue_top = None
    double_jump_red = False
    double_jump_blue = False

    def find_closest_piece_and_double(bitboards, double_bitboards):
        for row_idx in range(8):
            for col_idx in range(8):
                square_index = 63 - (row_idx * 8 + col_idx)
                for bitboard in bitboards:
                    if bitboard & (1 << square_index):
                        if any(double_bitboard & (1 << square_index) for double_bitboard in double_bitboards):
                            return row_idx, True
                        else:
                            return row_idx, False
        return None, False
    
    closest_red_top, _ = find_closest_piece_and_double([r_bitboard, rr_bitboard, br_bitboard], [])
    closest_blue_top, double_jump_blue = find_closest_piece_and_double([b_bitboard, bb_bitboard, rb_bitboard], [bb_bitboard, rb_bitboard])
    
    closest_red_bottom = None
    closest_blue_bottom = None

    def find_first_set_bit_from_bottom(bitboards, double_bitboards):
        for row_idx in reversed(range(8)):
            for col_idx in range(8):
                square_index = 63 - (row_idx * 8 + col_idx)
                for bitboard in bitboards:
                    if bitboard & (1 << square_index):
                        if any(double_bitboard & (1 << square_index) for double_bitboard in double_bitboards):
                            return 7 - row_idx, True
                        else:
                            return 7 - row_idx, False
        return None, False
    
    closest_red_bottom, double_jump_red = find_first_set_bit_from_bottom([r_bitboard, rr_bitboard, br_bitboard], [rr_bitboard, br_bitboard])
    closest_blue_bottom, _ = find_first_set_bit_from_bottom([b_bitboard, bb_bitboard, rb_bitboard], [])


    if closest_red_top != None and closest_red_bottom != None and closest_blue_top != None and closest_blue_bottom != None:
        if closest_blue_top == closest_red_bottom :  
                
            if next == 'blue' : 
                if double_jump_red == False and (double_jump_blue == False or double_jump_blue == True): 
                    position_bonus_blue += 5
                if double_jump_red == True and double_jump_blue == True: 
                    position_bonus_blue += 5
                if double_jump_red == True and double_jump_blue == False : 
                    position_bonus_blue -= 5

            if next == 'red' : 
                if double_jump_blue == False and (double_jump_red == False or double_jump_red == True): 
                    position_bonus_red += 5
                if double_jump_blue == True and double_jump_red == True: 
                    position_bonus_red += 5
                if double_jump_blue == True and double_jump_red == False : 
                    position_bonus_red -= 5    

        if closest_blue_top <= closest_red_top :          
            position_bonus_blue += 5
        if closest_red_bottom <= closest_blue_bottom :          
            position_bonus_red += 5

        if closest_red_bottom <  closest_blue_top and closest_red_bottom <= closest_blue_bottom and double_jump_blue == False: 
            position_bonus_red += 15
        if closest_blue_top < closest_red_bottom and closest_blue_top <= closest_red_top and double_jump_red == False: 
            position_bonus_blue += 15 
	
	
	
    if blue_pieces == 0 : 
        position_bonus_blue -= 500

    if red_pieces == 0 : 
        position_bonus_red -= 500

    blue_distances = 0
    red_distances = 0
    if red_pieces != 0 and blue_pieces != 0:
        for row_idx in range(8):
            for col_idx in range(8):
                square_index = 63 - (row_idx * 8 + col_idx)
                if r_bitboard & (1 << square_index):
                    red_distances += 8 - 1 - row_idx
                elif rr_bitboard & (1 << square_index):
                    red_distances += (8 - 1 - row_idx) * 1 - 1
                elif b_bitboard & (1 << square_index):
                    blue_distances += row_idx
                elif bb_bitboard & (1 << square_index):
                    blue_distances += row_idx * 2 - 1

    
    if blue_distances  < red_distances : 
        position_bonus_blue += 1
        if blue_distances + 2  < red_distances : 
            position_bonus_blue += 2
    elif red_distances  < blue_distances :
        position_bonus_red += 1
        if red_distances + 2  < blue_distances : 
            position_bonus_blue += 2  


    def is_position(bitboards, row_idx, col_idx):

        if not (0 <= row_idx < 8) or not (0 <= col_idx < 8):
            return False
        bit_position = (7 - row_idx) * 8 + col_idx
        for bitboard in bitboards:
            if (bitboard >> bit_position) & 1:
                return True

        return False
    
    def is_position_occupied(bitboards, row_idx, col_idx):

        if not (0 <= row_idx < 8) or not (0 <= col_idx < 8):
            return False
        bit_position = (7 - row_idx) * 8 + col_idx
        return not (bitboards['r'] & (1 << bit_position) or 
                bitboards['b'] & (1 << bit_position) or 
                bitboards['rr'] & (1 << bit_position) or 
                bitboards['bb'] & (1 << bit_position) or 
                bitboards['rb'] & (1 << bit_position) or 
                bitboards['br'] & (1 << bit_position))

    #Bonus Punkte: Schlagen/Gefahr oder kurz vorm Ziel

    for row_idx in range(8):
        for col_idx in range(8):
            if next == 'red':
                if bitboards['r'] & (1 << ((7 - row_idx) * 8 + col_idx)):
                    if row_idx < 8 - 1 and col_idx > 0 and col_idx < 8 - 1 and (is_position([bitboards['b']], row_idx + 1, col_idx - 1) or is_position([bitboards['b']], row_idx + 1, col_idx + 1)):
                        position_bonus_red -= 1
                        if red_pieces == 1 and blue_pieces > 1 :
                            position_bonus_red -= 10
                    if row_idx < 8 -1 and col_idx + 1> 0 and col_idx < 8 - 2 and (is_position([bitboards['bb'], bitboards['rb']], row_idx + 1, col_idx - 2) or is_position([bitboards['bb'], bitboards['rb']], row_idx + 1, col_idx + 2)):
                        position_bonus_red -= 1
                        if red_pieces == 1 and blue_pieces > 1:
                            position_bonus_red -= 10
                    if row_idx < 8 -2 and col_idx > 0 and col_idx < 8 - 1 and (is_position([bitboards['bb'], bitboards['rb']], row_idx + 2, col_idx - 1) or is_position([bitboards['bb'], bitboards['rb']], row_idx + 2, col_idx + 1)):
                        position_bonus_red -= 1   
                        if red_pieces == 1 and blue_pieces > 1:
                            position_bonus_red -= 10
                    if row_idx < 8 -1 and col_idx > 0 and col_idx < 8 - 1 and red_pieces == 1 and blue_pieces == 1 and is_position([bitboards['b']], row_idx + 1, col_idx):
                        position_bonus_red -= 50

                    if row_idx == 6 : 
                        position_bonus_red += 1
                        if row_idx == 6 and col_idx == 0 and is_position([bitboards['b'], bitboards['bb']], row_idx + 1, col_idx + 1) :
                            position_bonus_red += 80
                        if row_idx == 6 and col_idx == 7 and is_position([bitboards['b'], bitboards['bb']], row_idx + 1, col_idx - 1) :
                            position_bonus_red += 80
                        if row_idx == 6 and col_idx + 2 > 0 and col_idx < 8 - 2 and not is_position([bitboards['b']], row_idx + 1, col_idx-1) and not is_position([bitboards['b']], row_idx+1, col_idx+1) and not is_position([bitboards['bb'], bitboards['rb']], row_idx + 1, col_idx-2) and not is_position([bitboards['bb'], bitboards['rb']], row_idx + 1, col_idx+2): 
                            position_bonus_red += 10
                        if row_idx == 6 and not is_position_occupied(bitboards, row_idx + 1, col_idx): 
                            position_bonus_red += 50
                        if row_idx == 6 and is_position_occupied(bitboards, row_idx + 1, col_idx):                            
                            if blue_pieces == 1 and red_pieces > 1 :
                                position_bonus_red += 50
                            if red_pieces == 1 and blue_pieces >= 1:
                                position_bonus_red -= 50             
                if bitboards['b'] & (1 << ((7 - row_idx) * 8 + col_idx)):
                    if row_idx < 8 -1 and col_idx > 0 and col_idx < 8 - 1 and (is_position([bitboards['r']], row_idx - 1, col_idx-1) or is_position([bitboards['r']], row_idx-1, col_idx+1)):
                        position_bonus_blue -= 2
                        if blue_pieces == 1 and red_pieces >= 1 :
                            position_bonus_blue -= 30
                    if row_idx < 8 -1 and col_idx +1 > 0 and col_idx < 8 - 2 and ( is_position([bitboards['rr'], bitboards['br']], row_idx - 1, col_idx-2) or is_position([bitboards['rr'], bitboards['br']], row_idx - 1, col_idx+2)): 
                        position_bonus_blue -= 2
                        if blue_pieces == 1 and red_pieces >= 1 :
                            position_bonus_blue -= 30
                    if row_idx < 8 -2 and col_idx > 0 and col_idx < 8 - 1 and ( is_position([bitboards['rr'], bitboards['br']], row_idx - 2, col_idx-1) or is_position([bitboards['rr'], bitboards['br']], row_idx - 2, col_idx+1)): 
                        position_bonus_blue -= 2    
                        if blue_pieces == 1 and red_pieces >= 1 :
                            position_bonus_blue -= 30
                    if row_idx < 8 -1 and row_idx == 2 : 
                        position_bonus_blue += 2 
                        if row_idx < 8 -1 and col_idx > 0 and col_idx < 8 - 1 and (is_position([bitboards['r']], row_idx - 1, col_idx-1) or is_position([bitboards['r']], row_idx-1, col_idx+1) or is_position([bitboards['rr']], row_idx-2, col_idx+1) or is_position([bitboards['rr']], row_idx-2, col_idx-1)):
                            position_bonus_red -= 4
                        if row_idx < 8 -1 and col_idx + 1> 0 and col_idx < 8 - 2 and (is_position([bitboards['rr']], row_idx-1, col_idx-2)  or is_position([bitboards['rr']], row_idx-1, col_idx+2)):
                            position_bonus_red -= 4
                    if row_idx < 8 -1 and row_idx == 1 : 
                        position_bonus_blue += 2
                        if row_idx == 1 and col_idx == 0 and is_position([bitboards['rr']], row_idx-1, col_idx+1) and not is_position([bitboards['rr']], row_idx-1, col_idx+2):
                            position_bonus_blue += 50
                        if row_idx == 6 and col_idx == 7 and is_position([bitboards['rr']], row_idx-1, col_idx+1)  and not is_position([bitboards['rr']], row_idx-1, col_idx-2):
                            position_bonus_blue += 50
                        if row_idx == 1 and col_idx > 0 and col_idx < 8 - 2 and not is_position([bitboards['r']], row_idx - 1, col_idx-1) and not is_position([bitboards['r']], row_idx - 1, col_idx+1) and not is_position([bitboards['rr'], bitboards['br']], row_idx - 1, col_idx-2) and not is_position([bitboards['rr'], bitboards['br']], row_idx - 1, col_idx+2): 
                            position_bonus_blue += 15
                            if row_idx == 1 and not is_position_occupied(bitboards, row_idx - 1, col_idx): 
                                position_bonus_blue += 50
                            else:
                                if blue_pieces >= 1 and red_pieces == 1:
                                    position_bonus_blue += 40
                                if blue_pieces == 1 and red_pieces > 1:
                                    position_bonus_blue -= 40   
                        else:
                            position_bonus_blue -= 15

                if (bitboards['rr'] & (1 << ((7 - row_idx) * 8 + col_idx))) or (bitboards['br'] & (1 << ((7 - row_idx) * 8 + col_idx))):
                    position_bonus_red += 1
                    if row_idx < 8 -1 and col_idx > 0 and col_idx < 8 - 1 and (is_position([bitboards['b']], row_idx + 1, col_idx-1) or is_position([bitboards['b']], row_idx + 1, col_idx+1) ): 
                        position_bonus_red -= 1
                        if (red_pieces == 2 and bitboards['rr'] & (1 << ((7 - row_idx) * 8 + col_idx))) or (red_pieces == 1 and bitboards['br'] & (1 << ((7 - row_idx) * 8 + col_idx))):
                            position_bonus_red -= 10
                    if row_idx < 8 -1 and col_idx > 0 and col_idx < 8 - 2 and ( is_position([bitboards['rb'], bitboards['bb']], row_idx + 1, col_idx-2) or is_position([bitboards['rb'], bitboards['bb']], row_idx - 1, col_idx+2)) :   
                        position_bonus_red -= 1
                        if (red_pieces == 2 and bitboards['rr'] & (1 << ((7 - row_idx) * 8 + col_idx))) or (red_pieces == 1 and bitboards['br'] & (1 << ((7 - row_idx) * 8 + col_idx))):
                            position_bonus_red -= 10
                    if row_idx < 8 -2 and col_idx > 0 and col_idx < 8 - 1 and  ( is_position([bitboards['rb'], bitboards['bb']], row_idx + 2, col_idx-1) or is_position([bitboards['rb'], bitboards['bb']], row_idx - 2, col_idx+1)):
                        position_bonus_red -= 1
                        if (red_pieces == 2 and bitboards['rr'] & (1 << ((7 - row_idx) * 8 + col_idx))) or (red_pieces == 1 and bitboards['br'] & (1 << ((7 - row_idx) * 8 + col_idx))):
                            position_bonus_red -= 10
                    if row_idx == 6 or row_idx == 5 :      
                        position_bonus_red += 30
                        if row_idx == 6 and col_idx +1 > 0 and col_idx < 8 - 2 and not is_position([bitboards['b']], row_idx + 1, col_idx-1) and not is_position([bitboards['b']], row_idx + 1, col_idx+1) and not is_position([bitboards['rb'], bitboards['bb']], row_idx + 1, col_idx-2) and not is_position([bitboards['rb'], bitboards['bb']], row_idx + 1, col_idx+2):    
                            position_bonus_red += 40  
                            if row_idx == 6 and col_idx == 0 and (is_position([bitboards['bb']], row_idx + 1, col_idx+2) or is_position([bitboards['b']], row_idx + 1, col_idx+1)):    
                                position_bonus_red -= 5
                            if row_idx == 6 and col_idx == 8 and (is_position([bitboards['bb']], row_idx + 1, col_idx-2)  or is_position([bitboards['b']], row_idx + 1, col_idx-1) ):
                                position_bonus_red -= 5            
                        if row_idx == 5 and col_idx + 1 > 0 and col_idx < 8 - 2 and not is_position([bitboards['b']], row_idx + 1, col_idx-1)  and not is_position([bitboards['b']], row_idx + 1, col_idx+1)  and not is_position([bitboards['rb'], bitboards['bb']], row_idx + 1, col_idx-2) and not is_position([bitboards['rb'], bitboards['bb']], row_idx + 1, col_idx+2) and not is_position([bitboards['rb'], bitboards['bb']], row_idx + 2, col_idx-1) and not is_position([bitboards['rb'], bitboards['bb']], row_idx + 2, col_idx+1):    
                            position_bonus_red += 40
                            if row_idx == 5 and col_idx == 0 and (is_position([bitboards['bb']], row_idx + 1, col_idx+2) or is_position([bitboards['bb']], row_idx + 2, col_idx+1) or is_position([bitboards['b']], row_idx + 1, col_idx+1)):
                                position_bonus_red -= 5
                            if row_idx == 5 and col_idx == 8 and (is_position([bitboards['bb']], row_idx + 1, col_idx-2) or is_position([bitboards['bb']], row_idx + 2, col_idx-1) or is_position([bitboards['b']], row_idx + 1, col_idx-1)):
                                position_bonus_red -= 5   
                        else:
                            position_bonus_red -= 1
                if (bitboards['bb'] & (1 << ((7 - row_idx) * 8 + col_idx))) or (bitboards['rb'] & (1 << ((7 - row_idx) * 8 + col_idx))):
                    position_bonus_blue += 1
                    if row_idx < 8 -1 and col_idx > 0 and col_idx < 8 - 1 and (is_position([bitboards['r']], row_idx - 1, col_idx-1) or is_position([bitboards['r']], row_idx - 1, col_idx+1)): 
                        position_bonus_blue -= 2
                        if (blue_pieces == 2 and bitboards['bb'] & (1 << ((7 - row_idx) * 8 + col_idx))) or (blue_pieces == 1 and bitboards['rb'] & (1 << ((7 - row_idx) * 8 + col_idx))):
                            position_bonus_blue -= 30
                    if row_idx < 8 -1 and col_idx > 0 and col_idx < 8 - 2 and (is_position([bitboards['rr'], bitboards['br']], row_idx - 1, col_idx-2) or is_position([bitboards['rr'], bitboards['br']], row_idx - 1, col_idx+2)):   
                        position_bonus_blue -= 2
                        if (blue_pieces == 2 and bitboards['bb'] & (1 << ((7 - row_idx) * 8 + col_idx))) or (blue_pieces == 1 and bitboards['rb'] & (1 << ((7 - row_idx) * 8 + col_idx))):
                            position_bonus_blue -= 30
                    if row_idx < 8 -2 and col_idx > 0 and col_idx < 8 - 1 and  ( is_position([bitboards['rr'], bitboards['br']], row_idx - 2, col_idx-1) or is_position([bitboards['rr'], bitboards['br']], row_idx - 2, col_idx+1)):
                        position_bonus_blue -= 2
                        if (blue_pieces == 2 and bitboards['bb'] & (1 << ((7 - row_idx) * 8 + col_idx))) or (blue_pieces == 1 and bitboards['rb'] & (1 << ((7 - row_idx) * 8 + col_idx))):
                            position_bonus_blue -= 30

                    if row_idx == 1 or row_idx == 2 :      
                        position_bonus_blue += 1                        
                        if row_idx == 2 and col_idx +1 > 0 and col_idx < 8 - 2 and not is_position([bitboards['r']], row_idx - 1, col_idx-1) and not is_position([bitboards['r']], row_idx - 1, col_idx+1) and not is_position([bitboards['rr'], bitboards['br']], row_idx - 1, col_idx-2) and not is_position([bitboards['rr'], bitboards['br']], row_idx - 1, col_idx+2) and not is_position([bitboards['rr'], bitboards['br']], row_idx - 2, col_idx+1) and not is_position([bitboards['rr'], bitboards['br']], row_idx - 2, col_idx-1):    
                            position_bonus_red += 50  
                        if row_idx == 2 and col_idx == 0 and not is_position([bitboards['r']], row_idx - 1, col_idx+1) and not is_position([bitboards['rr'], bitboards['br']], row_idx - 1, col_idx+2) and not is_position([bitboards['rr'], bitboards['br']], row_idx - 2, col_idx+1):  
                            position_bonus_blue += 50  
                        if row_idx == 2 and col_idx == 7 and not is_position([bitboards['r']], row_idx - 1, col_idx-1) and not is_position([bitboards['rr'], bitboards['br']], row_idx - 1, col_idx-2) and not is_position([bitboards['rr'], bitboards['br']], row_idx - 2, col_idx-1):  
                            position_bonus_blue += 50 
                        if row_idx == 1 and col_idx == 0 and not is_position([bitboards['r']], row_idx - 1, col_idx+1) and not is_position([bitboards['rr'], bitboards['br']], row_idx - 1, col_idx+2):  
                            position_bonus_blue += 50  
                        if row_idx == 1 and col_idx == 7 and not is_position([bitboards['r']], row_idx - 1, col_idx-1) and not is_position([bitboards['rr'], bitboards['br']], row_idx - 1, col_idx-2):  
                            position_bonus_blue += 50    
                        if row_idx == 1 and col_idx +1 > 0 and col_idx < 8 - 2 and not is_position([bitboards['r']], row_idx - 1, col_idx-1) and not is_position([bitboards['r']], row_idx - 1, col_idx+1) and not is_position([bitboards['rr'], bitboards['br']], row_idx - 1, col_idx-2) and not is_position([bitboards['rr'], bitboards['br']], row_idx - 1, col_idx+2):    
                            position_bonus_red += 50  
                        else: 
                            position_bonus_blue -=60
            
            if next == 'blue' : 
                if bitboards['r'] & (1 << ((7 - row_idx) * 8 + col_idx)):
                    if row_idx < 8 -1 and col_idx > 0 and col_idx < 8 - 1 and (is_position([bitboards['b']], row_idx + 1, col_idx-1) or is_position([bitboards['b']], row_idx + 1, col_idx+1)): 
                        position_bonus_red -= 2
                        if red_pieces == 1 and blue_pieces >= 1:
                            position_bonus_red -= 30
                    if row_idx < 8 -1 and col_idx + 1> 0 and col_idx < 8 - 2 and(is_position([bitboards['rb'], bitboards['bb']], row_idx + 1, col_idx-2) or is_position([bitboards['rb'], bitboards['bb']], row_idx + 1, col_idx+2)):
                        position_bonus_red -= 2
                        if red_pieces == 1 and blue_pieces >= 1:
                            position_bonus_red -= 30
                    if row_idx < 8 -2 and col_idx > 0 and col_idx < 8 - 1 and(is_position([bitboards['rb'], bitboards['bb']], row_idx + 2, col_idx-1) or is_position([bitboards['rb'], bitboards['bb']], row_idx + 2, col_idx+1)):
                        position_bonus_red -= 2   
                        if red_pieces == 1 and blue_pieces >= 1:
                            position_bonus_red -= 30
                    if row_idx < 8 -1 and row_idx == 5 : 
                        position_bonus_red += 2
                        if row_idx < 8 -1 and col_idx > 0 and col_idx < 8 - 1 and (is_position([bitboards['b']], row_idx + 1, col_idx-1) or is_position([bitboards['b']], row_idx + 1, col_idx+1) or is_position([bitboards['bb']], row_idx + 2, col_idx+1) or is_position([bitboards['bb']], row_idx + 2, col_idx-1)):
                            position_bonus_red -= 4
                        if row_idx < 8 -1 and col_idx + 1> 0 and col_idx < 8 - 2 and (is_position([bitboards['bb']], row_idx + 1, col_idx-2) or is_position([bitboards['bb']], row_idx + 1, col_idx+2)):
                            position_bonus_red -= 4          
                    if row_idx < 8 -1 and row_idx == 6 : 
                        position_bonus_red += 2
                        if row_idx == 6 and col_idx == 0 and is_position([bitboards['bb']], row_idx + 1, col_idx+1) and not is_position([bitboards['bb']], row_idx + 1, col_idx+2):
                            position_bonus_red += 10
                            
                        if row_idx == 6 and col_idx == 7 and is_position([bitboards['bb']], row_idx + 1, col_idx-1) and not is_position([bitboards['bb']], row_idx + 1, col_idx-2):
                            position_bonus_red += 100
                        if row_idx == 6 and col_idx + 2 > 0 and col_idx < 8 - 2 and not is_position([bitboards['b']], row_idx + 1, col_idx-1) and not is_position([bitboards['b']], row_idx + 1, col_idx+1) and not is_position([bitboards['rb'], bitboards['bb']], row_idx + 1, col_idx-2) and not is_position([bitboards['rb'], bitboards['bb']], row_idx + 1, col_idx+2): 
                            position_bonus_red += 15
                            if row_idx == 6 and not is_position_occupied(bitboards, row_idx + 1, col_idx): 
                                position_bonus_red += 50
                            else: 
                                if blue_pieces == 1 and red_pieces >= 1:
                                    position_bonus_red += 40
                                if red_pieces == 1 and blue_pieces > 1:
                                    position_bonus_red -= 40
  
                        else:
                            position_bonus_red -= 15
                if bitboards['b'] & (1 << ((7 - row_idx) * 8 + col_idx)):
                    if row_idx < 8 -1 and col_idx > 0 and col_idx < 8 - 1 and (is_position([bitboards['r']], row_idx - 1, col_idx-1) or is_position([bitboards['r']], row_idx - 1, col_idx+1)):
                        position_bonus_blue -= 1
                        if blue_pieces == 1 and red_pieces > 1 :
                            position_bonus_blue -= 10
                    if row_idx < 8 -1 and col_idx +1 > 0 and col_idx < 8 - 2 and ( is_position([bitboards['rr'], bitboards['br']], row_idx - 1, col_idx-2) or is_position([bitboards['rr'], bitboards['br']], row_idx - 1, col_idx+2)): 
                        position_bonus_blue -= 1
                        if blue_pieces == 1 and red_pieces > 1 :
                            position_bonus_blue -= 10
                    if row_idx < 8 -2 and col_idx > 0 and col_idx < 8 - 1 and ( is_position([bitboards['rr'], bitboards['br']], row_idx - 2, col_idx-1) or is_position([bitboards['rr'], bitboards['br']], row_idx - 2, col_idx+1)): 
                        position_bonus_blue -= 1    
                        if blue_pieces == 1 and red_pieces > 1 :
                            position_bonus_blue -= 10
                    if row_idx < 8 -1 and col_idx > 0 and col_idx < 8 - 1 and red_pieces == 1 and blue_pieces == 1 and is_position([bitboards['r']], row_idx - 1, col_idx):
                        position_bonus_blue -= 50    
                    if row_idx < 8 -1 and row_idx == 1 : 
                        position_bonus_blue += 1
                        if row_idx == 1 and col_idx == 0 and is_position([bitboards['r'], bitboards['rr']], row_idx - 1, col_idx+1): 
                            position_bonus_blue += 50
                        if row_idx == 1 and col_idx == 7 and is_position([bitboards['r'], bitboards['rr']], row_idx - 1, col_idx-1): 
                            position_bonus_blue += 50            
                        if row_idx == 1 and col_idx + 2 > 0 and col_idx < 8 - 2 and not is_position([bitboards['r']], row_idx - 1, col_idx - 1) and not is_position([bitboards['r']], row_idx - 1, col_idx + 1) and not is_position([bitboards['rr'], bitboards['br']], row_idx - 1, col_idx-2) and not is_position([bitboards['rr'], bitboards['br']], row_idx - 1, col_idx+2): 
                            position_bonus_blue += 10
                        if row_idx == 1 and not is_position_occupied(bitboards, row_idx - 1, col_idx): 
                            position_bonus_blue += 50
                        if row_idx == 1 and is_position_occupied(bitboards, row_idx - 1, col_idx):
                            if red_pieces >= 1  and blue_pieces == 1:
                                position_bonus_blue -= 50
                            if blue_pieces > 1 and red_pieces == 1 : 
                                    position_bonus_blue += 50    

                if (bitboards['rr'] & (1 << ((7 - row_idx) * 8 + col_idx))) or (bitboards['br'] & (1 << ((7 - row_idx) * 8 + col_idx))):
                    position_bonus_red += 1
                    
                    if row_idx < 8-1 and col_idx > 0 and col_idx < 8 - 1 and (is_position([bitboards['b']], row_idx + 1, col_idx - 1) or is_position([bitboards['b']], row_idx + 1, col_idx + 1)): 
                        position_bonus_red -= 2
                        if (red_pieces == 2 and bitboards['rr'] & (1 << ((7 - row_idx) * 8 + col_idx))) or (red_pieces == 1 and bitboards['br'] & (1 << ((7 - row_idx) * 8 + col_idx))):
                            position_bonus_red -= 30
                    if row_idx < 8-1 and col_idx > 0 and col_idx < 8 - 2 and ( is_position([bitboards['rb'], bitboards['bb']], row_idx + 1, col_idx-2) or is_position([bitboards['rb'], bitboards['bb']], row_idx - 1, col_idx+2)) :   
                        position_bonus_red -= 2
                        if (red_pieces == 2 and bitboards['rr'] & (1 << ((7 - row_idx) * 8 + col_idx))) or (red_pieces == 1 and bitboards['br'] & (1 << ((7 - row_idx) * 8 + col_idx))):
                            position_bonus_red -= 30
                    if row_idx < 8-2 and col_idx > 0 and col_idx < 8 - 1 and ( is_position([bitboards['rb'], bitboards['bb']], row_idx + 2, col_idx-1) or is_position([bitboards['rb'], bitboards['bb']], row_idx - 2, col_idx+1)):
                        position_bonus_red -= 2
                        if (red_pieces == 2 and bitboards['rr'] & (1 << ((7 - row_idx) * 8 + col_idx))) or (red_pieces == 1 and bitboards['br'] & (1 << ((7 - row_idx) * 8 + col_idx))):
                            position_bonus_red -= 30
                    if row_idx == 6 or row_idx == 5 :      
                        position_bonus_red += 1
                        if row_idx == 5 and col_idx +1 > 0 and col_idx < 8 - 2 and not is_position([bitboards['b']], row_idx + 1, col_idx - 1) and not is_position([bitboards['b']], row_idx + 1, col_idx + 1) and not is_position([bitboards['rb'], bitboards['bb']], row_idx + 1, col_idx-2) and not is_position([bitboards['rb'], bitboards['bb']], row_idx + 1, col_idx+2) and not is_position([bitboards['rb'], bitboards['bb']], row_idx + 2, col_idx+1) and not is_position([bitboards['rb'], bitboards['bb']], row_idx + 2, col_idx-1):    
                            position_bonus_red += 50  
                        if row_idx == 5 and col_idx == 0 and not is_position([bitboards['b']], row_idx + 1, col_idx + 1) and not is_position([bitboards['rb'], bitboards['bb']], row_idx + 1, col_idx+2) and not is_position([bitboards['rb'], bitboards['bb']], row_idx + 2, col_idx+1):  
                            position_bonus_blue += 50  
                        if row_idx == 5 and col_idx == 7 and not is_position([bitboards['b']], row_idx + 1, col_idx - 1) and not is_position([bitboards['rb'], bitboards['bb']], row_idx + 1, col_idx-2) and not is_position([bitboards['rb'], bitboards['bb']], row_idx + 2, col_idx-1):  
                            position_bonus_blue += 50 
                        if row_idx == 6 and col_idx == 0 and not is_position([bitboards['b']], row_idx + 1, col_idx + 1) and not is_position([bitboards['rb'], bitboards['bb']], row_idx + 1, col_idx+2):  
                            position_bonus_blue += 50  
                        if row_idx == 6 and col_idx == 7 and not is_position([bitboards['b']], row_idx + 1, col_idx - 1) and not is_position([bitboards['rb'], bitboards['bb']], row_idx + 1, col_idx-2):  
                            position_bonus_blue += 50    
                        if row_idx == 6 and col_idx +1 > 0 and col_idx < 8 - 2 and not is_position([bitboards['b']], row_idx + 1, col_idx - 1) and not is_position([bitboards['b']], row_idx + 1, col_idx + 1) and not is_position([bitboards['rb'], bitboards['bb']], row_idx + 1, col_idx-2) and not is_position([bitboards['rb'], bitboards['bb']], row_idx + 1, col_idx+2):    
                            position_bonus_red += 50  
                        else: 
                            position_bonus_blue -=60
                if (bitboards['bb'] & (1 << ((7 - row_idx) * 8 + col_idx))) or (bitboards['rb'] & (1 << ((7 - row_idx) * 8 + col_idx))):
                    position_bonus_blue += 1
                    if row_idx < 8-1 and col_idx > 0 and col_idx < 8 - 1 and (is_position([bitboards['r']], row_idx - 1, col_idx - 1) or is_position([bitboards['r']], row_idx - 1, col_idx + 1)): 
                        position_bonus_blue -= 1
                        if (blue_pieces == 2 and bitboards['bb'] & (1 << ((7 - row_idx) * 8 + col_idx))) or (blue_pieces == 1 and bitboards['rb'] & (1 << ((7 - row_idx) * 8 + col_idx))):
                            position_bonus_blue -= 10
                    if row_idx < 8-1 and col_idx > 0 and col_idx < 8 - 2 and ( is_position([bitboards['rr'], bitboards['br']], row_idx - 1, col_idx-2) or is_position([bitboards['rr'], bitboards['br']], row_idx - 1, col_idx+2)) :   
                        position_bonus_blue -= 1
                        if (blue_pieces == 2 and bitboards['bb'] & (1 << ((7 - row_idx) * 8 + col_idx))) or (blue_pieces == 1 and bitboards['rb'] & (1 << ((7 - row_idx) * 8 + col_idx))):
                            position_bonus_blue -= 10
                    if row_idx < 8-2 and col_idx > 0 and col_idx < 8 - 1 and  ( is_position([bitboards['rr'], bitboards['br']], row_idx - 2, col_idx-1) or is_position([bitboards['rr'], bitboards['br']], row_idx - 2, col_idx+1)):
                        position_bonus_blue -= 1
                        if (blue_pieces == 2 and bitboards['bb'] & (1 << ((7 - row_idx) * 8 + col_idx))) or (blue_pieces == 1 and bitboards['rb'] & (1 << ((7 - row_idx) * 8 + col_idx))):
                            position_bonus_blue -= 10

                    if row_idx == 1 or row_idx == 2 :      
                        position_bonus_blue += 30
                        if row_idx == 1 and col_idx + 1 > 0 and col_idx < 8 - 2 and not is_position([bitboards['r']], row_idx - 1, col_idx - 1) and not is_position([bitboards['r']], row_idx - 1, col_idx + 1) and not is_position([bitboards['rr'], bitboards['br']], row_idx - 1, col_idx-2) and not is_position([bitboards['rr'], bitboards['br']], row_idx - 1, col_idx+2):    
                            position_bonus_blue += 40
                            if row_idx == 1 and col_idx == 0 and (is_position([bitboards['rr']], row_idx - 1, col_idx + 2) or is_position([bitboards['r']], row_idx - 1, col_idx + 1)):    
                                position_bonus_blue -= 5
                            if row_idx == 1 and col_idx == 8 and (is_position([bitboards['rr']], row_idx - 1, col_idx - 2) or is_position([bitboards['r']], row_idx + 1, col_idx - 1)):    
                                position_bonus_blue -= 5  
                        if row_idx == 2 and col_idx + 1 > 0 and col_idx < 8 - 2 and not is_position([bitboards['r']], row_idx - 1, col_idx - 1) and not is_position([bitboards['r']], row_idx - 1, col_idx + 1) and not is_position([bitboards['rr'], bitboards['br']], row_idx - 1, col_idx-2) and not is_position([bitboards['rr'], bitboards['br']], row_idx - 1, col_idx+2) and not is_position([bitboards['rr'], bitboards['br']], row_idx - 2, col_idx-1) and not is_position([bitboards['rr'], bitboards['br']], row_idx - 2, col_idx+1):    
                            position_bonus_blue += 40 
                            if row_idx == 2 and col_idx == 0 and (is_position([bitboards['rr']], row_idx - 1, col_idx + 2) or is_position([bitboards['rr']], row_idx - 2, col_idx + 1) or is_position([bitboards['r']], row_idx - 1, col_idx + 1)):  
                                position_bonus_blue -= 5  
                            if row_idx == 2 and col_idx == 8 and (is_position([bitboards['rr']], row_idx - 1, col_idx - 2) or is_position([bitboards['rr']], row_idx - 2, col_idx - 1) or is_position([bitboards['r']], row_idx - 1, col_idx - 1)):  
                                position_bonus_blue -= 5    
                        else:
                            position_bonus_blue -= 1 
    position_bonus_player = 0
    position_bonus_opponent = 0
    if color == 'red' :
        player_pieces = red_pieces
        opponent_pieces = blue_pieces
        position_bonus_player = position_bonus_red
        position_bonus_opponent = position_bonus_blue
        
    if color == 'blue' :
        player_pieces = blue_pieces
        opponent_pieces = red_pieces
        
        position_bonus_player = position_bonus_blue
        position_bonus_opponent = position_bonus_red
                        
    #print((player_pieces - opponent_pieces) + (position_bonus_player - position_bonus_opponent))
    

    return (player_pieces - opponent_pieces) + (position_bonus_player - position_bonus_opponent)